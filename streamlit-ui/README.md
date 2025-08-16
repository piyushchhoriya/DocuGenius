# 🚀 DocuGenius Streamlit UI

**AI-Powered Technical Documentation Generator with Streamlit Interface**

A beautiful, interactive Streamlit-based frontend for DocuGenius that provides the same powerful functionality as the React version, but with Python-native Streamlit components.

## ✨ Features

- **🎨 Beautiful Streamlit Interface**: Modern, responsive design with custom CSS styling
- **🔍 Smart Language Detection**: Automatically detects programming languages in your code
- **📊 Interactive Visualizations**: Plotly charts and diagrams for better understanding
- **🎯 Multiple Documentation Modes**: Explain, API Docs, How-to, Tutorial, and Diagram generation
- **👥 Audience Adaptation**: Beginner, Intermediate, and Expert content levels
- **⚡ Real-time Generation**: Fast, responsive documentation creation
- **📖 Source Citations**: Clear attribution with source information
- **📈 Analytics Dashboard**: Usage statistics and performance metrics
- **⚙️ Configurable Settings**: Customizable API endpoints and display options

## 🚀 Quick Start

### **Option 1: One-Command Startup (Recommended)**
```bash
python start_streamlit.py
```

### **Option 2: Manual Startup**
```bash
# Terminal 1: Start Backend (if not already running)
python start_backend.py

# Terminal 2: Start Streamlit UI
cd streamlit-ui
pip install -r requirements.txt
streamlit run app.py
```

### **Option 3: Direct Streamlit Run**
```bash
cd streamlit-ui
streamlit run app.py --server.port 8501
```

## 🌐 Access Points

- **Streamlit UI**: http://localhost:8501
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health

## 🎯 What You'll See

### **1. 🏠 Home Page**
- **System Status**: Backend health check and metrics
- **Key Features**: Overview of all capabilities
- **Quick Start**: Get started with examples

### **2. 🔍 Generate Page**
- **Smart Code Editor**: Ace editor with syntax highlighting
- **Language Detection**: Automatic programming language detection
- **Mode Selection**: Choose documentation type
- **Audience Levels**: Select target audience
- **Real-time Results**: Live documentation generation

### **3. 📚 Examples Page**
- **Preset Prompts**: Ready-to-use examples
- **Category Filtering**: Filter by Frontend, Backend, Architecture, etc.
- **One-Click Loading**: Load examples directly into the generator

### **4. ⚙️ Settings Page**
- **API Configuration**: Backend URL and connection testing
- **Display Options**: Customize UI behavior
- **Theme Settings**: Light/Dark mode preferences
- **Advanced Options**: Timeout and token limits

### **5. 📊 Analytics Page**
- **Usage Statistics**: Query counts and success rates
- **Performance Metrics**: Response times and trends
- **Mode Distribution**: Popular documentation types
- **Interactive Charts**: Plotly visualizations

## 🔧 Technical Stack

### **Frontend**
- **Streamlit**: Main web framework
- **Streamlit Ace**: Code editor component
- **Streamlit Option Menu**: Navigation menu
- **Plotly**: Interactive charts and diagrams
- **Pandas**: Data manipulation and analysis

### **Styling**
- **Custom CSS**: Professional gradient designs
- **Responsive Layout**: Mobile-friendly interface
- **Dark/Light Themes**: Automatic theme detection
- **Modern UI**: Clean, professional appearance

### **Backend Integration**
- **FastAPI**: RESTful API communication
- **Requests**: HTTP client for API calls
- **JSON**: Data serialization
- **Error Handling**: Robust error management

## 🎨 UI Components

### **1. Smart Code Editor**
```python
query = st_ace(
    placeholder="Paste your code here or ask a technical question...",
    language="text",
    theme="monokai",
    height=200,
    key="query_input"
)
```

### **2. Language Detection**
```python
def detect_language(text):
    patterns = {
        'python': [r'def\s+\w+\s*\(', r'import\s+\w+'],
        'javascript': [r'function\s+\w+\s*\(', r'const\s+\w+\s*='],
        # ... more patterns
    }
    # Automatic language detection logic
```

### **3. Interactive Results Display**
```python
def display_results(result):
    # Metrics display
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Generation Time", format_time(result.get('generation_time', 0)))
    # ... more result components
```

### **4. Mermaid Diagram Rendering**
```python
def render_mermaid_diagram(mermaid_code):
    # Parse Mermaid code and create Plotly visualizations
    # Interactive flowchart generation
```

## 📊 Features Comparison

| Feature | React UI | Streamlit UI |
|---------|----------|--------------|
| **Setup Complexity** | Medium (Node.js + npm) | Low (Python + pip) |
| **Customization** | High (Full CSS/JS control) | Medium (Streamlit + CSS) |
| **Development Speed** | Medium | High |
| **Deployment** | Build process required | Direct Python execution |
| **Interactive Charts** | Chart.js/D3.js | Plotly (built-in) |
| **Code Editor** | Custom component | Streamlit Ace |
| **Real-time Updates** | WebSocket/SSE | Streamlit session state |
| **Mobile Responsive** | Custom CSS | Streamlit responsive |

## 🔍 API Integration

### **Health Check**
```python
def health_check():
    try:
        response = requests.get(f"{API_BASE_URL}/health/", timeout=5)
        return response.status_code == 200, response.json()
    except requests.exceptions.RequestException:
        return False, None
```

