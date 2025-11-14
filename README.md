# 🧠 CodeBase Genius

**AI-powered multi-agent system for automatic codebase documentation generation**

CodeBase Genius is an intelligent documentation generator that analyzes GitHub repositories and produces comprehensive, beautiful HTML documentation with AI-enhanced insights.

---

## ✨ Features

- 🌍 **Universal Language Support** - Python, JavaScript, TypeScript, Java, C++, Go, Rust, Ruby, PHP, Swift, Kotlin, and more
- 🤖 **AI-Powered Insights** - Uses Google Gemini 2.0 for intelligent overview generation
- 🎨 **Beautiful HTML Output** - Modern, responsive documentation websites
- 📊 **Comprehensive Analysis** - Functions, classes, file structure, and code relationships
- 🚀 **Fast & Efficient** - Smart file prioritization and parallel processing
- 🔌 **REST API** - Easy integration with FastAPI backend
- 🎯 **Multi-Agent Architecture** - Supervisor, RepoMapper, CodeAnalyzer, and DocGenie agents

---

## 📁 Project Structure

```
codebase_genius/
├── BE/                          # Backend
│   ├── main.jac                # Jaclang entry point
│   ├── api.py                  # FastAPI server
│   ├── agents/                 # Jac agents
│   │   ├── __init__.py
│   │   ├── supervisor.jac      # Orchestrates pipeline
│   │   ├── repo_mapper.jac     # Maps repository structure
│   │   ├── code_analyzer.jac   # Analyzes code patterns
│   │   └── docgenie.jac        # Generates documentation
│   └── py/                     # Python implementations
│       ├── __init__.py
│       ├── repo_mapper.py      # GitHub API integration
│       ├── code_analyzer.py    # Universal code analyzer
│       └── docgen.py           # HTML documentation generator
├── FE/                         # Frontend (optional)
│   └── streamlit_frontend.py   # Streamlit web interface
├── outputs/                    # Generated documentation
├── requirements.txt
└── README.md
```

---

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- Git
- Graphviz (optional, for diagrams)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/codebase-genius.git
   cd codebase-genius
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   
   # Windows
   venv\Scripts\activate
   
   # Linux/Mac
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Create required files**
   ```bash
   cd BE
   
   # Create __init__.py files
   touch py/__init__.py
   touch agents/__init__.py
   
   # Create docgen.py (run the helper script)
   python create_docgen.py
   ```

5. **Set environment variables (optional)**
   ```bash
   # For AI-enhanced documentation
   export GEMINI_API_KEY=your_gemini_api_key
   
   # For higher GitHub API limits
   export GITHUB_TOKEN=your_github_token
   ```

### Running the Server

```bash
cd BE

# Option 1: Using the smart startup script (recommended)
python start.py

# Option 2: Direct API server
python api.py

# Option 3: Using Jaclang
jac run main.jac
```

The API server will start at `http://localhost:8000`

- **API Documentation**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health

---

## 📚 Usage

### API Endpoint

**Analyze a repository:**

```bash
curl -X POST http://localhost:8000/api/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "repo_url": "https://github.com/owner/repository",
    "max_files": 100
  }'
```

**Response:**
```json
{
  "status": "success",
  "message": "Successfully analyzed 95 files",
  "repo_url": "https://github.com/owner/repository",
  "total_files": 1250,
  "files_analyzed": 95,
  "documentation_path": "/path/to/outputs/repository/index.html",
  "stats": {
    "code_files": 80,
    "markup_files": 10,
    "config_files": 5,
    "functions": 450,
    "classes": 85,
    "languages": {
      "python": 45,
      "javascript": 25,
      "typescript": 10
    }
  }
}
```

### Python Client

```python
import requests

response = requests.post(
    "http://localhost:8000/api/analyze",
    json={
        "repo_url": "https://github.com/psf/requests",
        "max_files": 100
    }
)

result = response.json()
print(f"Documentation: {result['documentation_path']}")
```

### Command Line

```bash
# Quick test with small repository
python test_api.py

# Analyze specific repository
curl -X POST http://localhost:8000/api/analyze \
  -H "Content-Type: application/json" \
  -d '{"repo_url": "https://github.com/octocat/Hello-World", "max_files": 50}'
```

---

## 🎯 Supported Languages

### Programming Languages
- **Python** (.py)
- **JavaScript/Node.js** (.js, .jsx, .mjs)
- **TypeScript** (.ts, .tsx)
- **Java** (.java)
- **C/C++** (.c, .cpp, .h, .hpp)
- **C#** (.cs)
- **Go** (.go)
- **Rust** (.rs)
- **Ruby** (.rb)
- **PHP** (.php)
- **Swift** (.swift)
- **Kotlin** (.kt, .kts)
- **Scala** (.scala)

### Other Files
- Markup files (.html, .xml, .md, .rst)
- Stylesheets (.css, .scss, .sass)
- Configuration (.json, .yaml, .toml, .ini)

---

## ⚙️ Configuration

### Repository Size Guidelines

