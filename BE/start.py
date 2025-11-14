"""
Startup script for CodeBase Genius
Checks dependencies and starts the API server
"""
import os
import sys
from pathlib import Path

def check_environment():
    """Check if all required files and dependencies are present"""
    print("=" * 70)
    print("🚀 CodeBase Genius - Startup Check")
    print("=" * 70)
    
    issues = []
    warnings = []
    
    # Check required files
    print("\n📁 Checking required files...")
    required_files = [
        'py/repo_mapper.py',
        'py/code_analyzer.py',
        'py/docgen.py',
        'py/__init__.py',
        'api.py'
    ]
    
    for file in required_files:
        if Path(file).exists():
            print(f"   ✅ {file}")
        else:
            print(f"   ❌ {file} - MISSING!")
            issues.append(f"Missing file: {file}")
    
    # Check Python packages
    print("\n📦 Checking Python packages...")
    required_packages = [
        ('fastapi', 'FastAPI framework'),
        ('uvicorn', 'ASGI server'),
        ('requests', 'HTTP library'),
        ('pydantic', 'Data validation')
    ]
    
    for package, description in required_packages:
        try:
            __import__(package)
            print(f"   ✅ {package:20} - {description}")
        except ImportError:
            print(f"   ❌ {package:20} - NOT INSTALLED")
            issues.append(f"Missing package: {package}")
    
    # Check optional packages
    print("\n🔧 Checking optional packages...")
    optional_packages = [
        ('google.generativeai', 'AI documentation enhancement'),
        ('graphviz', 'Diagram generation'),
        ('streamlit', 'Web UI')
    ]
    
    for package, description in optional_packages:
        try:
            if package == 'google.generativeai':
                import google.generativeai as genai
            else:
                __import__(package)
            print(f"   ✅ {package:25} - {description}")
        except ImportError:
            print(f"   ⚠️  {package:25} - Not installed ({description})")
            warnings.append(f"Optional: {package}")
    
    # Check environment variables
    print("\n🔑 Checking environment variables...")
    env_vars = [
        ('GEMINI_API_KEY', 'AI enhancement', False),
        ('GITHUB_TOKEN', 'Higher API rate limits', False)
    ]
    
    for var, description, required in env_vars:
        if os.getenv(var):
            print(f"   ✅ {var:20} - Set ({description})")
        else:
            if required:
                print(f"   ❌ {var:20} - REQUIRED for {description}")
                issues.append(f"Missing env var: {var}")
            else:
                print(f"   ⚠️  {var:20} - Optional ({description})")
                warnings.append(f"Optional env: {var}")
    
    # Check Graphviz binary
    print("\n🎨 Checking Graphviz installation...")
    try:
        import subprocess
        result = subprocess.run(['dot', '-V'], capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            version = result.stderr.strip() if result.stderr else result.stdout.strip()
            print(f"   ✅ Graphviz binary found: {version}")
        else:
            print(f"   ⚠️  Graphviz found but not working properly")
            warnings.append("Graphviz binary issue")
    except FileNotFoundError:
        print(f"   ⚠️  Graphviz not found - diagram generation disabled")
        print(f"      Install: https://graphviz.org/download/")
        warnings.append("Graphviz not installed")
    except Exception as e:
        print(f"   ⚠️  Graphviz check failed: {e}")
        warnings.append("Graphviz check error")
    
    # Create required directories
    print("\n📂 Creating output directories...")
    Path('outputs').mkdir(exist_ok=True)
    print("   ✅ outputs/ directory ready")
    
    # Summary
    print("\n" + "=" * 70)
    print("Summary:")
    print("=" * 70)
    
    if issues:
        print("\n❌ CRITICAL ISSUES:")
        for issue in issues:
            print(f"   • {issue}")
        print("\n❌ Cannot start server - please fix the issues above")
        return False
    
    if warnings:
        print("\n⚠️  WARNINGS (non-critical):")
        for warning in warnings:
            print(f"   • {warning}")
    
    print("\n✅ All critical checks passed!")
    return True


def start_server():
    """Start the FastAPI server"""
    print("\n" + "=" * 70)
    print("🚀 Starting CodeBase Genius API Server")
    print("=" * 70)
    print("\n📝 Server will start at: http://localhost:8000")
    print("📚 API Documentation: http://localhost:8000/docs")
    print("💚 Health Check: http://localhost:8000/health")
    print("\n🛑 Press Ctrl+C to stop the server\n")
    print("=" * 70 + "\n")
    
    try:
        import uvicorn
        uvicorn.run("api:app", host="0.0.0.0", port=8000, reload=True)
    except KeyboardInterrupt:
        print("\n\n👋 Server stopped")
    except Exception as e:
        print(f"\n❌ Server failed to start: {e}")
        sys.exit(1)


if __name__ == "__main__":
    if check_environment():
        start_server()
    else:
        print("\n💡 Quick fix:")
        print("   pip install -r requirements.txt")
        sys.exit(1)