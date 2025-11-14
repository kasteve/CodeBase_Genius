"""
Graphviz Setup Helper
Automatically detects and configures Graphviz on Windows/Linux/Mac
"""
import os
import sys
import subprocess
from pathlib import Path


def find_graphviz():
    """Find Graphviz installation on the system"""
    
    # Check if 'dot' is already in PATH
    try:
        result = subprocess.run(['dot', '-V'], capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            print("✅ Graphviz already configured in PATH")
            return True
    except (FileNotFoundError, subprocess.TimeoutExpired):
        pass
    
    # Common Windows installation paths
    windows_paths = [
        r'C:\Program Files\Graphviz\bin',
        r'C:\Program Files (x86)\Graphviz\bin',
        r'C:\Graphviz\bin',
        Path.home() / 'AppData' / 'Local' / 'Programs' / 'Graphviz' / 'bin',
    ]
    
    # Common Linux/Mac paths
    unix_paths = [
        '/usr/bin',
        '/usr/local/bin',
        '/opt/homebrew/bin',  # Mac M1/M2
        '/opt/local/bin',     # MacPorts
    ]
    
    paths_to_check = windows_paths if sys.platform == 'win32' else unix_paths
    
    for path in paths_to_check:
        path = Path(path)
        dot_exe = path / 'dot.exe' if sys.platform == 'win32' else path / 'dot'
        
        if dot_exe.exists():
            # Add to PATH
            path_str = str(path)
            if path_str not in os.environ["PATH"]:
                os.environ["PATH"] = path_str + os.pathsep + os.environ["PATH"]
                print(f"✅ Graphviz found and added to PATH: {path_str}")
            
            # Verify it works
            try:
                result = subprocess.run(['dot', '-V'], capture_output=True, text=True, timeout=5)
                if result.returncode == 0:
                    print(f"✅ Graphviz version: {result.stderr.strip()}")
                    return True
            except Exception as e:
                print(f"⚠️ Found Graphviz but verification failed: {e}")
    
    return False


def setup_graphviz():
    """Setup Graphviz for the application"""
    print("🔍 Searching for Graphviz installation...")
    
    if find_graphviz():
        return True
    
    print("\n❌ Graphviz not found!")
    print("\n📥 Please install Graphviz:")
    
    if sys.platform == 'win32':
        print("   Windows: Download from https://graphviz.org/download/")
        print("   Or use chocolatey: choco install graphviz")
    elif sys.platform == 'darwin':
        print("   Mac: brew install graphviz")
    else:
        print("   Linux: sudo apt install graphviz (Ubuntu/Debian)")
        print("          sudo yum install graphviz (RedHat/CentOS)")
    
    print("\n⚠️ Diagram generation will be disabled without Graphviz")
    return False


def check_graphviz_python():
    """Check if Python graphviz package is installed"""
    try:
        import graphviz
        print("✅ Python graphviz package installed")
        return True
    except ImportError:
        print("⚠️ Python graphviz package not installed")
        print("   Install with: pip install graphviz")
        return False


if __name__ == "__main__":
    print("=" * 60)
    print("Graphviz Setup Check")
    print("=" * 60)
    
    graphviz_binary = setup_graphviz()
    graphviz_python = check_graphviz_python()
    
    print("\n" + "=" * 60)
    print("Summary:")
    print(f"  Graphviz Binary: {'✅ OK' if graphviz_binary else '❌ NOT FOUND'}")
    print(f"  Python Package:  {'✅ OK' if graphviz_python else '❌ NOT INSTALLED'}")
    print("=" * 60)
    
    if graphviz_binary and graphviz_python:
        print("\n🎉 Graphviz is fully configured!")
    else:
        print("\n⚠️ Graphviz setup incomplete - diagram generation will be disabled")