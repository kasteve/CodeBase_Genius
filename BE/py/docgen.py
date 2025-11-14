"""
Complete AI-Powered HTML Documentation Generator
Analyzes ALL file types and generates beautiful documentation
"""
import os
from pathlib import Path
import json
from typing import Dict, List, Optional
from datetime import datetime
import html as html_lib

# Try to import Gemini AI
try:
    import google.generativeai as genai
    GENAI_AVAILABLE = True
except ImportError:
    GENAI_AVAILABLE = False


class DocGenerator:
    """Complete documentation generator with AI capabilities"""
    
    def __init__(self, repo_url: str = "", gemini_api_key: Optional[str] = None):
        self.repo_url = repo_url
        self.owner, self.repo = self._parse_github_url(repo_url) if repo_url else ("", "")
        
        # Initialize AI
        self.api_key = gemini_api_key or os.getenv('GEMINI_API_KEY')
        if self.api_key and GENAI_AVAILABLE:
            try:
                genai.configure(api_key=self.api_key)
                self.model = genai.GenerativeModel('gemini-2.0-flash-exp')
                self.ai_enabled = True
                print("✅ AI-Powered Documentation enabled (Gemini 2.0 Flash)")
            except Exception as e:
                self.ai_enabled = False
                print(f"⚠️ AI initialization failed: {e}")
        else:
            self.ai_enabled = False
            print("⚠️ AI disabled - Basic documentation will be generated")
    
    def _parse_github_url(self, url: str) -> tuple:
        """Parse GitHub URL"""
        parts = url.rstrip('/').split('/')
        if len(parts) >= 2:
            return parts[-2], parts[-1]
        return "", ""
    
    def generate_ai_overview(self, repo_name: str, stats: Dict, file_info: Dict) -> str:
        """Generate AI-powered repository overview"""
        if not self.ai_enabled:
            return self._generate_basic_overview(repo_name, stats, file_info)
        
        try:
            # Build language summary
            lang_summary = []
            for lang, count in sorted(stats.get('files_by_language', {}).items(), 
                                     key=lambda x: x[1], reverse=True)[:5]:
                lang_summary.append(f"{lang}: {count} files")
            
            prompt = f"""You are a senior technical documentation writer. Write a comprehensive overview for this repository.

Repository: {repo_name}

Statistics:
- Total Files: {stats.get('total_files', 0):,}
- Total Directories: {stats.get('repo_total_dirs', 0):,}
- Files Analyzed: {stats.get('analyzed_files', 0)}

File Breakdown by Category:
- Code Files: {stats.get('code_files', 0)}
- Markup/Documentation: {stats.get('markup_files', 0)}
- Configuration: {stats.get('config_files', 0)}
- Stylesheets: {stats.get('style_files', 0)}

Primary Languages:
{chr(10).join(lang_summary)}

Code Analysis:
- Total Functions: {stats.get('total_functions', 0)}
- Total Classes: {stats.get('total_classes', 0)}
- Total Code Entities: {stats.get('total_entities', 0)}

Write 3-4 paragraphs covering:
1. Project purpose and what problem it solves
2. Technical architecture and key technologies
3. Code organization and structure
4. Notable features or interesting aspects

Use HTML <p> tags. Use <strong> for emphasis. Be specific and technical."""

            response = self.model.generate_content(prompt)
            text = response.text.strip()
            
            # Clean the response
            if not text.startswith('<p>'):
                # Convert to HTML paragraphs
                paragraphs = [p.strip() for p in text.split('\n\n') if p.strip()]
                text = '\n'.join(f'<p>{p}</p>' for p in paragraphs)
            
            return text
            
        except Exception as e:
            print(f"⚠️ AI overview failed: {e}")
            return self._generate_basic_overview(repo_name, stats, file_info)
    
    def _generate_basic_overview(self, repo_name: str, stats: Dict, file_info: Dict) -> str:
        """Generate basic overview without AI"""
        return f"""
        <p>The <strong>{repo_name}</strong> repository contains a total of <strong>{stats.get('total_files', 0):,}</strong> files 
        organized across <strong>{stats.get('repo_total_dirs', 0):,}</strong> directories. This comprehensive codebase demonstrates 
        a well-structured project with multiple file types and technologies.</p>
        
        <p>Our analysis examined <strong>{stats.get('analyzed_files', 0)}</strong> files across various categories: 
        <strong>{stats.get('code_files', 0)}</strong> code files, 
        <strong>{stats.get('markup_files', 0)}</strong> documentation/markup files, 
        <strong>{stats.get('config_files', 0)}</strong> configuration files, and 
        <strong>{stats.get('style_files', 0)}</strong> stylesheet files.</p>
        
        <p>The codebase contains <strong>{stats.get('total_functions', 0)}</strong> functions and 
        <strong>{stats.get('total_classes', 0)}</strong> classes across multiple programming languages, 
        indicating a robust and feature-rich implementation.</p>
        """
    
    def generate_file_documentation(self, file_result: Dict) -> str:
        """Generate documentation for a single file"""
        filepath = file_result.get('filepath', 'Unknown')
        language = file_result.get('language')
        category = file_result.get('category', 'other')
        functions = file_result.get('functions', [])
        classes = file_result.get('classes', [])
        entities = file_result.get('entities', [])
        lines = file_result.get('lines', 0)
        
        # Build description based on file type
        if language:
            desc = f"A <strong>{language}</strong> source file"
            if functions or classes:
                parts = []
                if functions:
                    parts.append(f"{len(functions)} function{'s' if len(functions) != 1 else ''}")
                if classes:
                    parts.append(f"{len(classes)} class{'es' if len(classes) != 1 else ''}")
                desc += f" containing {' and '.join(parts)}"
            desc += f" with {lines:,} lines of code."
        elif category == 'markup':
            desc = f"A markup/documentation file ({file_result.get('extension', '')}) with {lines:,} lines."
        elif category == 'config':
            desc = f"A configuration file ({file_result.get('extension', '')}) for project settings."
        elif category == 'style':
            desc = f"A stylesheet file ({file_result.get('extension', '')}) for styling."
        else:
            desc = f"A {file_result.get('extension', 'file')} file with {lines:,} lines."
        
        # Build HTML for this file
        html_parts = [f'<div class="file-card">']
        html_parts.append(f'<h3>📄 {filepath}</h3>')
        html_parts.append(f'<div class="file-description">{desc}</div>')
        
        # Add badges
        html_parts.append('<div style="margin-top: 1.5rem;">')
        if language:
            html_parts.append(f'<span class="badge">💻 {language.title()}</span>')
        html_parts.append(f'<span class="badge">📏 {lines:,} lines</span>')
        if functions:
            html_parts.append(f'<span class="badge">🔧 {len(functions)} Function{"s" if len(functions) != 1 else ""}</span>')
        if classes:
            html_parts.append(f'<span class="badge">📦 {len(classes)} Class{"es" if len(classes) != 1 else ""}</span>')
        html_parts.append('</div>')
        
        # Add classes list
        if classes:
            html_parts.append('<div class="class-list">')
            html_parts.append('<h4>Classes/Types</h4>')
            for cls in classes[:20]:
                html_parts.append(f'<div class="class-item">')
                html_parts.append(f'<span class="code-icon">📦</span>{cls["name"]} ')
                html_parts.append(f'<span class="line-number">(line {cls.get("line", "?")})</span>')
                html_parts.append('</div>')
            if len(classes) > 20:
                html_parts.append(f'<div class="class-item" style="font-style: italic;">... and {len(classes) - 20} more</div>')
            html_parts.append('</div>')
        
        # Add functions list
        if functions:
            html_parts.append('<div class="function-list">')
            html_parts.append('<h4>Functions/Methods</h4>')
            for func in functions[:30]:
                html_parts.append(f'<div class="function-item">')
                html_parts.append(f'<span class="code-icon">⚡</span>{func["name"]}() ')
                html_parts.append(f'<span class="line-number">(line {func.get("line", "?")})</span>')
                html_parts.append('</div>')
            if len(functions) > 30:
                html_parts.append(f'<div class="function-item" style="font-style: italic;">... and {len(functions) - 30} more</div>')
            html_parts.append('</div>')
        
        html_parts.append('</div>')
        return '\n'.join(html_parts)
    
    def generate(self, analysis_results: Dict, repo_map: Dict = None, opts: Dict = None) -> Dict:
        """Generate complete HTML documentation"""
        if not repo_map:
            repo_map = {'name': 'repository'}
        
        out_dir = opts.get('out_dir', './outputs') if opts else './outputs'
        repo_name = repo_map.get('name', 'repository')
        repo_url = repo_map.get('repo_url', '')
        
        od = Path(out_dir) / repo_name
        od.mkdir(parents=True, exist_ok=True)
        
        # Get analysis results
        results = analysis_results.get('results', [])
        analysis_stats = analysis_results.get('stats', {})
        
        # Calculate comprehensive stats
        total_repo_files = repo_map.get('total_files_in_repo', 0)
        total_repo_dirs = repo_map.get('total_dirs_in_repo', 0)
        
        files_by_category = analysis_stats.get('files_by_category', {})
        
        stats = {
            'total_files': total_repo_files,
            'repo_total_dirs': total_repo_dirs,
            'analyzed_files': analysis_results.get('files_analyzed', 0),
            'code_files': files_by_category.get('code', 0),
            'markup_files': files_by_category.get('markup', 0),
            'config_files': files_by_category.get('config', 0),
            'style_files': files_by_category.get('style', 0),
            'other_files': files_by_category.get('other', 0),
            'total_functions': analysis_results.get('total_functions', 0),
            'total_classes': analysis_results.get('total_classes', 0),
            'total_entities': analysis_results.get('total_entities', 0),
            'files_by_language': analysis_stats.get('files_by_language', {})
        }
        
        print(f"\n📊 Complete Repository Analysis:")
        print(f"   Total files in repository: {total_repo_files:,}")
        print(f"   Total directories: {total_repo_dirs:,}")
        print(f"   Files analyzed: {stats['analyzed_files']}")
        print(f"   - Code files: {stats['code_files']}")
        print(f"   - Markup files: {stats['markup_files']}")
        print(f"   - Config files: {stats['config_files']}")
        print(f"   - Style files: {stats['style_files']}")
        print(f"   Functions found: {stats['total_functions']}")
        print(f"   Classes found: {stats['total_classes']}")
        
        # Generate AI overview
        overview_html = self.generate_ai_overview(repo_name, stats, {})
        
        # Build HTML content
        timestamp = datetime.now().strftime("%B %d, %Y at %H:%M:%S")
        
        # Header section
        repo_link = f'<a href="{repo_url}" target="_blank" style="color: white; opacity: 0.9; text-decoration: underline;">{repo_url}</a>' if repo_url else ''
        
        html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{repo_name} - Technical Documentation</title>
    {self._get_css_styles()}
