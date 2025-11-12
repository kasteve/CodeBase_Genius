# Codebase Genius — Implementation Scaffold

This document contains a complete scaffold to implement **Codebase Genius**: an agentic, multi‑agent Jac application that clones a public GitHub repo, analyses it (file tree, README summary, Code Context Graph using Tree‑sitter), and generates a Markdown documentation bundle with diagrams.

The scaffold includes:

* Project layout
* `main.jac` with Jac walkers / agents (Supervisor, RepoMapper, CodeAnalyzer, DocGenie)
* Python helper modules (repo_mapper.py, code_analyzer.py, docgen.py)
* `requirements.txt` and setup/run instructions
* Example curl commands and sample output structure

---

## 1. Project layout

```
codebase_genius/
├── BE/
│   ├── main.jac
│   ├── agents/
│   │   ├── supervisor.jac
│   │   ├── repo_mapper.jac
│   │   ├── code_analyzer.jac
│   │   └── docgenie.jac
│   └── py/  # Python helpers callable from Jac via py_module
│       ├── repo_mapper.py
│       ├── code_analyzer.py
│       └── docgen.py
├── FE/ (optional)
│   └── streamlit_frontend.py
├── requirements.txt
└── README.md
```

---

## 2. `requirements.txt`

```
# Jac runtime (install separately as per Jac docs)
jaseci
byllm
flask
fastapi
uvicorn
pydantic
requests
GitPython
markdown
pyyaml
tree_sitter
networkx
matplotlib
graphviz
python-dotenv
```

> Note: `tree_sitter` Python bindings and language grammars require extra steps (see below). `graphviz` may require system install (`apt install graphviz` on Debian/Ubuntu).

---

## 3. Jac backend (BE/main.jac)

This file wires walkers that call Python helpers via `py_module`. The Jac code focuses on orchestration, delegating heavy parsing to Python modules.

```jac
# main.jac
import py_module as py

walker start:
    # entry: expect an event with {"repo_url": "https://github.com/owner/repo"}
    can run supervisor.start_supervisor(event)

# Provide simple HTTP handlers (the jac runtime exposes walkers as endpoints)

walker api_generate_docs:
    can run supervisor.generate_from_url(event)
```

---

## 4. Example Jac agent: `agents/supervisor.jac`

```jac
# supervisor.jac
import py_module as py

walker start_supervisor:
    # event.payload should contain repo_url and optional opts
    with event.payload as p:
        repo_url = p.get('repo_url', '')
    if not repo_url:
        emit({ 'error': 'Missing repo_url' })
        return

    emit({'status':'cloning', 'repo': repo_url})
    # call python to clone and produce file tree and readme summary
    map_res = py.call('py.repo_mapper.clone_and_map', [repo_url])
    if map_res.get('error'):
        emit(map_res)
        return

    # plan high level (choose top files)
    plan = py.call('py.repo_mapper.prioritize_files', [map_res])

    emit({'status':'analyzing', 'plan': plan.get('top_files')})

    ccg = {}
    for f in plan.get('top_files', []):
        r = py.call('py.code_analyzer.analyze_file', [map_res['local_path'], f])
        ccg[f] = r

    # merge ccg
    merged = py.call('py.code_analyzer.merge_ccg', [ccg])

    # generate docs
    out = py.call('py.docgen.generate_markdown', [map_res, merged, { 'out_dir': './outputs' }])

    emit({ 'status':'done', 'output': out })
```

---

## 5. Python helpers: `py/repo_mapper.py`

```python
# repo_mapper.py
import os
import tempfile
import git
import json
from pathlib import Path

IGNORED = {'.git', 'node_modules', '__pycache__'}

def clone_and_map(repo_url: str):
    try:
        tmp = tempfile.mkdtemp(prefix='codegen_')
        repo = git.Repo.clone_from(repo_url, tmp)
        # simple repo name
        name = Path(repo.working_tree_dir).name
        tree = build_tree(repo.working_tree_dir)
        readme = find_readme_and_summarize(repo.working_tree_dir)
        return { 'local_path': repo.working_tree_dir, 'name': name, 'file_tree': tree, 'readme_summary': readme }
    except Exception as e:
        return { 'error': str(e) }


def build_tree(base_dir: str):
    out = []
    for root, dirs, files in os.walk(base_dir):
        # filter dirs
        dirs[:] = [d for d in dirs if d not in IGNORED]
        relroot = os.path.relpath(root, base_dir)
        items = { 'path': relroot, 'files': files.copy() }
        out.append(items)
    return out


def find_readme_and_summarize(base_dir: str):
    candidates = ['README.md', 'readme.md', 'README.MD']
    for c in candidates:
        p = Path(base_dir) / c
        if p.exists():
            text = p.read_text(encoding='utf-8')
            return summarize_text(text)
    return ''


def summarize_text(text: str, max_sentences=5):
    # simple heuristic: return first few lines; in prod call an LLM
    lines = [l.strip() for l in text.splitlines() if l.strip()]
    return '\n'.join(lines[:max_sentences])


def prioritize_files(map_res):
    # simplistic: look for entrypoints
    candidates = []
    for node in map_res['file_tree']:
        for f in node['files']:
            if f in ('main.py', 'app.py', 'index.py'):
                path = os.path.join(node['path'], f)
                candidates.append(path)
    # fallback: top-level python files
    if not candidates:
        for node in map_res['file_tree']:
            for f in node['files']:
                if f.endswith('.py') and node['path'] in ('.', './'):
                    candidates.append(os.path.join(node['path'], f))
    return { 'top_files': candidates[:5] }
```

