"""
Universal Code Analyzer - Analyzes ALL file types
Supports Python, JavaScript, TypeScript, Java, C++, Go, Rust, Ruby, and more
"""
import re
from typing import Dict, List, Optional
from pathlib import Path


class CodeAnalyzer:
    """Universal code analyzer for multiple programming languages"""
    
    # Language-specific patterns
    LANGUAGE_PATTERNS = {
        'python': {
            'extensions': ['.py'],
            'function': r'^\s*def\s+(\w+)',
            'class': r'^\s*class\s+(\w+)',
            'import': r'^\s*(?:from\s+[\w.]+\s+)?import\s+([\w.,\s]+)',
        },
        'javascript': {
            'extensions': ['.js', '.jsx', '.mjs'],
            'function': r'(?:function\s+(\w+)|const\s+(\w+)\s*=\s*(?:async\s*)?\(|(\w+)\s*:\s*(?:async\s*)?function)',
            'class': r'^\s*class\s+(\w+)',
            'import': r'^\s*import\s+.*?from\s+[\'"](.+?)[\'"]',
        },
        'typescript': {
            'extensions': ['.ts', '.tsx'],
            'function': r'(?:function\s+(\w+)|const\s+(\w+)\s*=\s*(?:async\s*)?\(|(\w+)\s*:\s*(?:async\s*)?function)',
            'class': r'^\s*(?:export\s+)?(?:abstract\s+)?class\s+(\w+)',
            'import': r'^\s*import\s+.*?from\s+[\'"](.+?)[\'"]',
            'interface': r'^\s*(?:export\s+)?interface\s+(\w+)',
        },
        'java': {
            'extensions': ['.java'],
            'function': r'^\s*(?:public|private|protected)?\s*(?:static\s+)?(?:\w+\s+)?(\w+)\s*\([^)]*\)\s*(?:throws\s+[\w,\s]+)?\s*\{',
            'class': r'^\s*(?:public\s+)?(?:abstract\s+)?class\s+(\w+)',
            'interface': r'^\s*(?:public\s+)?interface\s+(\w+)',
        },
        'csharp': {
            'extensions': ['.cs'],
            'function': r'^\s*(?:public|private|protected|internal)?\s*(?:static\s+)?(?:async\s+)?(?:\w+\s+)?(\w+)\s*\(',
            'class': r'^\s*(?:public\s+)?(?:abstract\s+)?class\s+(\w+)',
        },
        'cpp': {
            'extensions': ['.cpp', '.cc', '.cxx', '.hpp', '.h'],
            'function': r'^\s*(?:[\w:]+\s+)?(\w+)\s*\([^)]*\)\s*(?:const)?\s*\{',
            'class': r'^\s*class\s+(\w+)',
        },
        'go': {
            'extensions': ['.go'],
            'function': r'^\s*func\s+(?:\([^)]*\)\s*)?(\w+)',
            'type': r'^\s*type\s+(\w+)\s+(?:struct|interface)',
        },
        'rust': {
            'extensions': ['.rs'],
            'function': r'^\s*(?:pub\s+)?fn\s+(\w+)',
            'struct': r'^\s*(?:pub\s+)?struct\s+(\w+)',
            'trait': r'^\s*(?:pub\s+)?trait\s+(\w+)',
        },
        'ruby': {
            'extensions': ['.rb'],
            'function': r'^\s*def\s+(\w+)',
            'class': r'^\s*class\s+(\w+)',
            'module': r'^\s*module\s+(\w+)',
        },
        'php': {
            'extensions': ['.php'],
            'function': r'^\s*(?:public|private|protected)?\s*function\s+(\w+)',
            'class': r'^\s*class\s+(\w+)',
        },
        'swift': {
            'extensions': ['.swift'],
            'function': r'^\s*(?:public\s+|private\s+)?func\s+(\w+)',
            'class': r'^\s*(?:public\s+|private\s+)?class\s+(\w+)',
            'struct': r'^\s*(?:public\s+|private\s+)?struct\s+(\w+)',
        },
        'kotlin': {
            'extensions': ['.kt', '.kts'],
            'function': r'^\s*(?:fun|suspend\s+fun)\s+(\w+)',
            'class': r'^\s*(?:data\s+)?class\s+(\w+)',
        }
    }
    
    # File type categories
    MARKUP_LANGUAGES = {
        '.html', '.htm', '.xml', '.svg', '.md', '.markdown',
        '.rst', '.tex', '.adoc'
    }
    
    CONFIG_FILES = {
        '.json', '.yaml', '.yml', '.toml', '.ini', '.cfg',
        '.conf', '.properties', '.env'
    }
    
    STYLE_FILES = {
        '.css', '.scss', '.sass', '.less', '.styl'
    }
    
    def __init__(self):
        self.stats = {
            'total_files': 0,
            'files_by_type': {},
            'files_by_category': {
                'code': 0,
                'markup': 0,
                'config': 0,
                'style': 0,
                'other': 0
            }
        }
    
    def detect_language(self, filepath: str) -> Optional[str]:
        """Detect programming language from file extension"""
        ext = Path(filepath).suffix.lower()
        
        for lang, patterns in self.LANGUAGE_PATTERNS.items():
            if ext in patterns['extensions']:
                return lang
        
        return None
    
    def categorize_file(self, filepath: str) -> str:
        """Categorize file type"""
        ext = Path(filepath).suffix.lower()
        
        if self.detect_language(filepath):
            return 'code'
        elif ext in self.MARKUP_LANGUAGES:
            return 'markup'
        elif ext in self.CONFIG_FILES:
            return 'config'
        elif ext in self.STYLE_FILES:
            return 'style'
        else:
            return 'other'
    
    def analyze_file(self, content: str, filepath: str) -> Dict:
        """
        Analyze a single file's content
        Returns: Dictionary with functions, classes, and metadata
        """
        language = self.detect_language(filepath)
        category = self.categorize_file(filepath)
        
        # Update stats
        self.stats['total_files'] += 1
        self.stats['files_by_category'][category] += 1
        
        ext = Path(filepath).suffix.lower()
        self.stats['files_by_type'][ext] = self.stats['files_by_type'].get(ext, 0) + 1
        
        if not language:
            # Non-code file
            return {
                'filepath': filepath,
                'language': None,
                'category': category,
                'extension': ext,
                'lines': len(content.split('\n')),
                'size': len(content),
                'nodes': [],
                'edges': [],
                'functions': [],
                'classes': [],
                'entities': []
            }
        
        # Analyze code file
        patterns = self.LANGUAGE_PATTERNS[language]
        lines = content.split('\n')
        
        entities = []
        nodes = []
        edges = []
        functions = []
        classes = []
        
        # Extract code entities based on language patterns
        for entity_type, pattern in patterns.items():
            if entity_type == 'extensions':
                continue
                
            for i, line in enumerate(lines, 1):
                matches = re.finditer(pattern, line, re.MULTILINE)
                for match in matches:
                    # Get the captured group (name)
                    name = None
                    for group in match.groups():
                        if group:
                            name = group
                            break
                    
                    if name:
                        entity = {
                            'type': entity_type,
                            'name': name,
                            'line': i,
                            'language': language
                        }
                        entities.append(entity)
                        
                        # Add to nodes
                        nodes.append({
                            'type': entity_type,
                            'name': name,
                            'line': i
                        })
                        
                        # Track functions and classes separately
                        if entity_type in ['function', 'func', 'def']:
                            functions.append(entity)
                        elif entity_type in ['class', 'struct', 'interface', 'trait', 'type']:
                            classes.append(entity)
        
        # Build call graph (simplified)
        all_names = [e['name'] for e in entities]
        for func in functions:
            # Get function body (next 30 lines)
            start_line = func['line'] - 1
            body_lines = lines[start_line:start_line + 30]
            body = '\n'.join(body_lines)
            
            # Find references to other entities
            for other_name in all_names:
                if other_name != func['name'] and re.search(r'\b' + re.escape(other_name) + r'\b', body):
                    edges.append({
                        'from': func['name'],
                        'to': other_name,
                        'type': 'calls'
                    })
        
        return {
            'filepath': filepath,
            'language': language,
            'category': category,
            'extension': ext,
            'lines': len(lines),
            'size': len(content),
            'nodes': nodes,
            'edges': edges,
            'functions': functions,
            'classes': classes,
            'entities': entities,
            'entity_count': len(entities)
        }
    
    def analyze_repository(self, files_content: Dict[str, str]) -> Dict:
        """
        Analyze multiple files of ANY type
        Args:
            files_content: Dict mapping filepath to file content
        Returns: Aggregated analysis results
        """
        all_results = []
        
        # Reset stats
        self.stats = {
            'total_files': 0,
            'files_by_type': {},
            'files_by_category': {
                'code': 0,
                'markup': 0,
                'config': 0,
                'style': 0,
                'other': 0
            },
            'files_by_language': {}
        }
        
        for filepath, content in files_content.items():
            try:
                result = self.analyze_file(content, filepath)
                all_results.append(result)
                
                # Track language stats
                if result.get('language'):
                    lang = result['language']
                    if lang not in self.stats['files_by_language']:
                        self.stats['files_by_language'][lang] = 0
                    self.stats['files_by_language'][lang] += 1
                    
            except Exception as e:
                print(f"⚠️ Error analyzing {filepath}: {e}")
                continue
        
        # Calculate totals
        total_functions = sum(len(r.get('functions', [])) for r in all_results)
        total_classes = sum(len(r.get('classes', [])) for r in all_results)
        total_entities = sum(r.get('entity_count', 0) for r in all_results)
        
        return {
            'success': True,
            'files_analyzed': len(all_results),
            'results': all_results,
            'stats': self.stats,
            'total_functions': total_functions,
            'total_classes': total_classes,
            'total_entities': total_entities
        }


if __name__ == "__main__":
    # Test the analyzer with multiple languages
    test_files = {
        'test.py': """
def hello():
    print("Hello")
    
class MyClass:
    def method(self):
        hello()
""",
        'test.js': """
function greet(name) {
    console.log(`Hello ${name}`);
}

class User {
    constructor(name) {
        this.name = name;
    }
}
""",
        'config.json': '{"key": "value"}',
        'styles.css': 'body { margin: 0; }'
    }
    
    analyzer = CodeAnalyzer()
    result = analyzer.analyze_repository(test_files)
    print(f"Analyzed {result['files_analyzed']} files")
    print(f"Found {result['total_functions']} functions")
    print(f"Found {result['total_classes']} classes")
    print(f"Stats: {result['stats']}")