"""
Code Analyzer - Analyzes code structure and patterns
"""
import re
from typing import Dict, List


class CodeAnalyzer:
    def __init__(self):
        pass
    
    def analyze_file(self, content: str, filepath: str) -> Dict:
        """
        Analyze a single file's content
        Returns: Dictionary with functions, classes, and call graph
        """
        lines = content.split('\n')
        funcs = []
        classes = []
        
        # Simple pattern matching to find functions and classes
        for i, line in enumerate(lines):
            s = line.strip()
            if s.startswith('def '):
                name = s.split('def ')[1].split('(')[0]
                funcs.append({'name': name, 'line': i+1})
            if s.startswith('class '):
                name = s.split('class ')[1].split('(')[0].split(':')[0].strip()
                classes.append({'name': name, 'line': i+1})
        
        # Build naive call graph where functions that mention other function names are linked
        names = [f['name'] for f in funcs]
        nodes = []
        edges = []
        
        for f in funcs:
            nodes.append({'type': 'function', 'name': f['name'], 'line': f['line']})
            # Build a small body window to search mentions
            start = max(0, f['line']-1)
            body = '\n'.join(lines[start:start+40])
            for other in names:
                if other != f['name'] and re.search(r'\b' + re.escape(other) + r'\b', body):
                    edges.append({'from': f['name'], 'to': other, 'type': 'calls'})
        
        for c in classes:
            nodes.append({'type': 'class', 'name': c['name'], 'line': c['line']})
        
        return {
            'filepath': filepath,
            'nodes': nodes,
            'edges': edges,
            'functions': funcs,
            'classes': classes
        }
    
    def analyze_repository(self, files_content: Dict[str, str]) -> Dict:
        """
        Analyze multiple files
        Args:
            files_content: Dict mapping filepath to file content
        Returns: Aggregated analysis results
        """
        all_results = []
        
        for filepath, content in files_content.items():
            if filepath.endswith('.py'):
                result = self.analyze_file(content, filepath)
                all_results.append(result)
        
        return {
            'success': True,
            'files_analyzed': len(all_results),
            'results': all_results
        }


if __name__ == "__main__":
    # Test the analyzer
    test_code = """
def hello():
    print("Hello")
    
class MyClass:
    def method(self):
        hello()
"""
    analyzer = CodeAnalyzer()
    result = analyzer.analyze_file(test_code, "test.py")
    print(result)