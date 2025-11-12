"""
FastAPI server for CodeBase Genius
Provides REST API endpoints to trigger Jac walkers
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import subprocess
import json
from typing import Optional
import os

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
    error: Optional[str] = None


@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "CodeBase Genius API",
        "version": "1.0.0"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}


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
        mapper = RepoMapper(request.repo_url)
        repo_map = mapper.map_repository()
        
        if not repo_map['success']:
            return AnalyzeResponse(
                status="error",
                message="Failed to map repository",
                repo_url=request.repo_url,
                error=repo_map.get('error', 'Unknown error')
            )
        
        # Step 2: Analyze code (placeholder for now)
        analyzer = CodeAnalyzer()
        # TODO: Fetch actual file contents and analyze
        analysis_results = {
            'success': True,
            'files_analyzed': 0,
            'results': []
        }
        
        # Step 3: Generate documentation
        docgen = DocGenerator()
        doc_result = docgen.generate(analysis_results, repo_map)
        
        return AnalyzeResponse(
            status="success",
            message="Repository analyzed successfully",
            repo_url=request.repo_url,
            file_count=repo_map.get('file_count', 0)
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )


@app.post("/api/generate-docs")
async def generate_docs(request: AnalyzeRequest):
    """
    Generate documentation for a repository
    """
    return await analyze_repository(request)


@app.get("/api/repositories")
async def list_repositories():
    """
    List recently analyzed repositories (placeholder)
    """
    return {
        "status": "success",
        "repositories": []
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("api:app", host="0.0.0.0", port=8000, reload=True)