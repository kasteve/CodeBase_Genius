"""Repository Mapper Agent - Maps GitHub repository structure"""

import py.repo_mapper as repo_mapper;

walker MapRepo {
    has repo_url: str;

    can map with `root entry {
        print(f"📂 Mapping repository: {self.repo_url}");
        
        # Create Python RepoMapper instance
        mapper = repo_mapper.RepoMapper(self.repo_url);
        result = mapper.map_repository();
        
        if result['success'] {
            print(f"✅ Mapped {result['file_count']} files and {result['directory_count']} directories");
        } else {
            print(f"❌ Error mapping repository: {result.get('error', 'Unknown error')}");
        }
        
        report result;
    }
}