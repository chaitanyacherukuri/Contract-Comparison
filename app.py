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
from src.comparison.document_comparison import DocumentComparisonGraph
from src.risk_analysis.risk_analyzer import RiskAnalyzer
from src.summary.summary_generator import SummaryGenerator

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
        return

    print(f"Loading documents: {args.doc1} and {args.doc2}")

    # Load documents
    loader = DocumentLoader()
    doc1_content = loader.load_document(args.doc1)
    doc2_content = loader.load_document(args.doc2)

    print("Documents loaded successfully.")

    # Create comparison graph
    comparison_graph = DocumentComparisonGraph()
    try:
        comparison_result = comparison_graph.run(doc1_content, doc2_content)
        print("Document comparison completed.")
    except Exception as e:
        print(f"Error during document comparison: {e}")
        print("Creating a simplified comparison result...")
        # Create a simplified comparison result
        comparison_result = {
            "structural_comparison": "Error during structural comparison",
            "semantic_comparison": "Error during semantic comparison",
            "final_comparison": "Error during final comparison"
        }

    # Analyze risks
    risk_analyzer = RiskAnalyzer()
    risk_analysis = risk_analyzer.analyze(doc1_content, doc2_content, comparison_result)

    print("Risk analysis completed.")

    # Generate summary
    summary_generator = SummaryGenerator()
    summary = summary_generator.generate(doc1_content, doc2_content, comparison_result, risk_analysis)

    print("Summary generation completed.")

    # Save the report
    with open(args.output, 'w') as f:
        f.write(summary)

    print(f"Comparison report saved to {args.output}")

if __name__ == "__main__":
    main()
