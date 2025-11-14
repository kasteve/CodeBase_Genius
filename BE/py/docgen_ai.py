"""
AI-Enhanced Documentation Generator using Gemini
Generates professional, meaningful documentation with AI assistance
"""
import os
from pathlib import Path
import json
from typing import Dict, List, Optional
import google.generativeai as genai


class AIDocGenerator:
    def __init__(self, gemini_api_key: Optional[str] = None):
        """
        Initialize with Gemini API key
        Falls back to environment variable GEMINI_API_KEY if not provided
        """
        self.api_key = gemini_api_key or os.getenv('GEMINI_API_KEY')
        if self.api_key:
            genai.configure(api_key=self.api_key)
            self.model = genai.GenerativeModel('gemini-pro')
            self.ai_enabled = True
            print("✅ AI Documentation Enhancement enabled (Gemini)")
        else:
            self.ai_enabled = False
            print("⚠️ AI Enhancement disabled - no Gemini API key provided")
    
    def generate_ai_overview(self, repo_name: str, stats: Dict, sample_code: List[Dict]) -> str:
        """Generate AI-powered repository overview"""
        if not self.ai_enabled:
            return f"Repository: {repo_name}"
        
        try:
            prompt = f"""You are a technical documentation expert. Generate a comprehensive, professional overview for this codebase:

Repository: {repo_name}
Statistics:
- Total Files: {stats.get('total_files', 0)}
- Total Directories: {stats.get('total_dirs', 0)}
- Analyzed Files: {stats.get('analyzed_files', 0)}
- Functions: {stats.get('total_functions', 0)}
- Classes: {stats.get('total_classes', 0)}

Sample code structure:
{json.dumps(sample_code[:5], indent=2)}

Generate a 2-3 paragraph overview that:
1. Describes what this codebase likely does based on file names and structure
2. Highlights the architecture and key components
3. Mentions the technology stack
4. Is written in professional, clear language

Keep it concise and insightful."""

            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            print(f"AI overview generation failed: {e}")
            return f"Repository: {repo_name}"
    
    def generate_ai_file_documentation(self, filepath: str, functions: List[Dict], 
                                       classes: List[Dict]) -> str:
        """Generate AI documentation for a specific file"""
        if not self.ai_enabled or (not functions and not classes):
            return ""
        
        try:
            prompt = f"""Generate concise documentation for this code file:

File: {filepath}

Functions:
{json.dumps(functions[:10], indent=2)}

Classes:
{json.dumps(classes[:5], indent=2)}

Write 2-3 sentences describing:
1. The main purpose of this file
2. Key functionality it provides
3. How it fits in the larger system

Be specific but concise. Use technical language."""

            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            print(f"AI file documentation failed for {filepath}: {e}")
            return ""
    
    def generate_ai_architecture_insights(self, nodes: List[Dict], edges: List[Dict]) -> str:
        """Generate architectural insights from the code graph"""
        if not self.ai_enabled or not nodes:
            return ""
        
        try:
            # Analyze relationships
            files = list(set(n.get('file', '') for n in nodes))[:10]
            func_count = sum(1 for n in nodes if n.get('type') == 'function')
            class_count = sum(1 for n in nodes if n.get('type') == 'class')
            
            prompt = f"""Analyze this codebase architecture:

Key Files: {', '.join(files)}
Total Functions: {func_count}
Total Classes: {class_count}
Relationships: {len(edges)} connections between components

Based on this structure, provide:
1. A 2-3 sentence description of the architectural patterns used
2. Key design principles evident in the code organization
3. Areas of high complexity or central components

Be specific and technical."""

            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            print(f"AI architecture insights failed: {e}")
            return ""
    
    def generate_markdown(self, map_res: Dict, ccg: Dict, opts: Optional[Dict] = None) -> Dict:
        """
        Generate AI-enhanced markdown documentation
        """
        out_dir = opts.get('out_dir', './outputs') if opts else './outputs'
        repo_name = map_res.get('name', 'repo')
        od = Path(out_dir) / repo_name
        od.mkdir(parents=True, exist_ok=True)
        
        md = []
        nodes = ccg.get('nodes', [])
        edges = ccg.get('edges', [])
        
        # Title
        md.append(f"# {repo_name}\n")
        md.append(f"*AI-Generated Technical Documentation*\n")
        md.append("---\n")
        
        # AI-Generated Overview
        md.append("## 📋 Overview\n")
        stats = {
            'total_files': map_res.get('total_files', 0),
            'total_dirs': map_res.get('total_dirs', 0),
            'analyzed_files': len(set(n.get('file', '') for n in nodes)),
            'total_functions': sum(1 for n in nodes if n.get('type') == 'function'),
            'total_classes': sum(1 for n in nodes if n.get('type') == 'class')
        }
        
        # Get sample code structure for AI
        sample_code = []
        nodes_by_file = {}
        for n in nodes[:100]:
            file = n.get('file', 'unknown')
            if file not in nodes_by_file:
                nodes_by_file[file] = {'functions': [], 'classes': []}
            if n.get('type') == 'function':
                nodes_by_file[file]['functions'].append(n.get('name'))
            elif n.get('type') == 'class':
                nodes_by_file[file]['classes'].append(n.get('name'))
        
        for file, items in list(nodes_by_file.items())[:10]:
            sample_code.append({'file': file, **items})
        
        ai_overview = self.generate_ai_overview(repo_name, stats, sample_code)
        md.append(ai_overview + "\n")
        
        # Quick Stats
        md.append("## 📊 Repository Statistics\n")
        md.append(f"| Metric | Count |")
        md.append(f"|--------|-------|")
        md.append(f"| **Total Files** | {stats['total_files']:,} |")
        md.append(f"| **Directories** | {stats['total_dirs']:,} |")
        md.append(f"| **Analyzed Files** | {stats['analyzed_files']} |")
        md.append(f"| **Functions** | {stats['total_functions']} |")
        md.append(f"| **Classes** | {stats['total_classes']} |")
        md.append(f"| **Relationships** | {len(edges)} |")
        md.append("\n")
        
        # AI Architecture Insights
        if self.ai_enabled and nodes:
            md.append("## 🏗️ Architecture Insights\n")
            arch_insights = self.generate_ai_architecture_insights(nodes, edges)
            if arch_insights:
                md.append(arch_insights + "\n")
        
        # File Structure
        md.append("## 📁 File Structure\n")
        file_tree = map_res.get('file_tree', [])
        for node in file_tree[:20]:
            path = node['path']
            files = node.get('files', [])
            md.append(f"### `{path}/` ({len(files)} files)\n")
            for f in files[:10]:
                md.append(f"- {f}")
            if len(files) > 10:
                md.append(f"- ... and {len(files) - 10} more files")
            md.append("\n")
        
        # Detailed Code Analysis with AI
        md.append("## 📚 Code Documentation\n")
        
        for file, file_data in list(nodes_by_file.items())[:15]:
            md.append(f"### 📄 `{file}`\n")
            
            # Get full node data for this file
            file_nodes = [n for n in nodes if n.get('file') == file]
            functions = [n for n in file_nodes if n.get('type') == 'function']
            classes = [n for n in file_nodes if n.get('type') == 'class']
            
            # AI-generated file description
            if self.ai_enabled and (functions or classes):
                ai_desc = self.generate_ai_file_documentation(
                    file, 
                    [{'name': f.get('name'), 'line': f.get('line')} for f in functions],
                    [{'name': c.get('name'), 'line': c.get('line')} for c in classes]
                )
                if ai_desc:
                    md.append(f"*{ai_desc}*\n")
            
            # Classes
            if classes:
                md.append("#### Classes\n")
                for cls in classes[:10]:
                    md.append(f"- **`{cls.get('name')}`** (line {cls.get('line', '?')})")
                md.append("\n")
            
            # Functions
            if functions:
                md.append("#### Functions\n")
                for func in functions[:15]:
                    md.append(f"- **`{func.get('name')}()`** (line {func.get('line', '?')})")
                md.append("\n")
            
            md.append("---\n")
        
        # Code Relationships
        if edges:
            md.append("## 🔗 Code Relationships\n")
            md.append("*Key function and class interactions*\n")
            for e in edges[:50]:
                md.append(f"- `{e['from']}` → `{e['to']}` *({e.get('type', 'relates')})*")
            if len(edges) > 50:
                md.append(f"\n*... and {len(edges) - 50} more relationships*")
            md.append("\n")
        
        # Write Markdown
        md_text = '\n'.join(md)
        md_file = od / 'docs.md'
        md_file.write_text(md_text, encoding='utf-8')
        
        # Generate diagram
        diagram = self._generate_diagram(nodes, edges, od)
        
        return {
            'success': True,
            'docs': str(md_file),
            'diagram': diagram
        }
    
    def _generate_diagram(self, nodes: List[Dict], edges: List[Dict], output_dir: Path) -> Optional[str]:
        """Generate graphviz diagram"""
        try:
            import graphviz
            g = graphviz.Digraph('ccg', comment='Code Context Graph')
            g.attr(rankdir='TB', size='14,12', dpi='300')
            g.attr('node', shape='box', style='rounded,filled', fontname='Arial')
            g.attr('edge', fontname='Arial', fontsize='10')
            
            # Group nodes by file (show top files)
            files_nodes = {}
            for n in nodes[:60]:
                file = n.get('file', 'unknown').split('/')[-1]
                if file not in files_nodes:
                    files_nodes[file] = []
                files_nodes[file].append(n)
            
            # Create subgraphs for each file
            for idx, (file, file_nodes) in enumerate(list(files_nodes.items())[:8]):
                with g.subgraph(name=f'cluster_{idx}') as sg:
                    sg.attr(label=f'📄 {file}', style='filled', color='lightgrey')
                    
                    for n in file_nodes[:8]:
                        node_type = n.get('type', 'unknown')
                        name = n.get('name', 'unknown')
                        
                        color = 'lightyellow' if node_type == 'function' else 'lightgreen'
                        icon = '⚡' if node_type == 'function' else '📦'
                        
                        sg.node(name, f'{icon} {name}', fillcolor=color)
            
            # Add edges
            node_names = {n.get('name') for n in nodes[:60]}
            for e in edges[:80]:
                if e['from'] in node_names and e['to'] in node_names:
                    edge_type = e.get('type', '')
                    g.edge(e['from'], e['to'], label=edge_type, color='gray40')
            
            g.render(str(output_dir / 'ccg'), format='png', cleanup=True)
            print(f"✅ Diagram generated successfully")
            return 'ccg.png'
        except Exception as ex:
            print(f"⚠️ Diagram generation failed: {ex}")
            return None
    
    def generate(self, analysis_results: Dict, repo_map: Dict = None, opts: Dict = None) -> Dict:
        """
        Main entry point for AI-enhanced documentation generation
        """
        if not repo_map:
            repo_map = {'name': 'repository'}
        
        # Build CCG from analysis results
        ccg = {
            'nodes': [],
            'edges': []
        }
        
        for result in analysis_results.get('results', []):
            filepath = result.get('filepath', 'unknown')
            for node in result.get('nodes', []):
                node['file'] = filepath
            for edge in result.get('edges', []):
                edge['file'] = filepath
            
            ccg['nodes'].extend(result.get('nodes', []))
            ccg['edges'].extend(result.get('edges', []))
        
        # Add stats to repo_map
        repo_map['total_files'] = repo_map.get('readme_summary', '').split('Total Files: ')[-1].split('\n')[0] if 'Total Files:' in repo_map.get('readme_summary', '') else 0
        repo_map['total_dirs'] = repo_map.get('readme_summary', '').split('Total Directories: ')[-1].split('\n')[0] if 'Total Directories:' in repo_map.get('readme_summary', '') else 0
        
        # Generate markdown
        return self.generate_markdown(repo_map, ccg, opts)


# Backward compatibility - keep old class name
class DocGenerator(AIDocGenerator):
    pass


if __name__ == "__main__":
    # Test with API key
    api_key = input("Enter Gemini API key (or press Enter to skip AI): ").strip()
    docgen = AIDocGenerator(api_key if api_key else None)
    
    test_map = {
        'name': 'test-repo',
        'readme_summary': 'Total Files: 100\nTotal Directories: 20',
        'file_tree': [{'path': 'src/', 'files': ['main.py', 'utils.py']}]
    }
    
    test_results = {
        'results': [{
            'filepath': 'src/main.py',
            'nodes': [
                {'type': 'function', 'name': 'main', 'line': 10},
                {'type': 'class', 'name': 'Application', 'line': 20}
            ],
            'edges': []
        }]
    }
    
    result = docgen.generate(test_results, test_map)
    print(result)