### **Documentation Generation**
```python
def generate_documentation(request_data):
    try:
        response = requests.post(
            f"{API_BASE_URL}/ask/",
            json=request_data,
            timeout=30
        )
        return response.json() if response.status_code == 200 else None
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}
```

### **Mode Retrieval**
```python
def get_modes():
    try:
        response = requests.get(f"{API_BASE_URL}/ask/modes", timeout=5)
        return response.json() if response.status_code == 200 else None
    except requests.exceptions.RequestException:
        return None
```

## 🎯 Example Usage

### **1. Generate API Documentation**
```python
# Input: Python function
def calculate_fibonacci(n):
    if n <= 1:
        return n
    return calculate_fibonacci(n-1) + calculate_fibonacci(n-2)

# Mode: API Documentation
# Audience: Intermediate
# Result: Complete API docs with parameters, return types, examples
```

### **2. Create How-to Guide**
```python
# Query: "How to implement authentication in Flask"
# Mode: How-to Guide
# Audience: Beginner
# Result: Step-by-step instructions with code examples
```

### **3. Generate Architecture Diagram**
```python
# Query: "Microservices communication patterns"
# Mode: Diagram
# Audience: Expert
# Result: Mermaid diagram + Plotly visualization
```

## 🔧 Configuration

### **Environment Variables**
```bash
# Optional: Override default API URL
export DOCUGENIUS_API_URL=http://localhost:8000
```

### **Streamlit Configuration**
```toml
# .streamlit/config.toml
[server]
port = 8501
enableCORS = false
enableXsrfProtection = false

[theme]
primaryColor = "#667eea"
backgroundColor = "#ffffff"
secondaryBackgroundColor = "#f0f2f6"
textColor = "#262730"
```

## 🚀 Deployment

### **Local Development**
```bash
# Install dependencies
pip install -r requirements.txt

# Run development server
streamlit run app.py --server.port 8501
```

### **Production Deployment**
```bash
# Using Docker
docker build -t docugenius-streamlit .
docker run -p 8501:8501 docugenius-streamlit

# Using Streamlit Cloud
# Deploy directly to streamlit.io
```

### **Docker Configuration**
```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 8501

CMD ["streamlit", "run", "app.py", "--server.port", "8501", "--server.address", "0.0.0.0"]
```

## 📈 Performance Optimization

### **1. Caching**
```python
@st.cache_data
def get_modes():
    # Cache API responses
    return DocuGeniusAPI.get_modes()
```

### **2. Session State Management**
```python
# Store results in session state
if 'doc_result' in st.session_state:
    display_results(st.session_state.doc_result)
```

### **3. Error Handling**
```python
try:
    result = DocuGeniusAPI.generate_documentation(request_data)
    if result and 'error' not in result:
        st.session_state.doc_result = result
        st.success("✅ Documentation generated successfully!")
except Exception as e:
    st.error(f"❌ Error: {str(e)}")
```

## 🔍 Troubleshooting

### **Common Issues**

#### **1. Backend Connection Failed**
```bash
# Check if backend is running
curl http://localhost:8000/health/

# Start backend if needed
python start_backend.py
```

#### **2. Dependencies Installation Issues**
```bash
# Upgrade pip
pip install --upgrade pip

# Install with verbose output
pip install -r requirements.txt -v
```

#### **3. Port Already in Use**
```bash
# Check what's using port 8501
lsof -i :8501

# Kill process or use different port
streamlit run app.py --server.port 8502
```

#### **4. Streamlit Performance Issues**
```bash
# Clear cache
streamlit cache clear

# Run with debug mode
streamlit run app.py --logger.level debug
```

## 🎉 Benefits of Streamlit UI

### **1. Rapid Development**
- **Python-native**: No need to learn JavaScript/React
- **Built-in components**: Rich set of pre-built widgets
- **Fast iteration**: Hot-reload for instant feedback

### **2. Easy Deployment**
- **Streamlit Cloud**: One-click deployment
- **Docker support**: Containerized deployment
- **Python ecosystem**: Leverage existing Python tools

### **3. Data Science Integration**
- **Pandas/Plotly**: Native data visualization
- **ML/AI libraries**: Easy integration with scikit-learn, TensorFlow, etc.
- **Jupyter compatibility**: Import from notebooks

### **4. Professional Appearance**
- **Custom CSS**: Professional styling
- **Responsive design**: Mobile-friendly interface
- **Interactive elements**: Rich user experience

## 🔮 Future Enhancements

### **Planned Features**
1. **Real-time Collaboration**: Multi-user editing
2. **Advanced Analytics**: Detailed usage insights
3. **Custom Themes**: User-defined color schemes
4. **Export Options**: PDF, Markdown, HTML export
5. **Integration APIs**: Connect with external tools

### **Technical Improvements**
1. **WebSocket Support**: Real-time updates
2. **Advanced Caching**: Redis integration
3. **Performance Monitoring**: Detailed metrics
4. **A/B Testing**: Feature experimentation

---

## 🎯 Conclusion

The DocuGenius Streamlit UI provides a **powerful, user-friendly alternative** to the React version, offering:

- ✅ **Easy setup and deployment**
- ✅ **Rich interactive features**
- ✅ **Professional appearance**
- ✅ **Seamless backend integration**
- ✅ **Comprehensive documentation generation**
- ✅ **Analytics and monitoring**

**Perfect for Python developers who want a quick, beautiful interface for AI-powered documentation generation! 🚀**

---

**Built with ❤️ for the DocuGenius project**

**Ready to generate amazing technical documentation with Streamlit! 🎉**
