# 🚀 DocuGenius Startup Guide

## **AI-Powered Interactive Technical Documentation Generator**

This guide will help you get DocuGenius running with its new advanced features including RAG, prompt engineering, and multimodal output.

---

## 📋 **Prerequisites**

### **1. Python Environment**
- Python 3.8+ (recommended: 3.9+)
- pip package manager

### **2. OpenAI API Key**
- Get your API key from [OpenAI Platform](https://platform.openai.com/api-keys)
- Set environment variable: `export OPENAI_API_KEY=your_key_here`

### **3. System Requirements**
- At least 4GB RAM (8GB+ recommended)
- 2GB free disk space
- Internet connection for API calls

---

## 🛠️ **Installation & Setup**

### **Step 1: Install Dependencies**
```bash
# Install all required packages
pip install -r requirements.txt
```

### **Step 2: Verify Installation**
```bash
# Check if key packages are installed
python -c "import fastapi, streamlit, sentence_transformers, faiss; print('✅ All packages installed')"
```

---

## 🚀 **Running DocuGenius**

### **Option 1: Full System (Recommended)**

#### **Terminal 1: Start Backend API**
```bash
# Start the FastAPI backend server
python run_backend.py
```

**Expected Output:**
```
🚀 Starting DocuGenius Backend Server...
📚 AI-Powered Interactive Technical Documentation Generator
🌐 API will be available at: http://localhost:8000
📖 API Documentation: http://localhost:8000/docs
🔍 Health Check: http://localhost:8000/health
```

#### **Terminal 2: Start Frontend UI**
```bash
# Start the Streamlit frontend
streamlit run ui/app.py
```

**Expected Output:**
```
You can now view your Streamlit app in your browser.
Local: http://localhost:8501
Network: http://192.168.x.x:8501
```

### **Option 2: Backend Only (API Testing)**
```bash
# Just run the backend for API testing
python run_backend.py
```

Then visit:
- **API Root**: http://localhost:8000
- **Interactive Docs**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health

---

## 🔍 **Testing the System**

### **1. Health Check**
```bash
curl http://localhost:8000/health
```

**Expected Response:**
```json
{
  "status": "healthy",
  "timestamp": "2024-01-15 10:30:00",
  "uptime": 123.45,
  "version": "2.0.0",
  "environment": "development"
}
```

### **2. API Endpoints Test**
```bash
# Test documentation generation
curl -X POST "http://localhost:8000/ask" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "How to implement error handling in Python?",
    "mode": "explain",
    "audience": "beginner"
  }'
```

### **3. Frontend Testing**
1. Open http://localhost:8501 in your browser
2. Enter a query like: "Explain how to implement authentication"
3. Select mode: "explain"
4. Select audience: "beginner"
5. Click "Generate Documentation"

---

## 🎯 **Example Queries to Try**

### **Beginner Level**
- "How to create a simple calculator in Python?"
- "Explain what is a function and how to use it"
- "What is an API and how does it work?"

### **Intermediate Level**
- "How to implement user authentication with JWT tokens?"
- "Create a REST API design for a todo application"
- "Explain the MVC architecture pattern with examples"

### **Advanced Level**
- "Design a microservices architecture for an e-commerce platform"
- "Implement a caching strategy for high-traffic applications"
- "Create a CI/CD pipeline with Docker and Kubernetes"

---

## 🔧 **Troubleshooting**

### **Common Issues & Solutions**

#### **1. "FAISS index not found" Error**
```bash
# Solution: Run ingestion first
python ingestor/ingest.py examples/tiny_repos
```

#### **2. "OpenAI API key not found" Warning**
```bash
# Solution: Set environment variable
export OPENAI_API_KEY=your_actual_api_key_here
```

#### **3. "Connection refused" Error**
- Check if backend is running on port 8000
- Verify no firewall blocking the port
- Try: `netstat -an | grep 8000`

#### **4. "Module not found" Errors**
```bash
# Solution: Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

#### **5. Memory Issues**
- Close other applications
- Reduce `top_k` parameter in queries
- Restart the backend server

---

## 📊 **System Architecture**

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Streamlit UI  │    │   FastAPI       │    │   RAG Engine    │
│   (Frontend)    │◄──►│   (Backend)     │◄──►│   (Core)        │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   User Input    │    │   API Endpoints │    │   FAISS Index   │
│   & Display     │    │   & Validation  │    │   & Metadata    │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

---

## 🎨 **Features Overview**

### **🔍 RAG (Retrieval-Augmented Generation)**
- Multi-stage search (BM25 + Vector similarity)
- Intelligent reranking
- Context-aware responses

### **🎯 Advanced Prompt Engineering**
- Mode-specific prompting strategies
- Audience-level adaptation
- Systematic context management

### **📊 Multimodal Output**
- Text documentation
- Code examples
- Mermaid diagrams
- Source citations

### **⚡ Performance Features**
- Fast FAISS vector search
- Async API endpoints
- Intelligent caching
- Fallback modes

---

## 🔐 **Security & Best Practices**

### **1. API Key Management**
- Never commit API keys to version control
- Use environment variables
- Rotate keys regularly

### **2. Production Deployment**
- Disable CORS for production
- Add authentication middleware
- Use HTTPS in production
- Monitor API usage

### **3. Rate Limiting**
- Implement request throttling
- Monitor OpenAI API usage
- Set appropriate timeouts

---

## 📈 **Monitoring & Logs**

### **1. Backend Logs**
- Check terminal output for errors
- Look for "INFO" and "ERROR" messages
- Monitor API response times

### **2. Health Endpoints**
```bash
# System status
curl http://localhost:8000/health/status

# Readiness check
curl http://localhost:8000/health/ready

# System info
curl http://localhost:8000/health/info
```

### **3. Performance Metrics**
- Generation time per request
- API response times
- Memory usage
- CPU utilization

---

## 🚀 **Next Steps**

### **1. Explore the API**
- Visit http://localhost:8000/docs
- Try different endpoints
- Test various query types

### **2. Customize Prompts**
- Modify `app/core/rag_engine.py`
- Adjust system prompts
- Fine-tune audience levels

### **3. Add New Features**
- Implement code verification
- Add more diagram types
- Integrate with IDEs

---

## 📞 **Support & Resources**

### **Documentation**
- **API Docs**: http://localhost:8000/docs
- **Project README**: README.md
- **Code Structure**: Check `app/` directory

### **Common Commands**
```bash
# Start backend
python run_backend.py

# Start frontend
streamlit run ui/app.py

# Run tests
python -m pytest

# Check health
curl http://localhost:8000/health
```

---

## 🎉 **Congratulations!**

You now have a **production-ready, industry-level AI-powered documentation generator** running! 

This system demonstrates:
- ✅ **RAG (Retrieval-Augmented Generation)**
- ✅ **Advanced Prompt Engineering**
- ✅ **Multimodal Output Generation**
- ✅ **Professional API Design**
- ✅ **Modern Web Interface**

**Ready to impress recruiters and build amazing documentation! 🚀**

