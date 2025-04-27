# 📄 Legal Document Comparison Tool

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.8%2B-blue)
![LangGraph](https://img.shields.io/badge/LangGraph-0.0.25%2B-orange)
![Streamlit](https://img.shields.io/badge/Streamlit-1.44.0%2B-red)

A powerful AI-driven tool that compares legal documents and provides a detailed analysis of changes, highlighting potential risks and generating comprehensive reports.

## ✨ Features

- 📋 **Multi-format Support**: Load documents from PDF, DOCX, and TXT formats
- 🔍 **Dual Analysis**: Perform both structural and semantic comparison of legal documents
- ⚠️ **Risk Assessment**: Identify and categorize potential risks in document changes
- 📊 **Comprehensive Reports**: Generate detailed summary reports with executive summaries
- 🖥️ **Interactive UI**: User-friendly web interface with drag-and-drop functionality
- 📱 **Responsive Design**: Clean, modern interface that works on various devices
- 📥 **PDF Export**: Download comparison reports as PDF files

## 🏗️ Architecture

The application is built using **LangGraph**, a framework for building agentic applications with complex reasoning processes. It leverages the **Groq API** with the `meta-llama/llama-4-scout-17b-16e-instruct` model for all language processing tasks.

### Workflow Components

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│  Document       │     │  Structural     │     │  Semantic       │
│  Loader         │────▶│  Analysis       │────▶│  Analysis       │
└─────────────────┘     └─────────────────┘     └─────────────────┘
                                                        │
                                                        ▼
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│  Summary        │     │  Risk           │     │  Final          │
│  Generation     │◀────│  Analyzer       │◀────│  Analysis       │
└─────────────────┘     └─────────────────┘     └─────────────────┘
```

The workflow uses a **state dictionary pattern**, where each node updates the state with its results, and subsequent nodes have access to the updates from previous nodes through the state dictionary.

## 🚀 Installation

### Prerequisites

- Python 3.8 or higher
- Groq API key

### Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/chaitanyacherukuri/Contract-Comparison.git
   cd Contract-Comparison
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up your Groq API key**

   **For local development:**
   Create a `.streamlit/secrets.toml` file with:
   ```toml
   [api_keys]
   groq = "your_groq_api_key_here"
   ```

   **For Streamlit Cloud deployment:**
   Add your Groq API key to the Streamlit Cloud secrets management in the dashboard.

## 🖥️ Usage

### Command Line Interface

Run the application with:

```bash
python app.py --doc1 path/to/first/document --doc2 path/to/second/document --output report.md
```

**Example:**
```bash
python app.py --doc1 data/sample_documents/contract_v1.txt --doc2 data/sample_documents/contract_v2.txt --output comparison_report.md
```

### Web Interface

Launch the user-friendly web interface:

```bash
streamlit run streamlit_app.py
```

The web interface provides:
- 📤 Drag-and-drop document uploads
- 📑 Support for PDF, DOCX, and TXT files
- 📊 Interactive results with expandable sections
- 🎨 Color-coded risk analysis
- 💾 One-click PDF report download

### Sample Documents

The repository includes sample documents in multiple formats:
- 📄 **TXT**: `contract_v1.txt` and `contract_v2.txt`
- 📑 **PDF**: `contract_v1.pdf` and `contract_v2.pdf`
- 📝 **DOCX**: `contract_v1.docx` and `contract_v2.docx`

You can use these to test the application without uploading your own documents.

## 🌐 Deployment

### Streamlit Cloud Deployment

1. Fork this repository to your GitHub account
2. Connect your GitHub repository to Streamlit Cloud
3. In the Streamlit Cloud dashboard, navigate to your app's settings
4. Under "Secrets", add your Groq API key:
   ```toml
   [api_keys]
   groq = "your_groq_api_key_here"
   ```
5. Deploy your application

## 🧪 Testing

Verify the application works correctly with the provided test scripts:

```bash
# Test the document loader
python test_app.py

# Test the complete workflow
python test_workflow.py
```

## 📋 Output Format

The application generates a comprehensive report that includes:

1. **Executive Summary**: Overview of the most important changes
2. **Detailed Changes Analysis**: In-depth analysis of structural and semantic changes
3. **Risk Assessment**: Evaluation of potential risks with severity ratings
4. **Recommendations**: Suggested actions based on the identified changes

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📜 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgements

- [LangGraph](https://github.com/langchain-ai/langgraph) for the workflow framework
- [Groq](https://groq.com/) for the high-performance LLM API
- [Streamlit](https://streamlit.io/) for the web interface framework
- [LangChain](https://github.com/langchain-ai/langchain) for LLM integration tools
