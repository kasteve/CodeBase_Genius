"""
Streamlit Frontend for CodeBase Genius
"""
import streamlit as st
import requests
import json
from pathlib import Path

# API Configuration
API_BASE_URL = "http://localhost:8000"

# Page config
st.set_page_config(
    page_title="CodeBase Genius",
    page_icon="🧠",
    layout="wide"
)

# Custom CSS
st.markdown("""
    <style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        color: #1f77b4;
        margin-bottom: 2rem;
    }
    .success-box {
        padding: 1rem;
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        border-radius: 0.25rem;
        color: #155724;
    }
    .error-box {
        padding: 1rem;
        background-color: #f8d7da;
        border: 1px solid #f5c6cb;
        border-radius: 0.25rem;
        color: #721c24;
    }
    </style>
""", unsafe_allow_html=True)

# Header
st.markdown('<div class="main-header">🧠 CodeBase Genius</div>', unsafe_allow_html=True)
st.markdown("### AI-Powered Codebase Documentation Generator")
st.markdown("---")

# Sidebar
with st.sidebar:
    st.header("📊 Navigation")
    page = st.radio(
        "Select Page",
        ["Generate Documentation", "View Repositories", "About"]
    )
    
    st.markdown("---")
    st.markdown("### 🔧 Settings")
    try:
        health_check = requests.get(f"{API_BASE_URL}/health", timeout=2)
        if health_check.status_code == 200:
            health_data = health_check.json()
            st.success("✅ API Connected")
            if health_data.get('graphviz_available'):
                st.info("✅ Graphviz Available")
            else:
                st.warning("⚠️ Graphviz Not Available")
        else:
            st.error("❌ API Disconnected")
    except:
        st.error("❌ API Disconnected")

# Main content
if page == "Generate Documentation":
    st.header("📝 Generate Documentation")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        repo_url = st.text_input(
            "GitHub Repository URL",
            placeholder="https://github.com/owner/repository",
            help="Enter the full GitHub repository URL"
        )
    
    with col2:
        st.markdown("<br>", unsafe_allow_html=True)
        analyze_button = st.button("🚀 Analyze Repository", type="primary", use_container_width=True)
    
    # Example repositories
    st.markdown("#### 💡 Example Repositories")
    example_cols = st.columns(3)
    
    example_repo = None
    with example_cols[0]:
        if st.button("octocat/Hello-World"):
            example_repo = "https://github.com/octocat/Hello-World"
    
    with example_cols[1]:
        if st.button("octocat/linguist"):
            example_repo = "https://github.com/octocat/linguist"
    
    with example_cols[2]:
        if st.button("torvalds/linux"):
            example_repo = "https://github.com/torvalds/linux"
    
    # Use example repo if clicked
    if example_repo:
        repo_url = example_repo
        analyze_button = True
    
    if analyze_button and repo_url:
        with st.spinner("🔄 Analyzing repository... This may take a few moments..."):
            try:
                # Call API
                response = requests.post(
                    f"{API_BASE_URL}/api/analyze",
                    json={"repo_url": repo_url},
                    timeout=120
                )
                
                if response.status_code == 200:
                    result = response.json()
                    
                    # Success message
                    st.success(f"✅ {result.get('message', 'Analysis Complete!')}")
                    
                    # Display results
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        st.metric("📄 Files", result.get('file_count', 0))
                    
                    with col2:
                        st.metric("📁 Directories", result.get('directory_count', 0))
                    
                    with col3:
                        st.metric("📊 Status", result.get('status', 'unknown').upper())
                    
                    # Documentation section
                    st.markdown("---")
                    st.markdown("### 📚 Generated Documentation")
                    
                    doc_path = result.get('documentation_path')
                    
                    # Debug info (can be removed in production)
                    with st.expander("🔍 Debug Info"):
                        st.json(result)
                        st.write(f"Doc path from API: {doc_path}")
                        if doc_path:
                            st.write(f"File exists: {Path(doc_path).exists()}")
                    
                    if doc_path:
                        doc_file = Path(doc_path)
                        
                        if doc_file.exists():
                            # Check if it's HTML or Markdown
                            is_html = doc_file.suffix == '.html' or doc_file.name == 'index.html'
                            
                            if is_html:
                                # Beautiful HTML documentation!
                                st.success("✨ Beautiful HTML documentation generated!")
                                
                                col1, col2 = st.columns(2)
                                with col1:
                                    # Button to open in browser
                                    if st.button("🌐 Open in Browser", type="primary"):
                                        import webbrowser
                                        webbrowser.open(f'file://{doc_file.absolute()}')
                                        st.info("📖 Documentation opened in your default browser!")
                                
                                with col2:
                                    # Download HTML
                                    with open(doc_file, 'r', encoding='utf-8') as f:
                                        html_content = f.read()
                                    st.download_button(
                                        label="⬇️ Download HTML",
                                        data=html_content,
                                        file_name=f"{repo_url.split('/')[-1]}_docs.html",
                                        mime="text/html"
                                    )
                                
                                # Show preview in iframe
                                st.markdown("### 👀 Preview")
                                with open(doc_file, 'r', encoding='utf-8') as f:
                                    html_content = f.read()
                                st.components.v1.html(html_content, height=600, scrolling=True)
                                
                            else:
                                # Markdown fallback
                                try:
                                    with open(doc_file, 'r', encoding='utf-8') as f:
                                        markdown_content = f.read()
                                    
                                    # Download button
                                    st.download_button(
                                        label="⬇️ Download Documentation",
                                        data=markdown_content,
                                        file_name=f"{repo_url.split('/')[-1]}_docs.md",
                                        mime="text/markdown"
                                    )
                                    
                                    # Display markdown
                                    with st.expander("📖 View Documentation", expanded=True):
                                        st.markdown(markdown_content)
                                except Exception as e:
                                    st.error(f"Error reading documentation file: {str(e)}")
                        else:
                            st.error(f"❌ Documentation file not found at: {doc_file}")
                            st.info("The file may have been generated but the path is incorrect. Check the debug info above.")
                    else:
                        st.warning("⚠️ No documentation path returned from API")
                    
                    # Diagram section
                    diagram_path = result.get('diagram_path')
                    if diagram_path:
                        diagram_file = Path(diagram_path)
                        
                        if diagram_file.exists():
                            st.markdown("### 📊 Code Context Graph")
                            st.image(str(diagram_file), caption="Code relationships diagram", use_container_width=True)
                        else:
                            st.info(f"ℹ️ Diagram not available (Graphviz may not be configured)")
                
                else:
                    error_detail = response.json().get('detail', 'Unknown error')
                    st.error(f"❌ Error: {error_detail}")
                    
            except requests.exceptions.Timeout:
                st.error("⏱️ Request timed out. The repository might be too large.")
            except requests.exceptions.RequestException as e:
                st.error(f"❌ Connection Error: {str(e)}")
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
                import traceback
                with st.expander("🐛 Error Details"):
                    st.code(traceback.format_exc())

