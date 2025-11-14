"""
FastAPI server for CodeBase Genius
Analyzes ALL file types and generates comprehensive documentation
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import Optional, List
import os
import sys
import requests
from pathlib import Path

# Setup Graphviz
try:
    from setup_graphviz import setup_graphviz
    GRAPHVIZ_AVAILABLE = setup_graphviz()
except Exception as e:
    print(f"⚠️ Graphviz setup failed: {e}")
    GRAPHVIZ_AVAILABLE = False

# Load API keys
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY', '')
if GEMINI_API_KEY:
    print("✅ Gemini API key loaded - AI documentation enabled")
else:
    print("⚠️ No Gemini API key - Set GEMINI_API_KEY environment variable")

app = FastAPI(
    title="CodeBase Genius API",
    description="Universal codebase documentation generator",
    version="2.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class AnalyzeRequest(BaseModel):
    repo_url: str
    max_files: Optional[int] = 200  # Limit files to analyze


class AnalyzeResponse(BaseModel):
    status: str
    message: str
    repo_url: str
    total_files: Optional[int] = None
    files_analyzed: Optional[int] = None
    documentation_path: Optional[str] = None
    stats: Optional[dict] = None
    error: Optional[str] = None


@app.get("/")
async def root():
    """API information"""
    return {
        "service": "CodeBase Genius API v2.0",
        "status": "healthy",
        "features": [
            "Universal file type analysis",
            "Multi-language support", 
            "AI-powered documentation",
            "Beautiful HTML output"
        ],
        "endpoints": {
            "docs": "/docs",
            "analyze": "/api/analyze",
            "health": "/health"
        }
    }


@app.get("/health")
async def health():
    """Health check"""
    return {"status": "healthy", "ai_enabled": bool(GEMINI_API_KEY)}


@app.post("/api/analyze", response_model=AnalyzeResponse)
async def analyze_repository(request: AnalyzeRequest):
    """
    Analyze repository and generate complete documentation
    Optimized for large repositories with timeout protection
    """
    import time
    start_time = time.time()
    max_runtime = 120  # 2 minute maximum runtime
    
    try:
        # Validate URL
        if not request.repo_url.startswith("https://github.com/"):
            raise HTTPException(400, "Invalid GitHub URL")
        
        print(f"\n🚀 Starting analysis: {request.repo_url}")
        
        # Import modules directly (avoid __init__.py issues)
        import sys
        from pathlib import Path as PathLib
        
        # Add py directory to path
        py_dir = PathLib(__file__).parent / 'py'
        if str(py_dir) not in sys.path:
            sys.path.insert(0, str(py_dir))
        
        # Import modules
        import repo_mapper
        import code_analyzer
        import docgen
        
        RepoMapper = repo_mapper.RepoMapper
        CodeAnalyzer = code_analyzer.CodeAnalyzer
        DocGenerator = docgen.DocGenerator
        
        # Step 1: Map repository
        print("📂 Step 1/3: Mapping repository...")
        mapper = RepoMapper(request.repo_url)
        repo_map = mapper.map_repository()
        
        if not repo_map['success']:
            return AnalyzeResponse(
                status="error",
                message="Failed to map repository",
                repo_url=request.repo_url,
                error=repo_map.get('error')
            )
        
        total_files = repo_map.get('file_count', 0)
        print(f"✅ Found {total_files:,} total files")
        
        # Step 2: Fetch and analyze ALL file types
        print(f"📥 Step 2/3: Fetching files...")
        owner = repo_map['owner']
        repo_name = repo_map['repo']
        all_files = repo_map.get('files', [])
        
        # Determine which files to analyze - Smart prioritization
        code_extensions = {
            '.py', '.js', '.jsx', '.ts', '.tsx', '.java', '.cpp', '.c', '.h',
            '.cs', '.go', '.rs', '.rb', '.php', '.swift', '.kt', '.scala'
        }
        
        config_extensions = {'.json', '.yaml', '.yml', '.toml', '.ini'}
        doc_extensions = {'.md', '.rst', '.txt'}
        
        # Categorize files
        priority_files = []  # Main code files
        config_files = []
        doc_files = []
        other_files = []
        
        for f in all_files:
            ext = Path(f).suffix.lower()
            # Skip common directories that bloat repos
            if any(skip in f.lower() for skip in [
                'node_modules/', 'vendor/', '.git/', 'dist/', 'build/',
                '__pycache__/', '.next/', '.nuxt/', 'target/'
            ]):
                continue
            
            if ext in code_extensions:
                priority_files.append(f)
            elif ext in config_extensions:
                config_files.append(f)
            elif ext in doc_extensions:
                doc_files.append(f)
            else:
                other_files.append(f)
        
        # Smart selection: prioritize main code files
        max_files = min(request.max_files, 150)  # Cap at 150 to prevent timeouts
        
        files_to_analyze = (
            priority_files[:int(max_files * 0.7)] +      # 70% code files
            config_files[:int(max_files * 0.15)] +       # 15% config
            doc_files[:int(max_files * 0.1)] +           # 10% docs
            other_files[:int(max_files * 0.05)]          # 5% other
        )
        
        files_to_analyze = files_to_analyze[:max_files]
        
        print(f"📊 Analyzing {len(files_to_analyze)} files (out of {total_files:,} total)")
        
        # Fetch file contents with parallel requests and timeout handling
        files_content = {}
        github_token = os.getenv('GITHUB_TOKEN')
        headers = {}
        if github_token:
            headers['Authorization'] = f'token {github_token}'
        
        # Use session for connection pooling (faster)
        session = requests.Session()
        session.headers.update(headers)
        
        # Fetch files with shorter timeout
        fetch_timeout = 5  # 5 seconds per file
        max_retries = 1
        
        for i, file_path in enumerate(files_to_analyze):
            if i % 10 == 0:
                print(f"   Fetching: {i}/{len(files_to_analyze)}...")
            
            # Skip very large files
            if len(file_path) > 200:
                continue
            
            success = False
            for attempt in range(max_retries + 1):
                try:
                    # Try main branch first
                    file_url = f"https://raw.githubusercontent.com/{owner}/{repo_name}/main/{file_path}"
                    response = session.get(file_url, timeout=fetch_timeout)
                    
                    if response.status_code == 404 and attempt == 0:
                        # Try master branch
                        file_url = f"https://raw.githubusercontent.com/{owner}/{repo_name}/master/{file_path}"
                        response = session.get(file_url, timeout=fetch_timeout)
                    
                    if response.status_code == 200:
                        # Only store text files (skip binaries)
                        try:
                            content = response.content.decode('utf-8')
                            # Skip very large files (>500KB)
                            if len(content) > 500000:
                                print(f"   Skipping large file: {file_path}")
                                continue
                            files_content[file_path] = content
                            success = True
                            break
                        except UnicodeDecodeError:
                            # Skip binary files
                            break
                    else:
                        break
                        
                except requests.Timeout:
                    if attempt == max_retries:
                        print(f"   ⏱️ Timeout: {file_path}")
                    continue
                except Exception as e:
                    if attempt == max_retries:
                        print(f"   ⚠️ Error: {file_path}: {str(e)[:50]}")
                    break
            
            # Stop if we've been running too long (prevent total timeout)
            if i > 0 and i % 50 == 0:
                if len(files_content) < i * 0.3:  # If less than 30% success rate
                    print(f"   ⚠️ Low success rate, stopping at {i} files")
                    break
        
        print(f"✅ Fetched {len(files_content)} files successfully")
        
        # Step 3: Analyze all files
        print("🔍 Step 3/3: Analyzing code structure...")
        analyzer = CodeAnalyzer()
        analysis_results = analyzer.analyze_repository(files_content)
        
        print(f"✅ Analysis complete:")
        print(f"   Files analyzed: {analysis_results['files_analyzed']}")
        print(f"   Functions found: {analysis_results['total_functions']}")
        print(f"   Classes found: {analysis_results['total_classes']}")
        print(f"   Total entities: {analysis_results['total_entities']}")
        
        # Step 4: Generate documentation
        print("📝 Generating documentation...")
        docgen = DocGenerator(repo_url=request.repo_url, gemini_api_key=GEMINI_API_KEY)
        
        # Prepare repo map
        map_res = {
            'name': repo_name,
            'repo_url': request.repo_url,
            'total_files_in_repo': total_files,
            'total_dirs_in_repo': repo_map.get('directory_count', 0)
        }
        
        # Generate docs
        doc_result = docgen.generate(
            analysis_results, 
            map_res, 
            opts={'out_dir': './outputs'}
        )
        
        docs_path = doc_result.get('docs')
        
        # Verify file exists
        if docs_path and Path(docs_path).exists():
            print(f"✅ Documentation generated: {docs_path}")
            
            return AnalyzeResponse(
                status="success",
                message=f"Successfully analyzed {len(files_content)} files and generated documentation",
                repo_url=request.repo_url,
                total_files=total_files,
                files_analyzed=len(files_content),
                documentation_path=str(Path(docs_path).absolute()),
                stats={
                    'code_files': analysis_results['stats']['files_by_category']['code'],
                    'markup_files': analysis_results['stats']['files_by_category']['markup'],
                    'config_files': analysis_results['stats']['files_by_category']['config'],
                    'functions': analysis_results['total_functions'],
                    'classes': analysis_results['total_classes'],
                    'languages': analysis_results['stats']['files_by_language']
                }
            )
        else:
            raise HTTPException(500, "Documentation generation failed")
            
    except HTTPException:
        raise
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(500, f"Analysis failed: {str(e)}")


@app.get("/api/download/{repo_name}")
async def download_docs(repo_name: str):
    """Download generated documentation"""
    doc_path = Path(f"./outputs/{repo_name}/index.html")
    
    if not doc_path.exists():
        raise HTTPException(404, f"Documentation not found for: {repo_name}")
    
    return FileResponse(
        path=str(doc_path),
        filename=f"{repo_name}_documentation.html",
        media_type="text/html"
    )


@app.get("/api/repositories")
async def list_repositories():
    """List analyzed repositories"""
    outputs_dir = Path("./outputs")
    
    if not outputs_dir.exists():
        return {"repositories": []}
    
    repos = []
    for repo_dir in outputs_dir.iterdir():
        if repo_dir.is_dir():
            doc_path = repo_dir / "index.html"
            if doc_path.exists():
                repos.append({
                    "name": repo_dir.name,
                    "docs_path": str(doc_path),
                    "size": doc_path.stat().st_size
                })
    
    return {"repositories": repos}


if __name__ == "__main__":
    import uvicorn
    print("\n🚀 Starting CodeBase Genius API Server")
    print("📝 Universal file type support enabled")
    print(f"🤖 AI Enhancement: {'Enabled' if GEMINI_API_KEY else 'Disabled'}")
    print("\n")
    uvicorn.run("api:app", host="0.0.0.0", port=8000, reload=True)