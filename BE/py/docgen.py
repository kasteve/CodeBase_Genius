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
        
        # Add statistics
        nodes = ccg.get('nodes', [])
        edges = ccg.get('edges', [])
        md.append('## Code Statistics\n')
        md.append(f"- **Total Functions**: {sum(1 for n in nodes if n.get('type') == 'function')}")
        md.append(f"- **Total Classes**: {sum(1 for n in nodes if n.get('type') == 'class')}")
        md.append(f"- **Total Relationships**: {len(edges)}\n")
        
        md.append('## API / Code Context Graph\n')
        md.append('### Functions and Classes\n')
        
        # Group by file
        nodes_by_file = {}
        for n in nodes[:200]:
            file = n.get('file', 'unknown')
            if file not in nodes_by_file:
                nodes_by_file[file] = []
            nodes_by_file[file].append(n)
        
        for file, file_nodes in list(nodes_by_file.items())[:30]:
            md.append(f"\n#### 📄 `{file}`\n")
            for n in file_nodes:
                line = n.get('line', '?')
                md.append(f"- **{n.get('type')}** `{n.get('name')}` (line {line})")
        
        md.append('\n### Relationships\n')
        for e in edges[:100]:
            md.append(f"- `{e['from']}` → `{e['to']}` ({e.get('type', 'relates')})")
        
        # Write Markdown
        md_text = '\n'.join(md)
        md_file = od / 'docs.md'
        md_file.write_text(md_text, encoding='utf-8')
        
        # Generate graphviz diagram
        diagram = None
        try:
            import graphviz
            g = graphviz.Digraph('ccg', comment='Code Context Graph')
            g.attr(rankdir='TB', size='12,10')
            g.attr('node', shape='box', style='rounded,filled')
            
            # Add nodes with colors based on type
            for n in nodes[:50]:  # Limit to prevent overcrowding
                node_type = n.get('type', 'unknown')
                name = n.get('name', 'unknown')
                file = n.get('file', '').split('/')[-1]  # Just filename
                label = f"{name}\n({file})"
                
                color = 'lightblue'
                if node_type == 'class':
                    color = 'lightgreen'
                elif node_type == 'function':
                    color = 'lightyellow'
                
                g.node(name, label, fillcolor=color)
            
            # Add edges
            node_names = {n.get('name') for n in nodes[:50]}
            for e in edges[:100]:
                # Only add edge if both nodes exist in our limited set
                if e['from'] in node_names and e['to'] in node_names:
                    edge_type = e.get('type', '')
                    g.edge(e['from'], e['to'], label=edge_type)
            
            g.render(str(od / 'ccg'), format='png', cleanup=True)
            diagram = 'ccg.png'
            print(f"✅ Diagram generated successfully")
        except ImportError:
            print(f"⚠️ Warning: graphviz module not installed. Run: pip install graphviz")
            diagram = None
        except Exception as ex:
            print(f"⚠️ Warning: Could not generate diagram: {ex}")
            import traceback
            traceback.print_exc()
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
            # Add file info to each node
            filepath = result.get('filepath', 'unknown')
            for node in result.get('nodes', []):
                node['file'] = filepath
            for edge in result.get('edges', []):
                edge['file'] = filepath
            
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
            {'type': 'function', 'name': 'main', 'file': 'main.py', 'line': 1},
            {'type': 'function', 'name': 'helper', 'file': 'utils.py', 'line': 5}
        ],
        'edges': [
            {'from': 'main', 'to': 'helper', 'type': 'calls', 'file': 'main.py'}
        ]
    }
    result = docgen.generate_markdown(test_map, test_ccg)
    print(result)