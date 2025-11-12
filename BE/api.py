"""
FastAPI server for CodeBase Genius
Provides REST API endpoints to trigger Jac walkers
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel
import subprocess
import json
from typing import Optional, List
import os
from pathlib import Path

# Configure Graphviz PATH for Windows
# Add Graphviz to system PATH so diagram generation works
graphviz_path = r'C:\Program Files (x86)\Graphviz\bin'
if os.path.exists(graphviz_path):
    os.environ["PATH"] += os.pathsep + graphviz_path
    print(f"✅ Graphviz added to PATH: {graphviz_path}")
else:
    # Try alternative location
    graphviz_path_alt = r'C:\Program Files\Graphviz\bin'
    if os.path.exists(graphviz_path_alt):
        os.environ["PATH"] += os.pathsep + graphviz_path_alt
        print(f"✅ Graphviz added to PATH: {graphviz_path_alt}")
    else:
        print("⚠️ Warning: Graphviz not found. Diagram generation may fail.")

app = FastAPI(
    title="CodeBase Genius API",
    description="AI-powered codebase documentation generator",
    version="1.0.0"
)

# Configure CORS for frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class AnalyzeRequest(BaseModel):
    repo_url: str
    

class AnalyzeResponse(BaseModel):
    status: str
    message: str
    repo_url: str
    file_count: Optional[int] = None
    directory_count: Optional[int] = None
    documentation_path: Optional[str] = None
    diagram_path: Optional[str] = None
    error: Optional[str] = None


class FileInfo(BaseModel):
    path: str
    type: str


class RepoInfo(BaseModel):
    repo_url: str
    owner: str
    repo: str
    files: List[str]
    directories: List[str]
    file_count: int
    directory_count: int


@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "CodeBase Genius API",
        "version": "1.0.0",
        "graphviz_configured": graphviz_path in os.environ["PATH"],
        "endpoints": {
            "docs": "/docs",
            "health": "/health",
            "analyze": "/api/analyze",
            "generate_docs": "/api/generate-docs"
        }
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    # Check if Graphviz is accessible
    graphviz_available = False
    try:
        result = subprocess.run(['dot', '-V'], capture_output=True, text=True, timeout=5)
        graphviz_available = result.returncode == 0
    except Exception:
        pass
    
    return {
        "status": "healthy",
        "graphviz_available": graphviz_available
    }


@app.post("/api/analyze", response_model=AnalyzeResponse)
async def analyze_repository(request: AnalyzeRequest):
    """
    Analyze a GitHub repository and generate documentation
    
    Args:
        request: AnalyzeRequest with repo_url
        
    Returns:
        AnalyzeResponse with status and results
    """
    try:
        # Validate GitHub URL
        if not request.repo_url.startswith("https://github.com/"):
            raise HTTPException(
                status_code=400,
                detail="Invalid GitHub URL. Must start with https://github.com/"
            )
        
        # Use Jac to analyze via Python integration
        from py.repo_mapper import RepoMapper
        from py.code_analyzer import CodeAnalyzer
        from py.docgen import DocGenerator
        
        # Step 1: Map repository
        print(f"📂 Mapping repository: {request.repo_url}")
        mapper = RepoMapper(request.repo_url)
        repo_map = mapper.map_repository()
        
        if not repo_map['success']:
            return AnalyzeResponse(
                status="error",
                message="Failed to map repository",
                repo_url=request.repo_url,
                error=repo_map.get('error', 'Unknown error')
            )
        
        print(f"✅ Repository mapped: {repo_map['file_count']} files found")
        
        # Step 2: Analyze code (placeholder for now)
        print("🔍 Analyzing code structure...")
        analyzer = CodeAnalyzer()
        # TODO: Fetch actual file contents and analyze
        analysis_results = {
            'success': True,
            'files_analyzed': 0,
            'results': []
        }
        
        # Step 3: Generate documentation
        print("📝 Generating documentation...")
        docgen = DocGenerator()
        
        # Prepare repo_map for docgen
        repo_name = repo_map.get('repo', 'repository')
        doc_map = {
            'name': repo_name,
            'readme_summary': f"Repository: {repo_map.get('owner')}/{repo_name}",
            'file_tree': [
                {
                    'path': 'root',
                    'files': repo_map.get('files', [])[:100]  # Limit for performance
                }
            ]
        }
        
        doc_result = docgen.generate(analysis_results, doc_map, opts={'out_dir': './outputs'})
        
        # Verify files were actually created and construct proper paths
        docs_path = doc_result.get('docs')
        diagram_path = doc_result.get('diagram')
        
        # Convert to absolute paths and verify existence
        if docs_path:
            docs_file = Path(docs_path)
            if not docs_file.is_absolute():
                docs_file = Path('./outputs') / repo_name / docs_file.name
            
            if docs_file.exists():
                print(f"✅ Documentation generated: {docs_file}")
                docs_path = str(docs_file.absolute())
            else:
                print(f"⚠️ Documentation path returned but file not found: {docs_file}")
                docs_path = None
        
        if diagram_path:
            diagram_file = Path(diagram_path)
            if not diagram_file.is_absolute():
                # Diagram is usually in the same directory as docs
                if docs_path:
                    diagram_file = Path(docs_path).parent / diagram_file.name
                else:
                    diagram_file = Path('./outputs') / repo_name / diagram_file.name
            
            if diagram_file.exists():
                print(f"✅ Diagram generated: {diagram_file}")
                diagram_path = str(diagram_file.absolute())
            else:
                print(f"⚠️ Diagram path returned but file not found: {diagram_file}")
                diagram_path = None
        
        # Build success message
        message_parts = ["Repository analyzed"]
        if docs_path:
            message_parts.append("documentation generated")
        if diagram_path:
            message_parts.append("diagram generated")
        
        success_message = " and ".join(message_parts) + " successfully"
        
        return AnalyzeResponse(
            status="success",
            message=success_message,
            repo_url=request.repo_url,
            file_count=repo_map.get('file_count', 0),
            directory_count=repo_map.get('directory_count', 0),
            documentation_path=docs_path,
            diagram_path=diagram_path
        )
        
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )


@app.post("/api/generate-docs", response_model=AnalyzeResponse)
async def generate_docs(request: AnalyzeRequest):
    """
    Generate documentation for a repository (same as analyze)
    """
    return await analyze_repository(request)


@app.get("/api/download-docs/{repo_name}")
async def download_docs(repo_name: str):
    """
    Download generated markdown documentation
    """
    doc_path = Path(f"./outputs/{repo_name}/docs.md")
    
    if not doc_path.exists():
        raise HTTPException(
            status_code=404,
            detail=f"Documentation not found for repository: {repo_name}"
        )
    
    return FileResponse(
        path=str(doc_path),
        filename=f"{repo_name}_docs.md",
        media_type="text/markdown"
    )


@app.get("/api/repositories")
async def list_repositories():
    """
    List recently analyzed repositories
    """
    outputs_dir = Path("./outputs")
    
    if not outputs_dir.exists():
        return {
            "status": "success",
            "repositories": []
        }
    
    repos = []
    for repo_dir in outputs_dir.iterdir():
        if repo_dir.is_dir():
            doc_path = repo_dir / "docs.md"
            if doc_path.exists():
                repos.append({
                    "name": repo_dir.name,
                    "docs_path": str(doc_path),
                    "has_diagram": (repo_dir / "ccg.png").exists()
                })
    
    return {
        "status": "success",
        "repositories": repos
    }


@app.get("/api/debug/outputs")
async def debug_outputs():
    """
    Debug endpoint to see what files are actually in outputs directory
    """
    outputs_dir = Path("./outputs")
    
    if not outputs_dir.exists():
        return {
            "status": "error",
            "message": "Outputs directory does not exist",
            "path": str(outputs_dir.absolute())
        }
    
    structure = {}
    for repo_dir in outputs_dir.iterdir():
        if repo_dir.is_dir():
            files = [f.name for f in repo_dir.iterdir() if f.is_file()]
            structure[repo_dir.name] = {
                "path": str(repo_dir.absolute()),
                "files": files
            }
    
    return {
        "status": "success",
        "outputs_path": str(outputs_dir.absolute()),
        "repositories": structure
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("api:app", host="0.0.0.0", port=8000, reload=True)