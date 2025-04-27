# Legal Document Comparison Tool

This application compares two legal documents and provides a detailed summary of all the changes present in both documents, as well as flagging potential risk areas.

## Features

- Document loading from various formats (PDF, DOCX, TXT)
- Structural and semantic comparison of legal documents
- Risk analysis of identified changes
- Comprehensive summary report generation

## Architecture

The application is built using LangGraph, a framework for building agentic applications with a focus on complex reasoning processes. It uses the Groq API with the "meta-llama/llama-4-scout-17b-16e-instruct" model for all language processing tasks.

The architecture consists of:

1. **Document Ingestion Layer**: Handles loading and preprocessing documents
2. **Document Comparison Graph**: Performs structural and semantic comparison
3. **Risk Analysis Component**: Identifies and assesses risks in the changes
4. **Summary Generation**: Creates a comprehensive report

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

Run the application with:

```
python app.py --doc1 path/to/first/document --doc2 path/to/second/document --output report.md
```

Example:

```
python app.py --doc1 data/sample_documents/contract_v1.txt --doc2 data/sample_documents/contract_v2.txt --output comparison_report.md
```

## Testing

You can test individual components of the application using the provided test scripts:

1. Test the document loader:
   ```
   python test_app.py
   ```

2. Test all components individually:
   ```
   python test_components.py
   ```

These tests will help verify that each component is working correctly before running the full application.

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
