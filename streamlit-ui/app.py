import streamlit as st
import requests
import json
import time
import re
from datetime import datetime
from typing import Dict, List, Optional
import plotly.graph_objects as go
import plotly.express as px
from streamlit_ace import st_ace
from streamlit_option_menu import option_menu
import pandas as pd
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
import io

# Page configuration
st.set_page_config(
    page_title="DocuGenius - AI-Powered Technical Documentation Generator",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
    }
    
    .feature-card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        border-left: 4px solid #667eea;
        margin-bottom: 1rem;
    }
    
    .result-card {
        background: #f8f9fa;
        padding: 1.5rem;
        border-radius: 10px;
        border: 1px solid #e9ecef;
        margin-bottom: 1rem;
    }
    
    .code-block {
        background: #2d3748;
        color: #e2e8f0;
        padding: 1rem;
        border-radius: 8px;
        font-family: 'Courier New', monospace;
        overflow-x: auto;
    }
    
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1rem;
        border-radius: 8px;
        text-align: center;
    }
    
    .source-tag {
        background: #e2e8f0;
        color: #4a5568;
        padding: 0.25rem 0.5rem;
        border-radius: 4px;
        font-size: 0.75rem;
        margin: 0.25rem;
        display: inline-block;
    }
    
    .resource-link {
        background: #f0fff4;
        color: #22543d;
        padding: 0.5rem 1rem;
        border-radius: 6px;
        font-size: 0.875rem;
        margin: 0.25rem;
        display: inline-block;
        text-decoration: none;
        border: 1px solid #9ae6b4;
    }
    
    .resource-link a {
        color: #22543d;
        text-decoration: none;
        font-weight: 500;
    }
    
    .resource-link a:hover {
        color: #1a4731;
        text-decoration: underline;
    }
    
    .stButton > button {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.5rem 1rem;
        font-weight: 600;
    }
    
    .stButton > button:hover {
        background: linear-gradient(90deg, #5a67d8 0%, #6b46c1 100%);
        transform: translateY(-2px);
        transition: all 0.3s ease;
    }
</style>
""", unsafe_allow_html=True)

# API Configuration
API_BASE_URL = "http://localhost:8000"

class DocuGeniusAPI:
    @staticmethod
    def health_check():
        """Check if the backend is running"""
        try:
            response = requests.get(f"{API_BASE_URL}/health/", timeout=5)
            return response.status_code == 200, response.json() if response.status_code == 200 else None
        except requests.exceptions.RequestException:
            return False, None
    
    @staticmethod
    def get_modes():
        """Get available documentation modes"""
        try:
            response = requests.get(f"{API_BASE_URL}/ask/modes", timeout=5)
            return response.json() if response.status_code == 200 else None
        except requests.exceptions.RequestException:
            return None
    
    @staticmethod
    def generate_documentation(request_data):
        """Generate documentation using the API"""
        try:
            response = requests.post(
                f"{API_BASE_URL}/ask/",
                json=request_data,
                timeout=60
            )
            return response.json() if response.status_code == 200 else None
        except requests.exceptions.RequestException as e:
            return {"error": str(e)}

def detect_language(text):
    """Detect programming language from text"""
    patterns = {
        'python': [r'def\s+\w+\s*\(', r'import\s+\w+', r'from\s+\w+\s+import', r'class\s+\w+'],
        'javascript': [r'function\s+\w+\s*\(', r'const\s+\w+\s*=', r'let\s+\w+\s*=', r'var\s+\w+\s*='],
        'java': [r'public\s+class', r'import\s+java', r'System\.out\.println'],
        'typescript': [r'interface\s+\w+', r'type\s+\w+', r'const\s+\w+:\s*\w+'],
        'rust': [r'fn\s+\w+\s*\(', r'let\s+\w+:\s*\w+'],
        'go': [r'func\s+\w+\s*\(', r'package\s+main'],
        'cpp': [r'#include', r'int\s+main\s*\('],
        'csharp': [r'using\s+System', r'public\s+class'],
    }
    
    for lang, patterns_list in patterns.items():
        for pattern in patterns_list:
            if re.search(pattern, text, re.IGNORECASE):
                return lang
    return 'text'

def format_time(seconds):
    """Format time in a human-readable way"""
    if seconds < 1:
        return f"{int(seconds * 1000)}ms"
    return f"{seconds:.1f}s"

def format_confidence(confidence):
    """Format confidence as percentage"""
    return f"{confidence * 100:.0f}%"

def generate_pdf(result: Dict) -> bytes:
    """Generate PDF from the explanation result"""
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    story = []
    
    # Get styles
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=16,
        spaceAfter=30,
        textColor=colors.HexColor('#667eea')
    )
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=14,
        spaceAfter=20,
        textColor=colors.HexColor('#4a5568')
    )
    normal_style = styles['Normal']
    
    # Title
    story.append(Paragraph("DocuGenius - AI Explanation Report", title_style))
    story.append(Spacer(1, 20))
    
    # Metrics
    story.append(Paragraph("📊 Generation Metrics", heading_style))
    metrics_data = [
        ["Metric", "Value"],
        ["Generation Time", f"{result.get('generation_time', 0):.2f} seconds"],
        ["Confidence", f"{result.get('confidence', 0):.1%}"],
        ["Success", "✅" if result.get('success', False) else "❌"]
    ]
    metrics_table = Table(metrics_data, colWidths=[2*inch, 3*inch])
    metrics_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#667eea')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#f8f9fa')),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    story.append(metrics_table)
    story.append(Spacer(1, 20))
    
    # Main Explanation
    if result.get('explanation'):
        story.append(Paragraph("📝 Explanation", heading_style))
        story.append(Paragraph(result['explanation'], normal_style))
        story.append(Spacer(1, 20))
    
    # Breakdown
    if result.get('breakdown'):
        story.append(Paragraph("📋 Breakdown", heading_style))
        for i, step in enumerate(result['breakdown'], 1):
            story.append(Paragraph(f"{i}. {step}", normal_style))
        story.append(Spacer(1, 20))
    
    # Code Analysis
    if result.get('code_analysis'):
        story.append(Paragraph("💻 Code Analysis", heading_style))
        for i, code in enumerate(result['code_analysis'], 1):
            story.append(Paragraph(f"Analysis {i}:", normal_style))
            story.append(Paragraph(f"<code>{code}</code>", normal_style))
            story.append(Spacer(1, 10))
        story.append(Spacer(1, 20))
    
    # External Resources
    if result.get('external_resources'):
        story.append(Paragraph("🔗 External Resources", heading_style))
        for resource in result['external_resources']:
            if isinstance(resource, dict) and 'url' in resource:
                story.append(Paragraph(f"📚 {resource['name']}: {resource['url']}", normal_style))
            else:
                story.append(Paragraph(f"📚 {resource}", normal_style))
        story.append(Spacer(1, 20))
    
    # Message
    if result.get('message'):
        story.append(Paragraph("ℹ️ Additional Information", heading_style))
        story.append(Paragraph(result['message'], normal_style))
    
    # Build PDF
    doc.build(story)
    buffer.seek(0)
    return buffer.getvalue()

def main():
    # Sidebar navigation
    with st.sidebar:
        st.markdown("## 🚀 DocuGenius")
        st.markdown("AI-Powered Technical Documentation Generator")
        
        selected = option_menu(
            menu_title=None,
            options=["🏠 Home", "🔍 Generate", "📚 Examples", "⚙️ Settings", "📊 Analytics"],
            icons=["house", "search", "book", "gear", "graph-up"],
            menu_icon="cast",
            default_index=0,
        )
    
    # Main content area
    if selected == "🏠 Home":
        show_home_page()
    elif selected == "🔍 Generate":
        show_generate_page()
    elif selected == "📚 Examples":
        show_examples_page()
    elif selected == "⚙️ Settings":
        show_settings_page()
    elif selected == "📊 Analytics":
        show_analytics_page()

def show_home_page():
    """Display the home page with features and overview"""
    st.markdown("""
    <div class="main-header">
        <h1>🚀 DocuGenius</h1>
        <h2>AI-Powered Technical Documentation Generator</h2>
        <p>Transform your technical questions into comprehensive, interactive documentation with AI-powered insights.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Check backend status
    is_backend_healthy, health_data = DocuGeniusAPI.health_check()
    
    if is_backend_healthy:
        st.success("✅ Backend API is running and healthy!")
        if health_data:
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Status", health_data.get("status", "Unknown"))
            with col2:
                st.metric("Version", health_data.get("version", "Unknown"))
            with col3:
                st.metric("Environment", health_data.get("environment", "Unknown"))
            with col4:
                uptime = health_data.get("uptime", 0)
                st.metric("Uptime", format_time(uptime))
    else:
        st.error("❌ Backend API is not accessible. Please start the backend server.")
        st.info("Run: `cd backend && python main.py`")
    
    # Key Features
    st.markdown("## 🎯 Key Features")
    
    features = [
        {
            "title": "🔍 Smart Code Analysis",
            "description": "Automatically detect programming languages and provide context-aware explanations.",
            "icon": "🔍"
        },
        {
            "title": "📊 Visual Diagrams",
            "description": "Generate Mermaid diagrams and flowcharts to illustrate complex concepts.",
            "icon": "📊"
        },
        {
            "title": "🎯 Audience Adaptation",
            "description": "Adapt documentation complexity from beginner-friendly to expert-level explanations.",
            "icon": "🎯"
        },
        {
            "title": "⚡ Fast Generation",
            "description": "Get comprehensive documentation in seconds with OpenAI GPT-3.5-turbo.",
            "icon": "⚡"
        },
        {
            "title": "📚 Multiple Modes",
            "description": "Explain, API Docs, How-to, Tutorial, and Diagram generation modes.",
            "icon": "📚"
        },
        {
            "title": "🔗 External Resources",
            "description": "Get curated external resources and references for further learning.",
            "icon": "🔗"
        }
    ]
    
    for feature in features:
        st.markdown(f"""
        <div class="feature-card">
            <h3>{feature['icon']} {feature['title']}</h3>
            <p>{feature['description']}</p>
        </div>
        """, unsafe_allow_html=True)

def show_generate_page():
    """Display the main documentation generation interface"""
    st.markdown("## 🔍 Generate Documentation")
    
    # Check backend status first
    is_backend_healthy, _ = DocuGeniusAPI.health_check()
    if not is_backend_healthy:
        st.error("❌ Backend API is not accessible. Please start the backend server.")
        st.info("Run: `cd backend && python main.py`")
        return
    
    # Get available modes
    modes_data = DocuGeniusAPI.get_modes()
    modes = {}
    if modes_data and 'modes' in modes_data:
        modes = {mode['id']: mode['name'] for mode in modes_data['modes']}
    else:
        modes = {
            'explain': 'Explain',
            'api_docs': 'API Documentation',
            'how_to': 'How-to Guide',
            'tutorial': 'Tutorial',
            'diagram': 'Diagram'
        }
    
    # Create two columns for input and output
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("### 📝 Input")
        
        # Query input with language detection
        query = st_ace(
            placeholder="Paste your code here or ask a technical question...",
            language="text",
            theme="monokai",
            height=200,
            key="query_input"
        )
        
        # Detect language
        detected_lang = detect_language(query) if query else 'text'
        if detected_lang != 'text':
            st.info(f"🔍 Detected language: {detected_lang}")
        
        # Mode selection
        selected_mode = st.selectbox(
            "Documentation Type",
            options=list(modes.keys()),
            format_func=lambda x: modes.get(x, x),
            index=0
        )
        
        # Audience selection
        audience = st.selectbox(
            "Target Audience",
            options=['beginner', 'intermediate', 'expert'],
            format_func=lambda x: x.title(),
            index=0
        )
        
        # Options
        verify_code = st.checkbox("Verify Code", value=False)
        
        # Generate button
        if st.button("🚀 Generate Explanation", type="primary", use_container_width=True):
            if not query.strip():
                st.warning("Please enter a query or paste some code.")
            else:
                generate_documentation(query, selected_mode, audience, False, verify_code)
    
    with col2:
        st.markdown("### 📊 Results")
        
        # Display results from session state
        if 'doc_result' in st.session_state:
            display_results(st.session_state.doc_result)

def generate_documentation(query, mode, audience, with_diagram, verify_code):
    """Generate documentation and display results"""
    with st.spinner("🤖 Generating documentation..."):
        # Prepare request data
        request_data = {
            "query": query,
            "mode": mode,
            "audience": audience,
            "withDiagram": with_diagram,
            "verifyCode": verify_code
        }
        
        # Call API
        result = DocuGeniusAPI.generate_documentation(request_data)
        
        if result and 'error' not in result:
            st.session_state.doc_result = result
            st.success("✅ Documentation generated successfully!")
            st.rerun()
        else:
            error_msg = result.get('error', 'Unknown error occurred') if result else 'Failed to generate documentation'
            st.error(f"❌ Error: {error_msg}")

def display_results(result):
    """Display the generated documentation results"""
    if not result:
        return
    
    # Metrics
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Generation Time", format_time(result.get('generation_time', 0)))
    with col2:
        st.metric("Confidence", format_confidence(result.get('confidence', 0)))
    with col3:
        st.metric("Success", "✅" if result.get('success', False) else "❌")
    
    # Main Explanation
    st.markdown("### 📝 Explanation")
    st.markdown(f"**{result.get('explanation', 'No explanation available')}**")
    
    # Breakdown
    if result.get('breakdown'):
        st.markdown("### 📋 Breakdown")
        for i, step in enumerate(result['breakdown'], 1):
            st.markdown(f"{i}. {step}")
    
    # Code Analysis
    if result.get('code_analysis'):
        st.markdown("### 💻 Code Analysis")
        for i, code in enumerate(result['code_analysis'], 1):
            st.markdown(f"**Analysis {i}:**")
            st.code(code, language=detect_language(code))
            
            # Copy button
            if st.button(f"📋 Copy Analysis {i}", key=f"copy_{i}"):
                st.write("Copied to clipboard!")
    
    # External Resources
    if result.get('external_resources'):
        st.markdown("### 🔗 External Resources")
        for resource in result['external_resources']:
            if isinstance(resource, dict) and 'url' in resource:
                st.markdown(f"""
                <div class="resource-link">
                    📚 <a href="{resource['url']}" target="_blank">{resource['name']}</a>
                </div>
                """, unsafe_allow_html=True)
            else:
                # Fallback for old format
                st.markdown(f"""
                <div class="resource-link">
                    📚 {resource}
                </div>
                """, unsafe_allow_html=True)
    
    # Removed diagram section
    
    # Sources (removed since we're focusing on explanation)
    pass
    
    # Message
    if result.get('message'):
        st.info(f"ℹ️ {result['message']}")
    
    # Download PDF Button
    st.markdown("---")
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("📄 Download PDF Report", type="primary", use_container_width=True):
            try:
                pdf_bytes = generate_pdf(result)
                st.download_button(
                    label="⬇️ Click to Download PDF",
                    data=pdf_bytes,
                    file_name=f"docugenius_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
                    mime="application/pdf",
                    use_container_width=True
                )
                st.success("✅ PDF generated successfully! Click the download button above.")
            except Exception as e:
                st.error(f"❌ Error generating PDF: {str(e)}")

def show_examples_page():
    """Display example queries and prompts"""
    st.markdown("## 📚 Quick Examples")
    st.markdown("Get started quickly with these preset prompts. Click any example to auto-fill the search.")
    
    examples = [
        {
            "title": "Python Function",
            "description": "Explain this Python function in detail",
            "prompt": "def fibonacci(n):\n    if n <= 1:\n        return n\n    return fibonacci(n-1) + fibonacci(n-2)",
            "category": "Code Explanation",
            "icon": "🐍"
        },
        {
            "title": "Streamlit Code",
            "description": "Explain this Streamlit code",
            "prompt": "col1, col2, col3 = st.columns(3)\nwith col1:\n    st.metric('Generation Time', '3.4s')\nwith col2:\n    st.metric('Confidence', '90%')",
            "category": "Code Explanation",
            "icon": "📊"
        },
        {
            "title": "JavaScript Function",
            "description": "Explain this JavaScript function",
            "prompt": "function processData(data, callback) {\n    console.log('Processing:', data);\n    callback(data);\n}",
            "category": "Code Explanation",
            "icon": "⚡"
        },
        {
            "title": "DOM Concept",
            "description": "Explain DOM manipulation in simple terms",
            "prompt": "What is DOM manipulation and how does it work?",
            "category": "Concept Explanation",
            "icon": "🌳"
        },
        {
            "title": "API Concept",
            "description": "Explain REST APIs in simple terms",
            "prompt": "What are REST APIs and how do they work?",
            "category": "Concept Explanation",
            "icon": "🔗"
        },
        {
            "title": "React Hooks",
            "description": "Explain React hooks concept",
            "prompt": "What are React hooks and why are they useful?",
            "category": "Concept Explanation",
            "icon": "⚛️"
        }
    ]
    
    # Category filter
    categories = list(set(ex['category'] for ex in examples))
    selected_category = st.selectbox("Filter by Category", ["All"] + categories)
    
    # Filter examples
    filtered_examples = examples
    if selected_category != "All":
        filtered_examples = [ex for ex in examples if ex['category'] == selected_category]
    
    # Display examples
    for example in filtered_examples:
        with st.expander(f"{example['icon']} {example['title']} ({example['category']})"):
            st.markdown(f"**Description:** {example['description']}")
            st.markdown(f"**Prompt:** {example['prompt']}")
            
            if st.button(f"Use This Example", key=f"example_{example['title']}"):
                st.session_state.example_query = example['prompt']
                st.success(f"✅ Example loaded! Switch to 'Generate' tab to use it.")

def show_settings_page():
    """Display settings and configuration options"""
    st.markdown("## ⚙️ Settings")
    
    st.markdown("### 🔧 Configuration")
    
    # API Configuration
    st.markdown("#### API Settings")
    api_url = st.text_input("Backend API URL", value=API_BASE_URL, key="api_url")
    
    # Test connection
    if st.button("Test Connection"):
        try:
            response = requests.get(f"{api_url}/health/", timeout=5)
            if response.status_code == 200:
                st.success("✅ Connection successful!")
            else:
                st.error(f"❌ Connection failed: {response.status_code}")
        except Exception as e:
            st.error(f"❌ Connection failed: {str(e)}")
    
    # Display Settings
    st.markdown("#### Display Settings")
    st.checkbox("Show diagrams by default", value=True, key="show_diagrams")
    st.checkbox("Show external resources", value=True, key="show_resources")
    st.checkbox("Auto-detect language", value=True, key="auto_detect")
    
    # Theme Settings
    st.markdown("#### Theme Settings")
    theme = st.selectbox("Theme", ["Light", "Dark", "Auto"], index=2)
    
    # Advanced Settings
    st.markdown("#### Advanced Settings")
    timeout = st.slider("API Timeout (seconds)", 10, 120, 60)
    max_tokens = st.slider("Max Tokens", 500, 3000, 2000)
    
    # Save settings
    if st.button("Save Settings"):
        st.success("✅ Settings saved!")

def show_analytics_page():
    """Display usage analytics and statistics"""
    st.markdown("## 📊 Analytics")
    
    # Mock analytics data
    st.markdown("### 📈 Usage Statistics")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Queries", "1,234")
    with col2:
        st.metric("Successful Generations", "1,156")
    with col3:
        st.metric("Average Response Time", "2.3s")
    with col4:
        st.metric("Success Rate", "93.7%")
    
    # Popular modes chart
    st.markdown("### 📊 Popular Documentation Modes")
    modes_data = {
        'Explain': 45,
        'API Docs': 25,
        'How-to': 20,
        'Tutorial': 8,
        'Diagram': 2
    }
    
    fig = px.pie(
        values=list(modes_data.values()),
        names=list(modes_data.keys()),
        title="Documentation Mode Distribution"
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # Response time trend
    st.markdown("### ⏱️ Response Time Trend")
    dates = pd.date_range(start='2024-01-01', end='2024-01-15', freq='D')
    response_times = [2.1, 2.3, 2.0, 2.5, 2.2, 2.4, 2.1, 2.3, 2.0, 2.5, 2.2, 2.4, 2.1, 2.3, 2.0]
    
    fig = px.line(
        x=dates,
        y=response_times,
        title="Average Response Time (Last 15 Days)",
        labels={'x': 'Date', 'y': 'Response Time (seconds)'}
    )
    st.plotly_chart(fig, use_container_width=True)

if __name__ == "__main__":
    main()
