"""
Summary Generator Module

This module generates a summary of the changes and risks between two legal documents.
"""

import json
from typing import Dict, List, Any
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser


class SummaryGenerator:
    """
    A class that generates a summary of the changes and risks between two legal documents.
    """

    def __init__(self):
        """Initialize the summary generator."""
        self.llm = ChatGroq(model="meta-llama/llama-4-scout-17b-16e-instruct", temperature=0)

    def generate(self, doc1: str, doc2: str, comparison_result: Dict[str, Any], risk_analysis: Dict[str, Any]) -> str:
        """
        Generate a summary of the changes and risks between two legal documents.

        Args:
            doc1: Content of the first document
            doc2: Content of the second document
            comparison_result: The result of the document comparison
            risk_analysis: The result of the risk analysis

        Returns:
            A markdown-formatted summary
        """
        # Handle the comparison result
        # First, ensure comparison_result is a dictionary
        if not isinstance(comparison_result, dict):
            comparison_result = {"final_comparison": comparison_result}

        # Convert inputs to strings if they're not already
        if "final_comparison" in comparison_result:
            if isinstance(comparison_result["final_comparison"], dict):
                final_comparison = json.dumps(comparison_result["final_comparison"])
            else:
                final_comparison = str(comparison_result["final_comparison"])
        else:
            final_comparison = "{}"

        # Handle risk analysis
        if isinstance(risk_analysis, dict):
            risk_analysis_str = json.dumps(risk_analysis)
        else:
            risk_analysis_str = str(risk_analysis)

        # Create the summary prompt
        summary_prompt = ChatPromptTemplate.from_template(
            """You are a legal document summarization expert.
            I have two versions of a legal document and have already performed comparison and risk analyses.

            # Final Comparison:
            {final_comparison}

            # Risk Analysis:
            {risk_analysis}

            Please generate a comprehensive, well-structured markdown report that summarizes the changes and risks.

            The report should include:

            1. Executive Summary
               - Brief overview of the documents compared
               - Summary of the most significant changes
               - Summary of the most critical risks

            2. Detailed Changes Analysis
               - Structural changes (added/removed/reorganized sections)
               - Semantic changes (terms, obligations, conditions)
               - Impact assessment of these changes

            3. Risk Assessment
               - Legal risks
               - Business risks
               - Operational risks
               - Strategic risks

            4. Recommendations
               - Suggested actions to address identified risks
               - Areas that may require further legal review

            Format the report in clear, professional markdown with appropriate headings, bullet points, and emphasis where needed.
            """
        )

        # Create and run the summary chain
        summary_chain = summary_prompt | self.llm | StrOutputParser()

        summary = summary_chain.invoke({
            "final_comparison": final_comparison,
            "risk_analysis": risk_analysis_str
        })

        return summary