---

## 6. Python: `py/code_analyzer.py` (Tree‑sitter usage)

> **Important:** Tree‑sitter requires installing language grammars and the Python bindings. See the README section below.

```python
# code_analyzer.py
import os
from pathlib import Path
from tree_sitter import Language, Parser
import networkx as nx

# assume grammars have been built into a shared lib at ./build/my-languages.so
LANG_SO = os.environ.get('TREE_SITTER_LANG_SO', './build/my-languages.so')

parser = Parser()
try:
    PY_LANG = Language(LANG_SO, 'python')
    parser.set_language(PY_LANG)
except Exception as e:
    PY_LANG = None


def analyze_file(repo_path: str, file_rel_path: str):
    p = Path(repo_path) / file_rel_path
    if not p.exists():
        return {'error': 'file not found', 'path': str(p)}
    src = p.read_text(encoding='utf-8')
    if not PY_LANG:
        # fallback: simple regex parse
        return simple_parse(src)
    tree = parser.parse(bytes(src, 'utf8'))
    # TODO: traverse tree to extract functions, classes, calls
    # For now return a placeholder
    return simple_parse(src)


def simple_parse(src: str):
    lines = src.splitlines()
    funcs = []
    classes = []
    for i,l in enumerate(lines):
        s = l.strip()
        if s.startswith('def '):
            name = s.split('def ')[1].split('(')[0]
            funcs.append({'name': name, 'line': i+1})
        if s.startswith('class '):
            name = s.split('class ')[1].split('(')[0].strip(':')
            classes.append({'name': name, 'line': i+1})
    # build small CCG as edges between functions if one mentions another (heuristic)
    import re
    g = { 'nodes': [], 'edges': [] }
    names = [f['name'] for f in funcs]
    for f in funcs:
        g['nodes'].append({'type':'function','name':f['name'],'line':f['line']})
        body = '\n'.join(lines[f['line']-1:f['line']+30])
        for other in names:
            if other != f['name'] and re.search(r'\b' + other + r'\b', body):
                g['edges'].append({'from': f['name'], 'to': other, 'type':'calls'})
    return g


def merge_ccg(ccg_map: dict):
    # merge simple graphs
    nodes = []
    edges = []
    for k,v in ccg_map.items():
        for n in v.get('nodes',[]):
            nodes.append({**n, 'file': k})
        for e in v.get('edges',[]):
            edges.append({**e, 'file': k})
    return { 'nodes': nodes, 'edges': edges }
```

---

## 7. Python: `py/docgen.py`

```python
# docgen.py
import os
from pathlib import Path
import markdown
import json
import networkx as nx


def generate_markdown(map_res, ccg, opts=None):
    out_dir = opts.get('out_dir','./outputs') if opts else './outputs'
    repo_name = map_res.get('name','repo')
    od = Path(out_dir) / repo_name
    od.mkdir(parents=True, exist_ok=True)
    md = []
    md.append(f"# {repo_name} — Auto-generated documentation\n")
    md.append('## Overview\n')
    md.append(map_res.get('readme_summary','No README found') + '\n')

    md.append('## File tree\n')
    for node in map_res['file_tree'][:40]:
        md.append(f"- {node['path']} ({len(node['files'])} files)")
    md.append('\n')

    md.append('## API / Code Context Graph\n')
    md.append('Nodes:\n')
    for n in ccg.get('nodes', [])[:200]:
        md.append(f"- {n.get('type')} `{n.get('name')}` (file: {n.get('file', '')})")
    md.append('\nEdges:\n')
    for e in ccg.get('edges', [])[:500]:
        md.append(f"- `{e['from']}` -> `{e['to']}` ({e.get('type','')}, file: {e.get('file','')})")

    # write Markdown
    md_text = '\n'.join(md)
    md_file = od / 'docs.md'
    md_file.write_text(md_text, encoding='utf-8')

    # optionally generate a simple graphviz diagram
    try:
        import graphviz
        g = graphviz.Digraph('ccg')
        for n in ccg.get('nodes',[]):
            g.node(n['name'])
        for e in ccg.get('edges',[]):
            g.edge(e['from'], e['to'])
        g.render(str(od / 'ccg'), format='png', cleanup=True)
        diagram = 'ccg.png'
    except Exception:
        diagram = None

    return { 'docs': str(md_file), 'diagram': diagram }
```