</head>
<body>
    <div class="header">
        <div class="header-content">
            <h1>📚 {repo_name}</h1>
            <p class="subtitle">Comprehensive AI-Generated Technical Documentation</p>
            {'<p style="margin-top: 0.5rem; font-size: 0.95rem; opacity: 0.85;">Repository: ' + repo_link + '</p>' if repo_url else ''}
        </div>
    </div>
    
    <div class="nav">
        <div class="nav-content">
            <a href="#overview">Overview</a>
            <a href="#statistics">Statistics</a>
            <a href="#files">Files</a>
            <a href="#languages">Languages</a>
        </div>
    </div>
    
    <div class="container">
        <!-- Overview Section -->
        <div class="card" id="overview">
            <h2 class="section-title">📋 Project Overview</h2>
            <div class="markdown-content">
                {overview_html}
            </div>
        </div>
        
        <!-- Statistics Section -->
        <div class="card" id="statistics">
            <h2 class="section-title">📊 Repository Statistics</h2>
            <p style="margin-bottom: 2rem; color: #586069;">
                Complete analysis of <strong>{total_repo_files:,}</strong> files across 
                <strong>{total_repo_dirs:,}</strong> directories.
            </p>
            <div class="stats-grid">
                <div class="stat-card">
                    <span class="stat-number">{stats['analyzed_files']}</span>
                    <span class="stat-label">Files Analyzed</span>
                </div>
                <div class="stat-card">
                    <span class="stat-number">{stats['code_files']}</span>
                    <span class="stat-label">Code Files</span>
                </div>
                <div class="stat-card">
                    <span class="stat-number">{stats['total_functions']}</span>
                    <span class="stat-label">Functions</span>
                </div>
                <div class="stat-card">
                    <span class="stat-number">{stats['total_classes']}</span>
                    <span class="stat-label">Classes/Types</span>
                </div>
            </div>
            
            <div style="margin-top: 2.5rem;">
                <h3 style="font-size: 1.3rem; margin-bottom: 1.5rem; color: #24292e;">File Categories</h3>
                <div class="stats-grid">
                    <div class="category-card" style="background: #e8f5e9;">
                        <div style="font-size: 2rem; margin-bottom: 0.5rem;">💻</div>
                        <div style="font-size: 1.5rem; font-weight: bold;">{stats['code_files']}</div>
                        <div>Code Files</div>
                    </div>
                    <div class="category-card" style="background: #e3f2fd;">
                        <div style="font-size: 2rem; margin-bottom: 0.5rem;">📝</div>
                        <div style="font-size: 1.5rem; font-weight: bold;">{stats['markup_files']}</div>
                        <div>Markup/Docs</div>
                    </div>
                    <div class="category-card" style="background: #fff3e0;">
                        <div style="font-size: 2rem; margin-bottom: 0.5rem;">⚙️</div>
                        <div style="font-size: 1.5rem; font-weight: bold;">{stats['config_files']}</div>
                        <div>Configuration</div>
                    </div>
                    <div class="category-card" style="background: #f3e5f5;">
                        <div style="font-size: 2rem; margin-bottom: 0.5rem;">🎨</div>
                        <div style="font-size: 1.5rem; font-weight: bold;">{stats['style_files']}</div>
                        <div>Stylesheets</div>
                    </div>
                </div>
            </div>
        </div>
        
        <!-- Languages Section -->
        <div class="card" id="languages">
            <h2 class="section-title">💻 Programming Languages</h2>
            <div class="language-list">
