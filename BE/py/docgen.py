"""
Documentation Generator - Generates documentation from analyzed code
"""
import os
from pathlib import Path
import json
from typing import Dict, List, Optional


class DocGenerator:
    def __init__(self):
        pass
    
    def generate_markdown(self, map_res: Dict, ccg: Dict, opts: Optional[Dict] = None) -> Dict:
        """
        Generate markdown documentation from repository map and code context graph
        
        Args:
            map_res: Repository mapping results
            ccg: Code Context Graph with nodes and edges
            opts: Options dict with 'out_dir' key
            
        Returns:
            Dict with paths to generated docs and diagram
        """
        out_dir = opts.get('out_dir', './outputs') if opts else './outputs'
        repo_name = map_res.get('name', 'repo')
        od = Path(out_dir) / repo_name
        od.mkdir(parents=True, exist_ok=True)
        
        md = []
        md.append(f"# {repo_name} — Auto-generated documentation\n")
        md.append('## Overview\n')
        md.append(map_res.get('readme_summary', 'No README found') + '\n')
        
        md.append('## File tree\n')
        file_tree = map_res.get('file_tree', [])
        for node in file_tree[:40]:
            md.append(f"- {node['path']} ({len(node.get('files', []))} files)")
        md.append('\n')
        
        md.append('## API / Code Context Graph\n')
        md.append('Nodes:\n')
        for n in ccg.get('nodes', [])[:200]:
            md.append(f"- {n.get('type')} `{n.get('name')}` (file: {n.get('file', '')})")
        md.append('\nEdges:\n')
        for e in ccg.get('edges', [])[:500]:
            md.append(f"- `{e['from']}` -> `{e['to']}` ({e.get('type', '')}, file: {e.get('file', '')})")
        
        # Write Markdown
        md_text = '\n'.join(md)
        md_file = od / 'docs.md'
        md_file.write_text(md_text, encoding='utf-8')
        
        # Optionally generate a simple graphviz diagram
        diagram = None
        try:
            import graphviz
            g = graphviz.Digraph('ccg')
            for n in ccg.get('nodes', []):
                g.node(n['name'])
            for e in ccg.get('edges', []):
                g.edge(e['from'], e['to'])
            g.render(str(od / 'ccg'), format='png', cleanup=True)
            diagram = 'ccg.png'
        except Exception as ex:
            print(f"Warning: Could not generate diagram: {ex}")
            diagram = None
        
        return {
            'success': True,
            'docs': str(md_file),
            'diagram': diagram
        }
    
    def generate(self, analysis_results: Dict, repo_map: Dict = None, opts: Dict = None) -> Dict:
        """
        Main entry point for documentation generation
        """
        if not repo_map:
            repo_map = {'name': 'repository'}
        
        # Build CCG from analysis results
        ccg = {
            'nodes': [],
            'edges': []
        }
        
        for result in analysis_results.get('results', []):
            ccg['nodes'].extend(result.get('nodes', []))
            ccg['edges'].extend(result.get('edges', []))
        
        # Generate markdown
        return self.generate_markdown(repo_map, ccg, opts)


if __name__ == "__main__":
    # Test the doc generator
    docgen = DocGenerator()
    test_map = {
        'name': 'test-repo',
        'readme_summary': 'A test repository',
        'file_tree': [{'path': 'src/', 'files': ['main.py', 'utils.py']}]
    }
    test_ccg = {
        'nodes': [
            {'type': 'function', 'name': 'main', 'file': 'main.py'},
            {'type': 'function', 'name': 'helper', 'file': 'utils.py'}
        ],
        'edges': [
            {'from': 'main', 'to': 'helper', 'type': 'calls', 'file': 'main.py'}
        ]
    }
    result = docgen.generate_markdown(test_map, test_ccg)
    print(result)