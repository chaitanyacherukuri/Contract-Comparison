#!/usr/bin/env python3
"""
Test script for the Contract Comparison Application
"""

import os
from dotenv import load_dotenv
from src.document_loaders.loader import DocumentLoader

# Load environment variables
load_dotenv()

def main():
    """Test the document loader."""
    # Check if API key is set
    if not os.getenv("GROQ_API_KEY"):
        print("Error: GROQ_API_KEY environment variable is not set.")
        print("Please set it in the .env file or as an environment variable.")
        print("For Streamlit Cloud deployment, use the secrets.toml approach instead.")
        return

    print("Testing document loader...")

    # Load documents
    loader = DocumentLoader()
    doc1_path = "data/sample_documents/contract_v1.txt"
    doc2_path = "data/sample_documents/contract_v2.txt"

    try:
        doc1_content = loader.load_document(doc1_path)
        doc2_content = loader.load_document(doc2_path)

        print(f"Successfully loaded {doc1_path}")
        print(f"Document 1 length: {len(doc1_content)} characters")
        print(f"Successfully loaded {doc2_path}")
        print(f"Document 2 length: {len(doc2_content)} characters")

        # Print a sample of each document
        print("\nSample of Document 1:")
        print(doc1_content[:200] + "...")
        print("\nSample of Document 2:")
        print(doc2_content[:200] + "...")

        print("\nDocument loader test passed!")
    except Exception as e:
        print(f"Error loading documents: {e}")

if __name__ == "__main__":
    main()
