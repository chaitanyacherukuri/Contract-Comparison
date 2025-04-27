"""
Risk Analysis Module

This module analyzes the risks in the changes between two legal documents.
"""

import json
from typing import Dict, List, Any
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser


class RiskAnalyzer:
    """
    A class that analyzes risks in the changes between two legal documents.
    """

    def __init__(self):
        """Initialize the risk analyzer."""
        self.llm = ChatGroq(model="meta-llama/llama-4-scout-17b-16e-instruct", temperature=0)

    def analyze(self, doc1: str, doc2: str, comparison_result: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze the risks in the changes between two legal documents.

        Args:
            doc1: Content of the first document
            doc2: Content of the second document
            comparison_result: The result of the document comparison

        Returns:
            A dictionary containing the risk analysis
        """
        # Handle the comparison result
        # First, ensure comparison_result is a dictionary
        if not isinstance(comparison_result, dict):
            comparison_result = {"structural_comparison": comparison_result,
                                "semantic_comparison": comparison_result,
                                "final_comparison": comparison_result}

        # Convert comparison result to string if it's not already
        if "structural_comparison" in comparison_result:
            if isinstance(comparison_result["structural_comparison"], dict):
                structural_comparison = json.dumps(comparison_result["structural_comparison"])
            else:
                structural_comparison = str(comparison_result["structural_comparison"])
        else:
            structural_comparison = "{}"

        if "semantic_comparison" in comparison_result:
            if isinstance(comparison_result["semantic_comparison"], dict):
                semantic_comparison = json.dumps(comparison_result["semantic_comparison"])
            else:
                semantic_comparison = str(comparison_result["semantic_comparison"])
        else:
            semantic_comparison = "{}"

        if "final_comparison" in comparison_result:
            if isinstance(comparison_result["final_comparison"], dict):
                final_comparison = json.dumps(comparison_result["final_comparison"])
            else:
                final_comparison = str(comparison_result["final_comparison"])
        else:
            final_comparison = "{}"

        # Create the risk analysis prompt
        risk_analysis_prompt = ChatPromptTemplate.from_template(
            """You are a legal risk assessment expert.
            I have two versions of a legal document and have already performed a comparison analysis.

            # Document 1:
            {doc1}

            # Document 2:
            {doc2}

            # Structural Comparison:
            {structural_comparison}

            # Semantic Comparison:
            {semantic_comparison}

            # Final Comparison:
            {final_comparison}

            Please analyze the risks associated with the changes between these documents. Focus on:
            1. Legal risks (e.g., compliance issues, regulatory concerns)
            2. Business risks (e.g., increased liability, unfavorable terms)
            3. Operational risks (e.g., new obligations, resource requirements)
            4. Strategic risks (e.g., long-term implications, competitive disadvantages)

            For each identified risk:
            - Provide a clear description of the risk
            - Explain why it's a risk
            - Rate its severity (Low, Medium, High)
            - Suggest potential mitigations

            Format your response as a JSON object with the following structure:
            ```json
            {{
                "legal_risks": [
                    {{
                        "description": "description",
                        "explanation": "explanation",
                        "severity": "severity",
                        "mitigation": "mitigation"
                    }}
                ],
                "business_risks": [...],
                "operational_risks": [...],
                "strategic_risks": [...]
            }}
            ```

            Only include the JSON in your response, no other text."""
        )

        # Create and run the risk analysis chain
        risk_analysis_chain = risk_analysis_prompt | self.llm | StrOutputParser()

        risk_analysis_result = risk_analysis_chain.invoke({
            "doc1": doc1,
            "doc2": doc2,
            "structural_comparison": structural_comparison,
            "semantic_comparison": semantic_comparison,
            "final_comparison": final_comparison
        })

        # Parse the result
        try:
            return json.loads(risk_analysis_result)
        except json.JSONDecodeError:
            # If the result is not valid JSON, return it as a string
            return {"error": "Failed to parse risk analysis result", "raw_result": risk_analysis_result}
