"""Supervisor Agent - Orchestrates the analysis pipeline"""

import py.repo_mapper as repo_mapper;

walker Supervisor {
    has repo_url: str;

    can orchestrate with `root entry {
        print(f"🎯 Supervisor starting analysis for: {self.repo_url}");
        
        # Step 1: Map the repository
        print("Step 1: Mapping repository structure...");
        mapper = repo_mapper.RepoMapper(self.repo_url);
        repo_map = mapper.map_repository();
        
        if repo_map['success'] {
            print(f"✅ Repository mapped: {repo_map['file_count']} files found");
            print("✅ Pipeline completed successfully!");
        } else {
            print(f"❌ Failed to map repository: {repo_map.get('error', 'Unknown error')}");
        }
    }
}