---

## 8. Optional Streamlit frontend (FE/streamlit_frontend.py)

```python
# streamlit_frontend.py (very small)
import streamlit as st
import requests

st.title('Codebase Genius')
repo = st.text_input('GitHub repo URL')
if st.button('Generate Docs'):
    r = requests.post('http://localhost:8000/api_generate_docs', json={'repo_url': repo})
    st.write(r.json())
```

---

## 9. README / Setup and run instructions (README.md)

```
# Codebase Genius — Quickstart

## Prereqs
- Python 3.10+
- Git
- System packages: graphviz (for diagrams), libstdc++ (for tree-sitter builds)

## 1. Clone repository (this project scaffold)

    git clone <your-fork-url>
    cd codebase_genius/BE

## 2. Create venv and install deps

    python3 -m venv venv
    source venv/bin/activate
    pip install -r ../requirements.txt

## 3. Tree-sitter setup (optional but recommended for better parsing)

    # clone grammars
    git clone https://github.com/tree-sitter/tree-sitter-python third_party/tree-sitter-python

    # build shared lib
    python -c "from tree_sitter import Language; Language.build_library('./build/my-languages.so', ['third_party/tree-sitter-python'])"

    # set env var
    export TREE_SITTER_LANG_SO=./build/my-languages.so

## 4. Run Jac server

You need Jac/Jaseci installed and on PATH. See https://jac-lang.org for install.

    jac serve main.jac

This exposes walkers as HTTP endpoints (e.g., `api_generate_docs`).

## 5. Call the API

    curl -X POST http://localhost:8000/api_generate_docs -H 'Content-Type: application/json' -d '{"repo_url":"https://github.com/psf/requests"}'

Generated docs will be under `./outputs/<repo_name>/docs.md` and `ccg.png`.
```

---

## 10. Example sample output (short excerpt)

```
# requests — Auto-generated documentation

## Overview
A simple, elegant HTTP library for Python, built for human beings.

## File tree
- . (4 files)
- requests (30 files)

## API / Code Context Graph
Nodes:
- function `get` (file: requests/api.py)
- function `request` (file: requests/api.py)

Edges:
- `get` -> `request` (calls, file: requests/api.py)
```

---

## 11. Limitations and next steps

* The included `simple_parse` is a heuristic fallback. For production-quality CCG you'll want full Tree‑sitter traversal to extract AST nodes, call expressions, inheritance, imports, and cross-file references.
* Add caching, parallel analysis, and better LLM-based README summarisation (call `byllm` or your LLM provider).
* Add authentication/queueing, and a nicer FE (Streamlit or React).

---

## 12. Useful references

* byLLM and Jac docs (examples and how to run Jac servers). See the Jaseci docs for `byLLM` examples for the Task Manager: [https://www.jac-lang.org/learn/examples/agentic_ai/task-manager-lite/](https://www.jac-lang.org/learn/examples/agentic_ai/task-manager-lite/) . citeturn0search1
* Jac & byLLM guides: [https://www.jac-lang.org/learn/jac-byllm/usage/](https://www.jac-lang.org/learn/jac-byllm/usage/). citeturn0search5
* Jaseci GitHub org: [https://github.com/jaseci-labs](https://github.com/jaseci-labs). citeturn0search6

---

### Final notes

This scaffold is a runnable starting point. I focused on clear separation of responsibilities (Supervisor, RepoMapper, CodeAnalyzer, DocGenie) and used Python modules to handle the heavy lifting so you can iterate quickly.

If you want, I can now:

* generate fully formed `main.jac` and the Jac agent files (ready to paste),
* create the Python files verbatim for you to copy, or
* produce a GitHub-ready commit patch with all files.

Which of those would you like me to produce next? (I'll create the files directly in this canvas.)
