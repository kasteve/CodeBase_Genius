"""
Diagnostic script to troubleshoot CodeBase Genius setup issues
"""
import os
import sys
from pathlib import Path

print("=" * 70)
print("🔍 CodeBase Genius - Diagnostic Tool")
print("=" * 70)

# 1. Check current directory
print("\n1️⃣ Current Directory:")
print(f"   {Path.cwd()}")

# 2. Check Python version
print("\n2️⃣ Python Version:")
print(f"   {sys.version}")

# 3. Check file structure
print("\n3️⃣ File Structure:")
files_to_check = [
    'py/__init__.py',
    'py/repo_mapper.py',
    'py/code_analyzer.py',
    'py/docgen.py',
    'api.py',
    'agents/__init__.py'
]

for file in files_to_check:
    path = Path(file)
    exists = "✅" if path.exists() else "❌"
    size = f"({path.stat().st_size} bytes)" if path.exists() else ""
    print(f"   {exists} {file} {size}")

# 4. Try importing modules
print("\n4️⃣ Testing Module Imports:")

# Test direct import
print("\n   Testing direct imports from py/...")
try:
    sys.path.insert(0, str(Path.cwd() / 'py'))
    import repo_mapper
    print(f"   ✅ repo_mapper: {repo_mapper.__file__}")
except Exception as e:
    print(f"   ❌ repo_mapper: {e}")

try:
    import code_analyzer
    print(f"   ✅ code_analyzer: {code_analyzer.__file__}")
except Exception as e:
    print(f"   ❌ code_analyzer: {e}")

try:
    import docgen
    print(f"   ✅ docgen: {docgen.__file__}")
except Exception as e:
    print(f"   ❌ docgen: {e}")

# 5. Check if docgen has correct content
print("\n5️⃣ Checking docgen.py content:")
docgen_path = Path('py/docgen.py')
if docgen_path.exists():
    with open(docgen_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    has_docgenerator = 'class DocGenerator' in content
    has_generate = 'def generate(' in content
    line_count = len(content.split('\n'))
    
    print(f"   ✅ File exists: {docgen_path}")
    print(f"   {'✅' if has_docgenerator else '❌'} Has DocGenerator class")
    print(f"   {'✅' if has_generate else '❌'} Has generate() method")
    print(f"   📝 Total lines: {line_count}")
    
    if line_count < 100:
        print(f"   ⚠️  WARNING: File seems too small ({line_count} lines)")
        print(f"       Expected: 500+ lines for complete implementation")
else:
    print(f"   ❌ File not found: {docgen_path}")

# 6. Check dependencies
print("\n6️⃣ Checking Dependencies:")
dependencies = [
    'fastapi',
    'uvicorn', 
    'requests',
    'pydantic',
    'google.generativeai',
    'graphviz'
]

for dep in dependencies:
    try:
        if dep == 'google.generativeai':
            import google.generativeai
            module = google.generativeai
        else:
            module = __import__(dep)
        
        version = getattr(module, '__version__', 'unknown')
        print(f"   ✅ {dep:25} - v{version}")
    except ImportError:
        print(f"   ❌ {dep:25} - NOT INSTALLED")

# 7. Check Graphviz
print("\n7️⃣ Checking Graphviz:")
import subprocess
try:
    result = subprocess.run(['dot', '-V'], capture_output=True, text=True, timeout=5)
    if result.returncode == 0:
        print(f"   ✅ Graphviz found: {result.stderr.strip()}")
    else:
        print(f"   ❌ Graphviz command failed")
except FileNotFoundError:
    print(f"   ❌ Graphviz 'dot' command not found in PATH")
    print(f"   💡 Install from: https://graphviz.org/download/")
except Exception as e:
    print(f"   ❌ Error checking Graphviz: {e}")

# 8. Environment variables
print("\n8️⃣ Environment Variables:")
env_vars = ['GEMINI_API_KEY', 'GITHUB_TOKEN']
for var in env_vars:
    value = os.getenv(var)
    if value:
        masked = value[:8] + '...' if len(value) > 8 else '***'
        print(f"   ✅ {var}: {masked}")
    else:
        print(f"   ⚠️  {var}: Not set (optional)")

# 9. Test creating a simple DocGenerator
print("\n9️⃣ Testing DocGenerator instantiation:")
try:
    sys.path.insert(0, str(Path.cwd() / 'py'))
    import docgen
    doc_gen = docgen.DocGenerator()
    print(f"   ✅ DocGenerator created successfully")
    print(f"   ✅ AI enabled: {doc_gen.ai_enabled}")
except Exception as e:
    print(f"   ❌ Failed to create DocGenerator: {e}")
    import traceback
    traceback.print_exc()

# 10. Summary
print("\n" + "=" * 70)
print("📋 DIAGNOSTIC SUMMARY")
print("=" * 70)

print("\n💡 Quick Fixes:")
print("   1. Make sure you're in the BE/ directory")
print("   2. Run: pip install -r ../requirements.txt")
print("   3. Copy the complete docgen.py file from the artifact")
print("   4. Install Graphviz: https://graphviz.org/download/")
print("   5. Set GEMINI_API_KEY for AI features (optional)")

print("\n🚀 To start the server:")
print("   python start.py")
print("   OR")
print("   python api.py")

print("\n" + "=" * 70)