| Repo Size | Files | Recommended max_files | Expected Time |
|-----------|-------|----------------------|---------------|
| Tiny | < 50 | 50 | ~10 seconds |
| Small | 50-200 | 100 | ~30 seconds |
| Medium | 200-1000 | 100-150 | ~60 seconds |
| Large | 1000-5000 | 100-150 | ~90 seconds |
| Huge | 5000+ | 50-100 | ~60 seconds |

### Environment Variables

```bash
# Optional: AI enhancement with Google Gemini
GEMINI_API_KEY=your_api_key_here

# Optional: Increase GitHub API rate limits
GITHUB_TOKEN=ghp_your_token_here
```

**Get API Keys:**
- Gemini API: https://makersuite.google.com/app/apikey
- GitHub Token: https://github.com/settings/tokens

---

## 🛠️ Development

### Running Tests

```bash
cd BE

# Run diagnostic checks
python diagnose.py

# Run API tests with sample repositories
python test_api.py

# Auto-fix common issues
python autofix.py
```

### Project Scripts

- **`start.py`** - Smart startup with environment checks
- **`diagnose.py`** - Comprehensive diagnostic tool
- **`autofix.py`** - Automatically fixes common setup issues
- **`test_api.py`** - Test suite with sample repositories
- **`create_docgen.py`** - Creates the docgen.py file

---

## 📖 Documentation Output

### Generated Files

```
outputs/
└── repository-name/
    └── index.html          # Beautiful HTML documentation
```

### Documentation Includes

1. **Project Overview** (AI-generated)
   - Purpose and domain analysis
   - Architecture overview
   - Technology stack
   - Key features

2. **Repository Statistics**
   - File counts by type
   - Language distribution
   - Code metrics (functions, classes)

3. **File-by-File Analysis**
   - Individual file documentation
   - Functions and classes
   - Line numbers and references

4. **Visual Elements**
   - Language distribution charts
   - File category breakdowns
   - Interactive navigation

---

## 🔧 Troubleshooting

### Common Issues

#### "ModuleNotFoundError: No module named 'docgen'"

**Solution:**
```bash
cd BE
python create_docgen.py
```

#### "Request timed out"

**Solution:**
```bash
# Use smaller max_files parameter
curl -X POST http://localhost:8000/api/analyze \
  -H "Content-Type: application/json" \
  -d '{"repo_url": "https://github.com/owner/repo", "max_files": 50}'

# Set GitHub token
export GITHUB_TOKEN=your_token
```

#### Graphviz not found

**Windows:**
```bash
# Download from: https://graphviz.org/download/
# OR use Chocolatey:
choco install graphviz
```

**Linux:**
```bash
sudo apt install graphviz
```

**Mac:**
```bash
brew install graphviz
```

### Getting Help

1. **Run diagnostics:**
   ```bash
   cd BE
   python diagnose.py
   ```

2. **Check the documentation:**
   - `TROUBLESHOOTING.md` - Detailed troubleshooting guide
   - `LARGE_REPOS.md` - Handling large repositories
   - `QUICK_FIX.txt` - Quick reference for common issues

---

## 🏗️ Architecture

### Multi-Agent System

CodeBase Genius uses a multi-agent architecture built with Jaclang:

1. **Supervisor Agent** - Orchestrates the entire pipeline
2. **RepoMapper Agent** - Maps repository structure via GitHub API
3. **CodeAnalyzer Agent** - Analyzes code with multi-language support
4. **DocGenie Agent** - Generates beautiful HTML documentation

### Technology Stack

- **Jaclang** - Agent orchestration and workflow
- **FastAPI** - REST API server
- **Python** - Core analysis implementation
- **Google Gemini 2.0** - AI-powered insights
- **GitHub API** - Repository data access

---

## 📊 Example Output

### Sample Analysis

For repository: `github/linguist` (2,037 files)

```
📊 Complete Repository Analysis:
   Total files in repository: 2,037
   Total directories: 401
   Files analyzed: 150
   - Code files: 120
   - Markup files: 20
   - Config files: 10
   Functions found: 450
   Classes found: 85
```

**Generated Documentation:** `outputs/linguist/index.html`

Open in browser to see:
- Beautiful responsive design
- Language distribution charts
- Detailed file analysis
- AI-generated overview

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

## 🙏 Acknowledgments

- Built with [Jaclang](https://www.jac-lang.org/) - The AI-first programming language
- Powered by [Google Gemini 2.0](https://deepmind.google/technologies/gemini/)
- Uses [Tree-sitter](https://tree-sitter.github.io/tree-sitter/) for code parsing
- GitHub API for repository access

---

## 📞 Support

- **Documentation**: Check the `/docs` folder for detailed guides
- **Issues**: Report bugs via GitHub Issues
- **Discussions**: Join the discussions for questions and ideas

---

## 🗺️ Roadmap

- [ ] Support for private repositories
- [ ] Real-time collaboration features
- [ ] Code quality metrics and recommendations
- [ ] Integration with CI/CD pipelines
- [ ] Multi-repository analysis
- [ ] Export to multiple formats (PDF, DOCX)
- [ ] Interactive code visualization
- [ ] Custom documentation templates

---

**Made with ❤️ using Jaclang and AI**

*Transform your codebase into beautiful, comprehensive documentation in minutes!*