"""
        
        # Add language breakdown
        for lang, count in sorted(stats['files_by_language'].items(), key=lambda x: x[1], reverse=True):
            percentage = (count / stats['code_files'] * 100) if stats['code_files'] > 0 else 0
            html_content += f"""
                <div class="language-item">
                    <div class="language-info">
                        <span class="language-name">{lang.title()}</span>
                        <span class="language-count">{count} files ({percentage:.1f}%)</span>
                    </div>
                    <div class="language-bar">
                        <div class="language-bar-fill" style="width: {percentage}%"></div>
                    </div>
                </div>
"""
        
        html_content += """
            </div>
        </div>
        
        <!-- Files Section -->
        <div class="card" id="files">
            <h2 class="section-title">📁 Analyzed Files</h2>
            <p style="margin-bottom: 2rem; color: #586069;">
                Detailed breakdown of all analyzed files in the repository
            </p>
"""
        
        # Add file documentation
        for result in results[:100]:  # Limit to first 100 files for HTML size
            html_content += self.generate_file_documentation(result)
        
        if len(results) > 100:
            html_content += f"""
            <div style="text-align: center; padding: 2rem; background: #f6f8fa; border-radius: 8px; margin-top: 2rem;">
                <p style="font-size: 1.1rem; color: #586069;">
                    ... and <strong>{len(results) - 100}</strong> more files
                </p>
            </div>
