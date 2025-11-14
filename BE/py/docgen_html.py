"""
AI-Powered HTML Documentation Generator
Generates beautiful, interactive documentation websites with markdown-style formatting
"""
import os
from pathlib import Path
import json
from typing import Dict, List, Optional
import google.generativeai as genai
from datetime import datetime
import html


class HTMLDocGenerator:
    def __init__(self, gemini_api_key: Optional[str] = None):
        """Initialize with Gemini API key"""
        self.api_key = gemini_api_key or os.getenv('GEMINI_API_KEY')
        if self.api_key:
            genai.configure(api_key=self.api_key)
            self.model = genai.GenerativeModel('gemini-pro')
            self.ai_enabled = True
            print("✅ AI-Powered HTML Documentation enabled")
        else:
            self.ai_enabled = False
            print("⚠️ AI disabled - basic HTML will be generated")
    
    def generate_ai_overview(self, repo_name: str, stats: Dict, sample_files: List[str]) -> str:
        """Generate comprehensive overview using AI"""
        if not self.ai_enabled:
            return f"""
            <p>This repository contains <strong>{stats.get('total_files', 0)}</strong> files 
            with <strong>{stats.get('total_functions', 0)}</strong> functions and 
            <strong>{stats.get('total_classes', 0)}</strong> classes.</p>
            """
        
        try:
            prompt = f"""You are a senior technical documentation writer. Analyze this codebase and write a comprehensive, professional overview in HTML format.

Repository Name: {repo_name}
Statistics:
- Total Files: {stats.get('total_files', 0)}
- Analyzed Files: {stats.get('analyzed_files', 0)}
- Functions: {stats.get('total_functions', 0)}
- Classes: {stats.get('total_classes', 0)}

Key Files Found: {', '.join(sample_files[:15])}

Write a detailed technical overview (4-5 paragraphs) covering:

1. **Project Purpose & Domain**: What this codebase is for, what problem it solves, and its target domain
2. **Architecture Overview**: High-level architecture, design patterns, and component organization
3. **Technology Stack**: Programming languages, frameworks, and key technologies used
4. **Key Features**: Notable functionality, unique aspects, or interesting implementation details
5. **Code Quality**: Observations about code structure, modularity, and engineering practices

Format your response as HTML paragraphs using <p> tags. Use <strong> for emphasis on key terms. Be specific, technical, and insightful. Write in clear, professional English."""

            response = self.model.generate_content(prompt)
            text = response.text.strip()
            
            # Clean and format the response
            if not text.startswith('<p>'):
                paragraphs = [p.strip() for p in text.split('\n\n') if p.strip()]
                text = '\n'.join(f'<p>{html.escape(p)}</p>' for p in paragraphs)
            
            return text
        except Exception as e:
            print(f"AI overview generation failed: {e}")
            return f"""
            <p>This repository <strong>{repo_name}</strong> contains a codebase with 
            {stats.get('total_files', 0)} total files.</p>
            <p>The analysis identified {stats.get('total_functions', 0)} functions and 
            {stats.get('total_classes', 0)} classes across the analyzed files.</p>
            """
    
    def generate_ai_file_docs(self, filepath: str, functions: List[Dict], classes: List[Dict]) -> Dict[str, str]:
        """Generate detailed documentation for a file using AI"""
        if not self.ai_enabled or (not functions and not classes):
            return {
                'description': f'This file contains {len(functions)} function(s) and {len(classes)} class(es).',
                'purpose': 'Code implementation and logic',
                'key_features': [],
                'technical_details': f'{len(functions)} functions, {len(classes)} classes'
            }
        
        try:
            func_names = ', '.join(f['name'] for f in functions[:15])
            class_names = ', '.join(c['name'] for c in classes[:10])
            
            prompt = f"""Analyze this code file and provide technical documentation:

File Path: {filepath}

Contains:
- {len(functions)} Functions: {func_names}
- {len(classes)} Classes: {class_names}

Provide a JSON response with these fields:
1. "description": 2-3 sentences explaining what this file does and its role
2. "purpose": 1 clear sentence stating its primary purpose  
3. "key_features": Array of 3-5 bullet points describing important functionality
4. "technical_details": 1-2 sentences about implementation approach or patterns used

Be specific and technical. Focus on actual functionality based on function/class names.

Response format:
{{"description": "...", "purpose": "...", "key_features": ["...", "..."], "technical_details": "..."}}"""

            response = self.model.generate_content(prompt)
            text = response.text.strip()
            
            # Extract and parse JSON
            if '{' in text and '}' in text:
                json_start = text.find('{')
                json_end = text.rfind('}') + 1
                json_str = text[json_start:json_end]
                data = json.loads(json_str)
                
                # Validate required fields
                if 'description' in data and 'purpose' in data:
                    return {
                        'description': data.get('description', ''),
                        'purpose': data.get('purpose', ''),
                        'key_features': data.get('key_features', []),
                        'technical_details': data.get('technical_details', '')
                    }
            
            # Fallback
            return {
                'description': f'This file implements functionality related to {filepath.split("/")[-1]}.',
                'purpose': 'Provides core implementation logic',
                'key_features': [
                    f'Defines {len(classes)} class(es) for object-oriented design',
                    f'Implements {len(functions)} function(s) for business logic',
                    'Contributes to overall system architecture'
                ],
                'technical_details': f'Contains {len(functions) + len(classes)} code entities'
            }
        except Exception as e:
            print(f"AI file docs failed for {filepath}: {e}")
            return {
                'description': f'Code file implementing functionality in {filepath}.',
                'purpose': 'Core implementation file',
                'key_features': [],
                'technical_details': f'{len(functions)} functions, {len(classes)} classes'
            }
    
    def generate_html_template(self) -> str:
        """Generate beautiful HTML template with markdown-style formatting"""
        return """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} - Technical Documentation</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
            line-height: 1.7;
            color: #24292e;
            background: #f6f8fa;
        }}
        
        .header {{
            background: linear-gradient(135deg, #2b5876 0%, #4e4376 100%);
            color: white;
            padding: 4rem 2rem 3rem;
            box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        }}
        
        .header-content {{
            max-width: 1200px;
            margin: 0 auto;
        }}
        
        .header h1 {{
            font-size: 3rem;
            margin-bottom: 0.75rem;
            font-weight: 700;
            letter-spacing: -0.5px;
        }}
        
        .header .subtitle {{
            font-size: 1.2rem;
            opacity: 0.95;
            font-weight: 300;
        }}
        
        .nav {{
            background: white;
            padding: 1.25rem 2rem;
            box-shadow: 0 2px 8px rgba(0,0,0,0.08);
            position: sticky;
            top: 0;
            z-index: 100;
            border-bottom: 1px solid #e1e4e8;
        }}
        
        .nav-content {{
            max-width: 1200px;
            margin: 0 auto;
            display: flex;
            gap: 2.5rem;
        }}
        
        .nav a {{
            color: #2b5876;
            text-decoration: none;
            font-weight: 600;
            transition: all 0.3s;
            padding-bottom: 4px;
            border-bottom: 2px solid transparent;
        }}
        
        .nav a:hover {{
            color: #4e4376;
            border-bottom-color: #4e4376;
        }}
        
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            padding: 3rem 2rem;
        }}
        
        .card {{
            background: white;
            border-radius: 10px;
            padding: 2.5rem;
            margin-bottom: 2.5rem;
            box-shadow: 0 2px 12px rgba(0,0,0,0.06);
            border: 1px solid #e1e4e8;
        }}
        
        .section-title {{
            font-size: 2.25rem;
            color: #24292e;
            margin-bottom: 2rem;
            padding-bottom: 1rem;
            border-bottom: 3px solid #2b5876;
            font-weight: 700;
        }}
        
        .subsection-title {{
            font-size: 1.75rem;
            color: #24292e;
            margin: 2rem 0 1rem;
            font-weight: 600;
        }}
        
        .markdown-content p {{
            margin-bottom: 1.25rem;
            font-size: 1.05rem;
            line-height: 1.8;
        }}
        
        .markdown-content strong {{
            color: #2b5876;
            font-weight: 600;
        }}
        
        .stats-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
            gap: 1.75rem;
            margin: 2.5rem 0;
        }}
        
        .stat-card {{
            background: linear-gradient(135deg, #2b5876 0%, #4e4376 100%);
            color: white;
            padding: 2rem;
            border-radius: 12px;
            text-align: center;
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
            transition: transform 0.3s;
        }}
        
        .stat-card:hover {{
            transform: translateY(-4px);
        }}
        
        .stat-number {{
            font-size: 3rem;
            font-weight: bold;
            display: block;
            margin-bottom: 0.5rem;
        }}
        
        .stat-label {{
            font-size: 1rem;
            opacity: 0.95;
            font-weight: 500;
        }}
        
        .file-card {{
            background: #fafbfc;
            border-left: 5px solid #2b5876;
            padding: 2rem;
            margin-bottom: 2rem;
            border-radius: 8px;
            box-shadow: 0 1px 4px rgba(0,0,0,0.05);
        }}
        
        .file-card h3 {{
            color: #2b5876;
            font-size: 1.4rem;
            margin-bottom: 1.25rem;
            font-family: 'Courier New', Consolas, monospace;
            font-weight: 600;
        }}
        
        .file-description {{
            color: #24292e;
            margin-bottom: 1.25rem;
            font-size: 1.05rem;
            line-height: 1.7;
        }}
        
        .purpose-box {{
            background: #e8f4f8;
            padding: 1rem 1.25rem;
            border-radius: 6px;
            margin: 1rem 0;
            border-left: 4px solid #2b5876;
        }}
        
        .purpose-box strong {{
            color: #2b5876;
        }}
        
        .technical-details {{
            background: #f1f8ff;
            padding: 1rem 1.25rem;
            border-radius: 6px;
            margin: 1rem 0;
            font-style: italic;
            color: #444;
        }}
        
        .badge {{
            display: inline-block;
            padding: 0.4rem 1rem;
            background: #dfe9f3;
            color: #2b5876;
            border-radius: 20px;
            font-size: 0.9rem;
            font-weight: 600;
            margin-right: 0.75rem;
            margin-bottom: 0.75rem;
        }}
        
        .function-list, .class-list {{
            background: white;
            padding: 1.5rem;
            border-radius: 8px;
            margin-top: 1.5rem;
            border: 1px solid #e1e4e8;
        }}
        
        .function-list h4, .class-list h4 {{
            margin-bottom: 1rem;
            color: #24292e;
            font-size: 1.15rem;
        }}
        
        .function-item, .class-item {{
            padding: 0.9rem;
            border-bottom: 1px solid #f0f0f0;
            font-family: 'Courier New', Consolas, monospace;
            color: #24292e;
            font-size: 0.95rem;
        }}
        
        .function-item:last-child, .class-item:last-child {{
            border-bottom: none;
        }}
        
        .code-icon {{
            color: #2b5876;
            margin-right: 0.75rem;
            font-weight: bold;
        }}
        
        .line-number {{
            color: #999;
            font-size: 0.85rem;
            font-style: italic;
        }}
        
        .key-features {{
            background: #fff8e1;
            padding: 1.5rem;
            border-radius: 8px;
            margin: 1.5rem 0;
        }}
        
        .key-features h4 {{
            margin-bottom: 1rem;
            color: #24292e;
        }}
        
        .key-features ul {{
            margin-left: 1.75rem;
        }}
        
        .key-features li {{
            margin-bottom: 0.75rem;
            color: #24292e;
            line-height: 1.6;
        }}
        
        .diagram-container {{
            background: white;
            padding: 2.5rem;
            border-radius: 12px;
            text-align: center;
            margin: 2.5rem 0;
            border: 1px solid #e1e4e8;
        }}
        
        .diagram-container img {{
            max-width: 100%;
            height: auto;
            border-radius: 8px;
            box-shadow: 0 4px 16px rgba(0,0,0,0.12);
        }}
        
        .footer {{
            background: #24292e;
            color: white;
            text-align: center;
            padding: 3rem 2rem;
            margin-top: 5rem;
        }}
        
        .footer p {{
            margin: 0.5rem 0;
        }}
        
        @media (max-width: 768px) {{
            .header h1 {{
                font-size: 2rem;
            }}
            
            .stats-grid {{
                grid-template-columns: 1fr;
            }}
            
            .nav-content {{
                flex-direction: column;
                gap: 1rem;
            }}
        }}
    </style>
</head>
<body>
    {content}
    
    <div class="footer">
        <p><strong>📚 Generated by CodeBase Genius</strong></p>
        <p style="opacity: 0.85; margin-top: 0.75rem;">Powered by AI • Generated on {timestamp}</p>
    </div>
    
    <script>
        document.querySelectorAll('a[href^="#"]').forEach(anchor => {{
            anchor.addEventListener('click', function (e) {{
                e.preventDefault();
                const target = document.querySelector(this.getAttribute('href'));
                if (target) {{
                    target.scrollIntoView({{ behavior: 'smooth', block: 'start' }});
                }}
            }});
        }});
    </script>
</body>
</html>"""
    
    def generate(self, analysis_results: Dict, repo_map: Dict = None, opts: Dict = None) -> Dict:
        """Generate beautiful HTML documentation with markdown-style formatting"""
        if not repo_map:
            repo_map = {'name': 'repository'}
        
        out_dir = opts.get('out_dir', './outputs') if opts else './outputs'
        repo_name = repo_map.get('name', 'repository')
        od = Path(out_dir) / repo_name
        od.mkdir(parents=True, exist_ok=True)
        
        # Build CCG
        ccg = {'nodes': [], 'edges': []}
        for result in analysis_results.get('results', []):
            filepath = result.get('filepath', 'unknown')
            for node in result.get('nodes', []):
                node['file'] = filepath
            for edge in result.get('edges', []):
                edge['file'] = filepath
            ccg['nodes'].extend(result.get('nodes', []))
            ccg['edges'].extend(result.get('edges', []))
        
        nodes = ccg['nodes']
        edges = ccg['edges']
        
        # Calculate stats
        unique_files = list(set(n.get('file', '') for n in nodes))
        stats = {
            'total_files': len(unique_files),
            'total_functions': sum(1 for n in nodes if n.get('type') == 'function'),
            'total_classes': sum(1 for n in nodes if n.get('type') == 'class'),
            'total_relationships': len(edges),
            'analyzed_files': analysis_results.get('files_analyzed', 0)
        }
        
        print(f"📊 Generating docs: {stats['total_files']} files, {stats['total_functions']} functions, {stats['total_classes']} classes")
        
        # Generate AI overview
        overview_html = self.generate_ai_overview(repo_name, stats, unique_files)
        
        # Build HTML content
        content_parts = []
        
        # Header
        content_parts.append(f"""
    <div class="header">
        <div class="header-content">
            <h1>📚 {{repo_name}}</h1>
            <p class="subtitle">Comprehensive AI-Generated Technical Documentation</p>
        </div>
    </div>
    
    <div class="nav">
        <div class="nav-content">
            <a href="#overview">Overview</a>
            <a href="#statistics">Statistics</a>
            <a href="#files">Code Files</a>
            <a href="#diagram">Architecture</a>
        </div>
    </div>
    
    <div class="container">
        <!-- Overview Section -->
        <div class="card" id="overview">
            <h2 class="section-title">📋 Project Overview</h2>
            <div class="markdown-content">
                {{overview_html}}
            </div>
        </div>
        
        <!-- Statistics Section -->
        <div class="card" id="statistics">
            <h2 class="section-title">📊 Repository Statistics</h2>
            <div class="stats-grid">
                <div class="stat-card">
                    <span class="stat-number">{{stats['total_files']}}</span>
                    <span class="stat-label">Files Analyzed</span>
                </div>
                <div class="stat-card">
                    <span class="stat-number">{{stats['total_functions']}}</span>
                    <span class="stat-label">Functions</span>
                </div>
                <div class="stat-card">
                    <span class="stat-number">{{stats['total_classes']}}</span>
                    <span class="stat-label">Classes</span>
                </div>
                <div class="stat-card">
                    <span class="stat-number">{{stats['total_relationships']}}</span>
                    <span class="stat-label">Code Relationships</span>
                </div>
            </div>
        </div>
        
        <!-- Files Section -->
        <div class="card" id="files">
            <h2 class="section-title">📁 Code Files & Components</h2>
            <p style="margin-bottom: 2rem; color: #586069;">Detailed analysis of each file with AI-generated documentation</p>
        """)
        
        # Group nodes by file
        nodes_by_file = {}
        for n in nodes:
            file = n.get('file', 'unknown')
            if file not in nodes_by_file:
                nodes_by_file[file] = {'functions': [], 'classes': []}
            if n.get('type') == 'function':
                nodes_by_file[file]['functions'].append(n)
            elif n.get('type') == 'class':
                nodes_by_file[file]['classes'].append(n)
        
        # Generate file documentation with AI
        for idx, (filepath, data) in enumerate(list(nodes_by_file.items())[:25]):
            functions = data['functions']
            classes = data['classes']
            
            # Get AI documentation
            file_docs = self.generate_ai_file_docs(
                filepath,
                [{'name': f.get('name'), 'line': f.get('line')} for f in functions],
                [{'name': c.get('name'), 'line': c.get('line')} for c in classes]
            )
            
            content_parts.append(f"""
            <div class="file-card">
                <h3>📄 {{filepath}}</h3>
                
                <div class="file-description">
                    {{file_docs.get('description', '')}}
                </div>
                
                <div class="purpose-box">
                    <strong>Purpose:</strong> {{file_docs.get('purpose', '')}}
                </div>
                
                {{f'''<div class="technical-details">
                    <strong>Technical Details:</strong> {{file_docs.get('technical_details', '')}}
                </div>''' if file_docs.get('technical_details') else ''}}
                
                {{f'''<div class="key-features">
                    <h4>🔑 Key Features</h4>
                    <ul>
                        {{"".join(f"<li>{{feature}}</li>" for feature in file_docs.get('key_features', []))}}
                    </ul>
                </div>''' if file_docs.get('key_features') else ''}}
                
                <div style="margin-top: 1.5rem;">
                    <span class="badge">🔧 {{len(functions)}} Function{{'' if len(functions) == 1 else 's'}}</span>
                    <span class="badge">📦 {{len(classes)}} Class{{'es' if len(classes) != 1 else ''}}</span>
                </div>
                
                {{f'''<div class="class-list">
                    <h4>Classes</h4>
                    {{"".join(f'<div class="class-item"><span class="code-icon">📦</span>{{c.get("name")}} <span class="line-number">(line {{c.get("line", "?")}})</span></div>' for c in classes[:15])}}
                </div>''' if classes else ''}}
                
                {{f'''<div class="function-list">
                    <h4>Functions</h4>
                    {{"".join(f'<div class="function-item"><span class="code-icon">⚡</span>{{f.get("name")}}() <span class="line-number">(line {{f.get("line", "?")}})</span></div>' for f in functions[:20])}}
                </div>''' if functions else ''}}
            </div>
            """)
        
        content_parts.append("</div>")
        
        # Diagram section
        diagram_path = self._generate_diagram(nodes, edges, od)
        if diagram_path and Path(od / diagram_path).exists():
            content_parts.append(f"""
        <div class="card" id="diagram">
            <h2 class="section-title">🏗️ Code Architecture Diagram</h2>
            <p style="margin-bottom: 2rem; color: #586069;">Visual representation of code relationships and dependencies</p>
            <div class="diagram-container">
                <img src="{{diagram_path}}" alt="Code Architecture Diagram">
            </div>
        </div>
            """)
        
        content_parts.append("</div>")
        
        # Generate final HTML
        html_template = self.generate_html_template()
        full_html = html_template.format(
            title=repo_name,
            content=''.join(content_parts),
            timestamp=datetime.now().strftime("%B %d, %Y at %H:%M:%S")
        )
        
        # Save HTML
        html_file = od / 'index.html'
        html_file.write_text(full_html, encoding='utf-8')
        
        # Also save markdown for compatibility
        self._save_markdown(repo_map, ccg, stats, od)
        
        print(f"✅ Beautiful HTML documentation: {html_file}")
        
        return {
            'success': True,
            'docs': str(html_file),
            'diagram': str(od / diagram_path) if diagram_path else None
        }
    
    def _generate_diagram(self, nodes: List[Dict], edges: List[Dict], output_dir: Path) -> Optional[str]:
        """Generate architecture diagram"""
        try:
            import graphviz
            g = graphviz.Digraph('ccg', comment='Code Architecture')
            g.attr(rankdir='TB', size='16,12', dpi='300', bgcolor='transparent')
            g.attr('node', shape='box', style='rounded,filled', fontname='Arial', fontsize='11')
            g.attr('edge', fontname='Arial', fontsize='9', color='#666666')
            
            # Limit nodes for clarity
            for n in nodes[:60]:
                name = n.get('name', 'unknown')
                node_type = n.get('type', 'unknown')
                color = '#fff9c4' if node_type == 'function' else '#c8e6c9'
                g.node(name, fillcolor=color, color='#2b5876')
            
            # Add edges
            node_names = {n.get('name') for n in nodes[:60]}
            for e in edges[:100]:
                if e['from'] in node_names and e['to'] in node_names:
                    g.edge(e['from'], e['to'], label=e.get('type', ''))
            
            g.render(str(output_dir / 'ccg'), format='png', cleanup=True)
            print("✅ Architecture diagram generated")
            return 'ccg.png'
        except Exception as e:
            print(f"⚠️ Diagram generation failed: {e}")
            return None
    
    def _save_markdown(self, repo_map: Dict, ccg: Dict, stats: Dict, output_dir: Path):
        """Save markdown version for compatibility"""
        md_lines = [
            f"# {repo_map.get('name', 'Repository')}\n",
            "## Documentation\n",
            f"For the full interactive HTML documentation, open `index.html` in your browser.\n",
            f"\n## Quick Stats\n",
            f"- Files: {stats.get('total_files', 0)}",
            f"- Functions: {stats.get('total_functions', 0)}",
            f"- Classes: {stats.get('total_classes', 0)}\n"
        ]
        md_file = output_dir / 'docs.md'
        md_file.write_text('\n'.join(md_lines), encoding='utf-8')


# Backward compatibility
class DocGenerator(HTMLDocGenerator):
    pass