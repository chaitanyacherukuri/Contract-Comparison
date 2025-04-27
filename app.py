#!/usr/bin/env python3
"""
Contract Comparison Application

This application compares two legal documents and provides a detailed summary of changes
and potential risk areas using LangGraph and LLMs.
"""

import os
import argparse
from dotenv import load_dotenv
from src.document_loaders.loader import DocumentLoader
from src.workflow.contract_comparison_workflow import ContractComparisonWorkflow

# Load environment variables
load_dotenv()

def main():
    """Main entry point for the application."""
    parser = argparse.ArgumentParser(description='Compare two legal documents and identify changes and risks.')
    parser.add_argument('--doc1', type=str, required=True, help='Path to the first document')
    parser.add_argument('--doc2', type=str, required=True, help='Path to the second document')
    parser.add_argument('--output', type=str, default='comparison_report.md', help='Output file path')

    args = parser.parse_args()

    # Check if API key is set
    if not os.getenv("GROQ_API_KEY"):
        print("Error: GROQ_API_KEY environment variable is not set.")
        print("Please set it in the .env file or as an environment variable.")
        print("For Streamlit Cloud deployment, use the secrets.toml approach instead.")
        return

    print(f"Loading documents: {args.doc1} and {args.doc2}")

    # Load documents
    try:
        loader = DocumentLoader()
        doc1_content = loader.load_document(args.doc1)
        doc2_content = loader.load_document(args.doc2)
        print("Documents loaded successfully.")
    except Exception as e:
        print(f"Error loading documents: {e}")
        return

    # Run the workflow
    try:
        workflow = ContractComparisonWorkflow()
        print("Starting contract comparison workflow...")
        result = workflow.run(doc1_content, doc2_content)
        print("Workflow completed successfully.")

        # Extract the summary from the result
        summary = result["summary"]

        # Save the report
        with open(args.output, 'w') as f:
            f.write(summary)

        print(f"Comparison report saved to {args.output}")
    except Exception as e:
        print(f"Error during workflow execution: {e}")
        return

if __name__ == "__main__":
    main()
