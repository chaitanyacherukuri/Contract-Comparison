#!/usr/bin/env python3
"""
Test script for the Contract Comparison Workflow
"""

import os
import json
from dotenv import load_dotenv
from src.document_loaders.loader import DocumentLoader
from src.workflow.contract_comparison_workflow import ContractComparisonWorkflow

# Load environment variables
load_dotenv()

def test_workflow():
    """Test the contract comparison workflow."""
    # Check if API key is set
    if not os.getenv("GROQ_API_KEY"):
        print("Error: GROQ_API_KEY environment variable is not set.")
        print("Please set it in the .env file or as an environment variable.")
        return

    print("Starting workflow test...")

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

        # Create a simplified version of the documents for testing
        doc1_sample = doc1_content[:1000]
        doc2_sample = doc2_content[:1000]

        # Run the workflow
        print("\nCreating and running workflow...")
        workflow = ContractComparisonWorkflow()
        result = workflow.run(doc1_sample, doc2_sample)

        print("Workflow completed successfully.")
        
        # Print the keys in the result
        print("\nWorkflow result keys:", result.keys())
        
        # Print samples of each step's output
        print("\nStructural comparison sample:")
        structural_str = str(result["structural_comparison"])
        print(structural_str[:200] + "..." if len(structural_str) > 200 else structural_str)
        
        print("\nSemantic comparison sample:")
        semantic_str = str(result["semantic_comparison"])
        print(semantic_str[:200] + "..." if len(semantic_str) > 200 else semantic_str)
        
        print("\nFinal comparison sample:")
        final_str = str(result["final_comparison"])
        print(final_str[:200] + "..." if len(final_str) > 200 else final_str)
        
        print("\nRisk analysis sample:")
        risk_str = str(result["risk_analysis"])
        print(risk_str[:200] + "..." if len(risk_str) > 200 else risk_str)
        
        print("\nSummary sample:")
        summary = result["summary"]
        print(summary[:500] + "..." if len(summary) > 500 else summary)
        
        print("\nWorkflow test passed!")
        
        # Save the summary to a file
        with open("workflow_test_report.md", "w") as f:
            f.write(summary)
        print("\nTest report saved to workflow_test_report.md")
        
    except Exception as e:
        print(f"Error in workflow test: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_workflow()
