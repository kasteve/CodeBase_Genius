"""
Repository Mapper - Maps the structure of a GitHub repository
"""
import os
import requests
from typing import Dict, List
from pathlib import Path


class RepoMapper:
    def __init__(self, repo_url: str):
        self.repo_url = repo_url
        self.owner, self.repo = self._parse_github_url(repo_url)
        
    def _parse_github_url(self, url: str) -> tuple:
        """Parse GitHub URL to extract owner and repo name"""
        parts = url.rstrip('/').split('/')
        if len(parts) >= 2:
            return parts[-2], parts[-1]
        return "", ""
    
    def map_repository(self) -> Dict:
        """
        Map the repository structure using GitHub API
        Returns: Dictionary with files, directories, and metadata
        """
        try:
            api_url = f"https://api.github.com/repos/{self.owner}/{self.repo}/git/trees/main?recursive=1"
            
            headers = {
                'Accept': 'application/vnd.github.v3+json',
            }
            
            # Add GitHub token if available
            github_token = os.getenv('GITHUB_TOKEN')
            if github_token:
                headers['Authorization'] = f'token {github_token}'
            
            response = requests.get(api_url, headers=headers)
            
            if response.status_code == 404:
                # Try 'master' branch if 'main' doesn't exist
                api_url = f"https://api.github.com/repos/{self.owner}/{self.repo}/git/trees/master?recursive=1"
                response = requests.get(api_url, headers=headers)
            
            if response.status_code == 200:
                data = response.json()
                tree = data.get('tree', [])
                
                files = [item['path'] for item in tree if item['type'] == 'blob']
                directories = [item['path'] for item in tree if item['type'] == 'tree']
                
                return {
                    'success': True,
                    'repo_url': self.repo_url,
                    'owner': self.owner,
                    'repo': self.repo,
                    'files': files,
                    'directories': directories,
                    'file_count': len(files),
                    'directory_count': len(directories)
                }
            else:
                return {
                    'success': False,
                    'error': f"Failed to fetch repository: {response.status_code}",
                    'files': [],
                    'directories': []
                }
                
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'files': [],
                'directories': []
            }


if __name__ == "__main__":
    # Test the mapper
    mapper = RepoMapper("https://github.com/octocat/Hello-World")
    result = mapper.map_repository()
    print(result)