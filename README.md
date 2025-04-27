# Legal Document Comparison Tool

This application compares two legal documents and provides a detailed summary of all the changes present in both documents, as well as flagging potential risk areas.

## Features

- Document loading from various formats (PDF, DOCX, TXT)
- Structural and semantic comparison of legal documents
- Risk analysis of identified changes
- Comprehensive summary report generation
- User-friendly web interface with interactive visualizations

## Architecture

The application is built using LangGraph, a framework for building agentic applications with a focus on complex reasoning processes. It uses the Groq API with the "meta-llama/llama-4-scout-17b-16e-instruct" model for all language processing tasks.

The architecture consists of a unified workflow with the following nodes:

1. **Document Loader**: Handles loading and preprocessing documents from various formats
2. **Structural Analysis**: Analyzes the structural differences between documents
3. **Semantic Analysis**: Analyzes the semantic differences between documents
4. **Final Analysis**: Combines structural and semantic analyses into a comprehensive comparison
5. **Risk Analyzer**: Identifies and assesses risks in the changes
6. **Summary Generation**: Creates a comprehensive report

The workflow uses a state dictionary pattern, where each node updates the state with its results, and subsequent nodes have access to the updates from previous nodes through the state dictionary.

## Installation

1. Clone the repository
2. Create a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
4. Set up your Groq API key in a `.env` file:
   ```
   GROQ_API_KEY=your_groq_api_key_here
   ```

## Usage

Before running the application, make sure to set your Groq API key in the `.env` file:

```
GROQ_API_KEY=your_groq_api_key_here
```

### Command Line Interface

Run the application with:

```
python app.py --doc1 path/to/first/document --doc2 path/to/second/document --output report.md
```

Example:

```
python app.py --doc1 data/sample_documents/contract_v1.txt --doc2 data/sample_documents/contract_v2.txt --output comparison_report.md
```

### Web Interface

The application also provides a user-friendly web interface using Streamlit. To launch the web interface:

```
streamlit run streamlit_app.py
```

The web interface offers the following features:
- Drag-and-drop document uploads
- Support for PDF, DOCX, and TXT files
- Clean, minimalist interface with tabbed navigation
- Interactive results display with expandable sections
- Color-coded risk analysis
- One-click report download

#### Screenshots

![Streamlit UI - Document Upload](docs/images/streamlit_upload.png)
*Document upload interface with drag-and-drop functionality*

![Streamlit UI - Comparison Results](docs/images/streamlit_results.png)
*Interactive comparison results with expandable sections*

![Streamlit UI - Download Report](docs/images/streamlit_download.png)
*Download comparison report functionality*

> Note: You'll need to take screenshots of the application and save them in the `docs/images` directory.

## Testing

You can test the application using the provided test scripts:

1. Test the document loader:
   ```
   python test_app.py
   ```

2. Test the complete workflow:
   ```
   python test_workflow.py
   ```

These tests will help verify that the workflow is working correctly before running the full application.

## Sample Documents

The repository includes sample documents in the `data/sample_documents` directory:

- `contract_v1.txt`: Original contract
- `contract_v2.txt`: Modified contract with various changes

## Output

The application generates a markdown report that includes:

1. Executive Summary
2. Detailed Changes Analysis
3. Risk Assessment
4. Recommendations

## License

MIT
