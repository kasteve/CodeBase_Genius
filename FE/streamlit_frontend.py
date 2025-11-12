"""
Streamlit Frontend for CodeBase Genius
"""
import streamlit as st
import sys
import os
from pathlib import Path

# Add the parent directory to the path so we can import from BE
sys.path.insert(0, str(Path(__file__).parent.parent / "BE"))

from py.repo_mapper import RepoMapper
from py.code_analyzer import CodeAnalyzer
from py.docgen import DocGenerator


# Page configuration
st.set_page_config(
    page_title="CodeBase Genius",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        padding: 1rem;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .section-header {
        font-size: 1.5rem;
        font-weight: bold;
        margin-top: 2rem;
        margin-bottom: 1rem;
        color: #667eea;
    }
    .stProgress > div > div > div > div {
        background-color: #667eea;
    }
    </style>
""", unsafe_allow_html=True)

# Header
st.markdown('<div class="main-header">🧠 CodeBase Genius</div>', unsafe_allow_html=True)
st.markdown("### Automatically generate comprehensive documentation for any GitHub repository")

# Sidebar
with st.sidebar:
    st.header("⚙️ Configuration")
    
    github_token = st.text_input(
        "GitHub Token (Optional)",
        type="password",
        help="Provide a GitHub token to increase API rate limits"
    )
    
    if github_token:
        os.environ['GITHUB_TOKEN'] = github_token
    
    st.markdown("---")
    st.markdown("### 📖 How it works")
    st.markdown("""
    1. **Map Repository** - Analyze repository structure
    2. **Analyze Code** - Detect languages and dependencies
    3. **Generate Docs** - Create comprehensive documentation
    """)
    
    st.markdown("---")
    st.markdown("### 🔗 Quick Links")
    st.markdown("- [GitHub](https://github.com)")
    st.markdown("- [Documentation]()")

# Main content
tab1, tab2, tab3 = st.tabs(["🚀 Generate Docs", "📊 Analytics", "📄 History"])

with tab1:
    st.markdown('<div class="section-header">Generate Documentation</div>', unsafe_allow_html=True)
    
    # Input form
    col1, col2 = st.columns([3, 1])
    
    with col1:
        repo_url = st.text_input(
            "Repository URL",
            placeholder="https://github.com/owner/repository",
            help="Enter the full GitHub repository URL"
        )
    
    with col2:
        st.markdown("<br>", unsafe_allow_html=True)
        generate_btn = st.button("🚀 Generate", use_container_width=True, type="primary")
    
    # Process when button is clicked
    if generate_btn and repo_url:
        if not repo_url.startswith("https://github.com/"):
            st.error("❌ Please enter a valid GitHub repository URL")
        else:
            # Progress tracking
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            # Step 1: Map Repository
            status_text.text("📂 Step 1/3: Mapping repository structure...")
            progress_bar.progress(10)
            
            mapper = RepoMapper(repo_url)
            repo_data = mapper.map_repository()
            
            if not repo_data.get('success'):
                st.error(f"❌ Error mapping repository: {repo_data.get('error')}")
                st.stop()
            
            progress_bar.progress(33)
            
            # Display repo mapping results
            with st.expander("📂 Repository Structure", expanded=True):
                col1, col2, col3 = st.columns(3)
                col1.metric("Total Files", repo_data.get('file_count', 0))
                col2.metric("Directories", repo_data.get('directory_count', 0))
                col3.metric("Owner", repo_data.get('owner', 'N/A'))
            
            # Step 2: Analyze Code
            status_text.text("🔍 Step 2/3: Analyzing code patterns...")
            progress_bar.progress(40)
            
            analyzer = CodeAnalyzer(repo_url)
            analysis_data = analyzer.analyze_code()
            
            if not analysis_data.get('success'):
                st.warning(f"⚠️ Warning during analysis: {analysis_data.get('error')}")
            
            progress_bar.progress(66)
            
            # Display analysis results
            with st.expander("🔍 Code Analysis", expanded=True):
                col1, col2, col3 = st.columns(3)
                col1.metric("Primary Language", analysis_data.get('primary_language', 'Unknown'))
                col2.metric("Stars ⭐", analysis_data.get('stars', 0))
                col3.metric("Forks 🍴", analysis_data.get('forks', 0))
                
                if analysis_data.get('description'):
                    st.info(f"📝 {analysis_data['description']}")
                
                # Languages breakdown
                languages = analysis_data.get('languages', {})
                if languages:
                    st.markdown("**Languages:**")
                    total_bytes = sum(languages.values())
                    for lang, bytes_count in sorted(languages.items(), key=lambda x: x[1], reverse=True):
                        percentage = (bytes_count / total_bytes) * 100
                        st.progress(percentage / 100, text=f"{lang}: {percentage:.1f}%")
            
            # Step 3: Generate Documentation
            status_text.text("📝 Step 3/3: Generating documentation...")
            progress_bar.progress(75)
            
            docgen = DocGenerator(repo_url)
            docs_data = docgen.generate_docs()
            
            if not docs_data.get('success'):
                st.error(f"❌ Error generating documentation: {docs_data.get('error')}")
                st.stop()
            
            progress_bar.progress(100)
            status_text.text("✅ Documentation generated successfully!")
            
            # Display documentation results
            with st.expander("📄 Generated Documentation", expanded=True):
                st.success(f"✅ Documentation saved to: `{docs_data.get('output_path')}`")
                st.info(f"📊 Generated {docs_data.get('sections_count')} sections")
                
                # Preview
                st.markdown("**Preview:**")
                st.code(docs_data.get('preview', ''), language='markdown')
                
                # Download button
                if docs_data.get('output_path') and os.path.exists(docs_data['output_path']):
                    with open(docs_data['output_path'], 'r', encoding='utf-8') as f:
                        doc_content = f.read()
                    
                    st.download_button(
                        label="📥 Download Documentation",
                        data=doc_content,
                        file_name=f"{repo_data.get('repo', 'repo')}_docs.md",
                        mime="text/markdown"
                    )
            
            st.balloons()
    
    elif generate_btn:
        st.warning("⚠️ Please enter a repository URL")

with tab2:
    st.markdown('<div class="section-header">Analytics Dashboard</div>', unsafe_allow_html=True)
    st.info("📊 Analytics dashboard coming soon!")
    st.markdown("""
    This section will include:
    - Repository complexity metrics
    - Code quality scores
    - Documentation coverage
    - Historical trends
    """)

with tab3:
    st.markdown('<div class="section-header">Generation History</div>', unsafe_allow_html=True)
    st.info("📄 History tracking coming soon!")
    st.markdown("""
    This section will show:
    - Previously generated documentation
    - Generation timestamps
    - Repository snapshots
    - Version comparisons
    """)

# Footer
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: #666;'>
        <p>Made with ❤️ using Jaclang and Streamlit | CodeBase Genius v1.0</p>
    </div>
    """,
    unsafe_allow_html=True
)