"""
        
        html_content += """
        </div>
    </div>
    
    <div class="footer">
        <p><strong>📚 Generated by CodeBase Genius</strong></p>
        <p style="opacity: 0.85; margin-top: 0.75rem;">Powered by AI • Generated on """ + timestamp + """</p>
    </div>
    
    <script>
        document.querySelectorAll('a[href^="#"]').forEach(anchor => {
            anchor.addEventListener('click', function (e) {
                e.preventDefault();
                const target = document.querySelector(this.getAttribute('href'));
                if (target) {
                    target.scrollIntoView({ behavior: 'smooth', block: 'start' });
                }
            });
        });
    </script>
</body>
</html>"""
        
        # Save HTML
        html_file = od / 'index.html'
        html_file.write_text(html_content, encoding='utf-8')
        
        print(f"✅ Documentation generated: {html_file}")
        
        return {
            'success': True,
            'docs': str(html_file),
            'diagram': None
        }
    
    def _get_css_styles(self) -> str:
        """Get CSS styles for the HTML document"""
        return """
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Arial, sans-serif;
            line-height: 1.7;
            color: #24292e;
            background: #f6f8fa;
        }
        
        .header {
            background: linear-gradient(135deg, #2b5876 0%, #4e4376 100%);
            color: white;
            padding: 4rem 2rem 3rem;
            box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        }
        
        .header-content {
            max-width: 1200px;
            margin: 0 auto;
        }
        
        .header h1 {
            font-size: 3rem;
            margin-bottom: 0.75rem;
            font-weight: 700;
        }
        
        .header .subtitle {
            font-size: 1.2rem;
            opacity: 0.95;
        }
        
        .nav {
            background: white;
            padding: 1.25rem 2rem;
            box-shadow: 0 2px 8px rgba(0,0,0,0.08);
            position: sticky;
            top: 0;
            z-index: 100;
        }
        
        .nav-content {
            max-width: 1200px;
            margin: 0 auto;
            display: flex;
            gap: 2.5rem;
        }
        
        .nav a {
            color: #2b5876;
            text-decoration: none;
            font-weight: 600;
            transition: all 0.3s;
            padding-bottom: 4px;
            border-bottom: 2px solid transparent;
        }
        
        .nav a:hover {
            color: #4e4376;
            border-bottom-color: #4e4376;
        }
        
        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 3rem 2rem;
        }
        
        .card {
            background: white;
            border-radius: 10px;
            padding: 2.5rem;
            margin-bottom: 2.5rem;
            box-shadow: 0 2px 12px rgba(0,0,0,0.06);
            border: 1px solid #e1e4e8;
        }
        
        .section-title {
            font-size: 2.25rem;
            color: #24292e;
            margin-bottom: 2rem;
            padding-bottom: 1rem;
            border-bottom: 3px solid #2b5876;
            font-weight: 700;
        }
        
        .markdown-content p {
            margin-bottom: 1.25rem;
            font-size: 1.05rem;
            line-height: 1.8;
        }
        
        .markdown-content strong {
            color: #2b5876;
            font-weight: 600;
        }
        
        .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
            gap: 1.75rem;
            margin: 2.5rem 0;
        }
        
        .stat-card {
            background: linear-gradient(135deg, #2b5876 0%, #4e4376 100%);
            color: white;
            padding: 2rem;
            border-radius: 12px;
            text-align: center;
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
            transition: transform 0.3s;
        }
        
        .stat-card:hover {
            transform: translateY(-4px);
        }
        
        .stat-number {
            font-size: 3rem;
            font-weight: bold;
            display: block;
            margin-bottom: 0.5rem;
        }
        
        .stat-label {
            font-size: 1rem;
            opacity: 0.95;
        }
        
        .category-card {
            padding: 2rem;
            border-radius: 12px;
            text-align: center;
            box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        }
        
        .language-list {
            display: flex;
            flex-direction: column;
            gap: 1.5rem;
        }
        
        .language-item {
            padding: 1.5rem;
            background: #f6f8fa;
            border-radius: 8px;
            border-left: 4px solid #2b5876;
        }
        
        .language-info {
            display: flex;
            justify-content: space-between;
            margin-bottom: 0.75rem;
        }
        
        .language-name {
            font-weight: 600;
            color: #24292e;
            font-size: 1.1rem;
        }
        
        .language-count {
            color: #586069;
        }
        
        .language-bar {
            height: 8px;
            background: #e1e4e8;
            border-radius: 4px;
            overflow: hidden;
        }
        
        .language-bar-fill {
            height: 100%;
            background: linear-gradient(90deg, #2b5876 0%, #4e4376 100%);
            transition: width 0.5s ease;
        }
        
        .file-card {
            background: #fafbfc;
            border-left: 5px solid #2b5876;
            padding: 2rem;
            margin-bottom: 2rem;
            border-radius: 8px;
            box-shadow: 0 1px 4px rgba(0,0,0,0.05);
        }
        
        .file-card h3 {
            color: #2b5876;
            font-size: 1.4rem;
            margin-bottom: 1.25rem;
            font-family: 'Courier New', monospace;
            word-break: break-all;
        }
        
        .file-description {
            color: #24292e;
            margin-bottom: 1.25rem;
            font-size: 1.05rem;
        }
        
        .badge {
            display: inline-block;
            padding: 0.4rem 1rem;
            background: #dfe9f3;
            color: #2b5876;
            border-radius: 20px;
            font-size: 0.9rem;
            font-weight: 600;
            margin-right: 0.75rem;
            margin-bottom: 0.75rem;
        }
        
        .function-list, .class-list {
            background: white;
            padding: 1.5rem;
            border-radius: 8px;
            margin-top: 1.5rem;
            border: 1px solid #e1e4e8;
        }
        
        .function-list h4, .class-list h4 {
            margin-bottom: 1rem;
            color: #24292e;
        }
        
        .function-item, .class-item {
            padding: 0.9rem;
            border-bottom: 1px solid #f0f0f0;
            font-family: 'Courier New', monospace;
            font-size: 0.95rem;
        }
        
        .function-item:last-child, .class-item:last-child {
            border-bottom: none;
        }
        
        .code-icon {
            color: #2b5876;
            margin-right: 0.75rem;
        }
        
        .line-number {
            color: #999;
            font-size: 0.85rem;
            font-style: italic;
        }
        
        .footer {
            background: #24292e;
            color: white;
            text-align: center;
            padding: 3rem 2rem;
            margin-top: 5rem;
        }
        
        @media (max-width: 768px) {
            .header h1 { font-size: 2rem; }
            .stats-grid { grid-template-columns: 1fr; }
            .nav-content { flex-direction: column; gap: 1rem; }
        }
    </style>
"""