"""
Auto-fix script for common CodeBase Genius issues
"""
import os
import sys
from pathlib import Path

def fix_init_files():
    """Ensure all __init__.py files exist and are correct"""
    print("\n🔧 Fixing __init__.py files...")
    
    # py/__init__.py
    py_init = Path('py/__init__.py')
    py_init_content = '''"""Python implementations for CodeBase Genius agents"""

# Import only what exists
try:
    from .repo_mapper import RepoMapper
except ImportError:
    RepoMapper = None

try:
    from .code_analyzer import CodeAnalyzer
except ImportError:
    CodeAnalyzer = None

try:
    from .docgen import DocGenerator
except ImportError:
    DocGenerator = None

# Export what's available
__all__ = []
if RepoMapper:
    __all__.append('RepoMapper')
if CodeAnalyzer:
    __all__.append('CodeAnalyzer')
if DocGenerator:
    __all__.append('DocGenerator')
'''
    
    py_init.parent.mkdir(exist_ok=True)
    py_init.write_text(py_init_content, encoding='utf-8')
    print(f"   ✅ Created/updated: {py_init}")
    
    # agents/__init__.py
    agents_init = Path('agents/__init__.py')
    agents_init.parent.mkdir(exist_ok=True)
    agents_init.write_text('"""Agents module for CodeBase Genius"""', encoding='utf-8')
    print(f"   ✅ Created/updated: {agents_init}")


def check_docgen():
    """Check if docgen.py exists and has correct structure"""
    print("\n🔍 Checking docgen.py...")
    
    docgen_path = Path('py/docgen.py')
    
    if not docgen_path.exists():
        print(f"   ❌ docgen.py not found!")
        print(f"   📝 You need to create this file from the artifact")
        print(f"   💡 Copy the complete content from 'py/docgen.py - Complete HTML Generator'")
        return False
    
    content = docgen_path.read_text(encoding='utf-8')
    lines = len(content.split('\n'))
    
    has_class = 'class DocGenerator' in content
    has_generate = 'def generate(' in content
    has_ai_overview = 'generate_ai_overview' in content
    
    print(f"   📄 File exists: {docgen_path}")
    print(f"   📏 Lines: {lines}")
    print(f"   {'✅' if has_class else '❌'} Has DocGenerator class")
    print(f"   {'✅' if has_generate else '❌'} Has generate() method")
    print(f"   {'✅' if has_ai_overview else '❌'} Has AI features")
    
    if lines < 100:
        print(f"\n   ⚠️  WARNING: File too small ({lines} lines)")
        print(f"   Expected: 500+ lines for complete implementation")
        print(f"   💡 The file might be incomplete - please copy the full version")
        return False
    
    return True


def create_outputs_dir():
    """Create outputs directory"""
    print("\n📂 Creating directories...")
    Path('outputs').mkdir(exist_ok=True)
    print("   ✅ outputs/ directory ready")


def test_imports():
    """Test if modules can be imported"""
    print("\n🧪 Testing imports...")
    
    sys.path.insert(0, str(Path.cwd() / 'py'))
    
    modules = ['repo_mapper', 'code_analyzer', 'docgen']
    success = True
    
    for module_name in modules:
        try:
            module = __import__(module_name)
            print(f"   ✅ {module_name}: OK")
        except Exception as e:
            print(f"   ❌ {module_name}: {e}")
            success = False
    
    return success


def check_dependencies():
    """Check required Python packages"""
    print("\n📦 Checking dependencies...")
    
    required = [
        'fastapi',
        'uvicorn',
        'requests',
        'pydantic'
    ]
    
    optional = [
        'google.generativeai',
        'graphviz',
        'streamlit'
    ]
    
    missing = []
    
    for package in required:
        try:
            __import__(package)
            print(f"   ✅ {package}")
        except ImportError:
            print(f"   ❌ {package} - REQUIRED")
            missing.append(package)
    
    for package in optional:
        try:
            if package == 'google.generativeai':
                import google.generativeai
            else:
                __import__(package)
            print(f"   ✅ {package} (optional)")
        except ImportError:
            print(f"   ⚠️  {package} (optional)")
    
    if missing:
        print(f"\n   💡 Install missing packages:")
        print(f"      pip install {' '.join(missing)}")
        return False
    
    return True


def main():
    """Run all fixes"""
    print("=" * 70)
    print("🔧 CodeBase Genius Auto-Fix")
    print("=" * 70)
    
    # Check we're in the right directory
    if not Path('api.py').exists():
        print("\n❌ ERROR: Please run this from the BE/ directory")
        print("   cd BE")
        print("   python autofix.py")
        sys.exit(1)
    
    # Run fixes
    fix_init_files()
    create_outputs_dir()
    
    docgen_ok = check_docgen()
    deps_ok = check_dependencies()
    imports_ok = test_imports()
    
    # Summary
    print("\n" + "=" * 70)
    print("📋 SUMMARY")
    print("=" * 70)
    
    issues = []
    
    if not docgen_ok:
        issues.append("docgen.py needs to be created/updated")
    if not deps_ok:
        issues.append("Missing required dependencies")
    if not imports_ok:
        issues.append("Module import errors")
    
    if not issues:
        print("\n✅ ALL CHECKS PASSED!")
        print("\n🚀 You can now start the server:")
        print("   python start.py")
        print("   OR")
        print("   python api.py")
    else:
        print("\n⚠️  ISSUES FOUND:")
        for issue in issues:
            print(f"   • {issue}")
        
        print("\n💡 NEXT STEPS:")
        if not docgen_ok:
            print("\n   1. Copy the complete docgen.py from the artifact")
            print("      - Look for 'py/docgen.py - Complete HTML Generator'")
            print("      - Should be 500-600 lines long")
            print("      - Save to: BE/py/docgen.py")
        
        if not deps_ok:
            print("\n   2. Install dependencies:")
            print("      pip install -r ../requirements.txt")
        
        print("\n   3. Run this script again:")
        print("      python autofix.py")
    
    print("\n" + "=" * 70)


if __name__ == "__main__":
    main()