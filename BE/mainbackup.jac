# main.jac — Entry point for Codebase Genius

import json;

walker CodeGenius {
    has repo_url: str = "";

    can start_analysis with `root entry {
        if self.repo_url == "" {
            self.repo_url = "https://github.com/octocat/Hello-World";
        }
        print("🚀 Starting CodeGenius analysis for:", self.repo_url);
        
        # === Step 1: Map repository ===
        print("🗺 Running RepoMapper...");
        rm = RepoMapper() spawn here;
        rm.repo_url = self.repo_url;
        visit rm;

        # === Step 2: Analyze code ===
        print("🧩 Running CodeAnalyzer...");
        ca = CodeAnalyzer() spawn here;
        ca.repo_url = self.repo_url;
        visit ca;

        # === Step 3: Generate docs ===
        print("🧾 Running DocGenie...");
        dg = DocGenie() spawn here;
        dg.repo_url = self.repo_url;
        visit dg;

        # === Step 4: Complete ===
        print("✅ Documentation generation completed!");
    }
}

walker api_generate_docs {
    has repo_url: str = "";

    can generate with `root entry {
        if self.repo_url == "" {
            self.repo_url = "https://github.com/octocat/Hello-World";
        }
        
        cg = CodeGenius() spawn here;
        cg.repo_url = self.repo_url;
        visit cg;
    }
}

with entry {
    agent = CodeGenius() spawn root;
}