elif page == "View Repositories":
    st.header("📂 Analyzed Repositories")
    
    try:
        response = requests.get(f"{API_BASE_URL}/api/repositories")
        
        if response.status_code == 200:
            data = response.json()
            repos = data.get('repositories', [])
            
            if repos:
                for repo in repos:
                    with st.expander(f"📦 {repo['name']}"):
                        col1, col2 = st.columns([3, 1])
                        
                        with col1:
                            st.write(f"**Documentation:** {repo['docs_path']}")
                            st.write(f"**Has Diagram:** {'✅ Yes' if repo['has_diagram'] else '❌ No'}")
                        
                        with col2:
                            # Read and provide download
                            if Path(repo['docs_path']).exists():
                                with open(repo['docs_path'], 'r', encoding='utf-8') as f:
                                    content = f.read()
                                st.download_button(
                                    "⬇️ Download",
                                    content,
                                    file_name=f"{repo['name']}_docs.md",
                                    mime="text/markdown",
                                    key=f"download_{repo['name']}"
                                )
            else:
                st.info("No repositories analyzed yet. Generate documentation from the 'Generate Documentation' page.")
        else:
            st.error("Failed to load repositories")
            
    except Exception as e:
        st.error(f"Error: {str(e)}")

else:  # About page
    st.header("ℹ️ About CodeBase Genius")
    
    st.markdown("""
    ### 🎯 What is CodeBase Genius?
    
    CodeBase Genius is an AI-powered tool that automatically analyzes GitHub repositories 
    and generates comprehensive documentation.
    
    ### ✨ Features
    
    - 🔍 **Repository Mapping**: Analyzes repository structure
    - 📊 **Code Analysis**: Identifies functions, classes, and relationships
    - 📝 **Auto Documentation**: Generates detailed markdown documentation
    - 🎨 **Visualization**: Creates code context graphs
    - 🚀 **Fast & Easy**: Simple URL input, instant results
    
    ### 🛠️ Technology Stack
    
    - **Backend**: FastAPI + Jaclang
    - **Frontend**: Streamlit
    - **Analysis**: Python AST parsing
    - **Visualization**: Graphviz
    
    ### 📞 Support
    
    For issues or questions, please contact the development team.
    """)

# Footer
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: gray;'>CodeBase Genius v1.0.0 | Built with ❤️ using Jac & Streamlit</div>",
    unsafe_allow_html=True
)