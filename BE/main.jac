# main.jac — Entry point for Codebase Genius

import from agents { supervisor, repo_mapper, code_analyzer, docgenie }

# Main walker
walker CodeGenius {
    has repo_url: str = "";

    can start_analysis with `root entry {
        if self.repo_url == "" {
            self.repo_url = "https://github.com/octocat/Hello-World";
        }
        print("🚀 Starting CodeGenius analysis for:", self.repo_url);
        
        # Spawn the supervisor to orchestrate the analysis
        sup = supervisor.Supervisor(repo_url=self.repo_url);
        root spawn sup;
        
        print("✅ Analysis pipeline completed!");
    }
}

# API walker for FastAPI/Streamlit integration
walker api_generate_docs {
    has repo_url: str = "";

    can generate with `root entry {
        if self.repo_url == "" {
            return {"error": "Repository URL is required"};
        }
        
        print(f"API: Starting documentation generation for {self.repo_url}");
        
        cg = CodeGenius(repo_url=self.repo_url);
        root spawn cg;
        
        return {
            "status": "success",
            "message": "Documentation generation completed",
            "repo_url": self.repo_url
        };
    }
}

# Entry point
with entry {
    root spawn CodeGenius();
}