"""
Document Comparison Module

This module implements the document comparison functionality using LangChain.
"""

import json
from typing import Dict, Any
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser


class DocumentComparisonGraph:
    """
    A class that implements a document comparison workflow.
    """

    def __init__(self):
        """Initialize the document comparison."""
        self.llm = ChatGroq(model="meta-llama/llama-4-scout-17b-16e-instruct", temperature=0)

    def run(self, doc1: str, doc2: str) -> Dict[str, Any]:
        """
        Run the document comparison.

        Args:
            doc1: Content of the first document
            doc2: Content of the second document

        Returns:
            A dictionary containing the comparison results
        """
        # Structural comparison
        structural_comparison_prompt = ChatPromptTemplate.from_template(
            """You are a legal document comparison expert.
            I have two versions of a legal document. Please analyze their structural differences.

            # Document 1:
            {doc1}

            # Document 2:
            {doc2}

            Perform a detailed structural comparison of these documents. Focus on:
            1. Added or removed sections
            2. Changes in section numbering or organization
            3. Changes in document structure

            Format your response as a JSON object with the following structure:
            ```json
            {{
                "added_sections": [{{"section": "section_name", "content": "content"}}],
                "removed_sections": [{{"section": "section_name", "content": "content"}}],
                "reorganized_sections": [{{"old_section": "old_name", "new_section": "new_name"}}]
            }}
            ```

            Only include the JSON in your response, no other text."""
        )

        structural_comparison_chain = structural_comparison_prompt | self.llm | StrOutputParser()
        structural_result = structural_comparison_chain.invoke({"doc1": doc1, "doc2": doc2})

        # Semantic comparison
        semantic_comparison_prompt = ChatPromptTemplate.from_template(
            """You are a legal document comparison expert.
            I have two versions of a legal document. Please analyze their semantic differences.

            # Document 1:
            {doc1}

            # Document 2:
            {doc2}

            Perform a detailed semantic comparison of these documents. Focus on:
            1. Changes in language, terms, and definitions
            2. Changes in obligations, rights, or responsibilities
            3. Changes in conditions or requirements

            Format your response as a JSON object with the following structure:
            ```json
            {{
                "term_changes": [{{"term": "term_name", "old_definition": "old_def", "new_definition": "new_def"}}],
                "obligation_changes": [{{"party": "party_name", "old_obligation": "old_obl", "new_obligation": "new_obl"}}],
                "condition_changes": [{{"condition": "condition_name", "old_text": "old_text", "new_text": "new_text"}}]
            }}
            ```

            Only include the JSON in your response, no other text."""
        )

        semantic_comparison_chain = semantic_comparison_prompt | self.llm | StrOutputParser()
        semantic_result = semantic_comparison_chain.invoke({"doc1": doc1, "doc2": doc2})

        # Final comparison
        final_comparison_prompt = ChatPromptTemplate.from_template(
            """You are a legal document comparison expert.
            I have two versions of a legal document and have already performed structural and semantic analyses.

            # Structural Analysis:
            {structural_comparison}

            # Semantic Analysis:
            {semantic_comparison}

            Please synthesize these analyses into a comprehensive comparison. Include:
            1. A summary of the most significant changes
            2. An assessment of how these changes affect the overall agreement
            3. Identification of any potential inconsistencies created by the changes

            Format your response as a JSON object with the following structure:
            ```json
            {{
                "significant_changes": [{{"category": "category", "description": "description", "impact": "impact"}}],
                "overall_assessment": "text",
                "potential_inconsistencies": [{{"description": "description", "location": "location"}}]
            }}
            ```

            Only include the JSON in your response, no other text."""
        )

        final_comparison_chain = final_comparison_prompt | self.llm | StrOutputParser()
        final_result = final_comparison_chain.invoke({
            "structural_comparison": structural_result,
            "semantic_comparison": semantic_result
        })

        # Try to parse JSON if the results are strings
        try:
            structural_analysis = json.loads(structural_result)
        except json.JSONDecodeError:
            structural_analysis = structural_result

        try:
            semantic_analysis = json.loads(semantic_result)
        except json.JSONDecodeError:
            semantic_analysis = semantic_result

        try:
            final_analysis = json.loads(final_result)
        except json.JSONDecodeError:
            final_analysis = final_result

        return {
            "structural_comparison": structural_analysis,
            "semantic_comparison": semantic_analysis,
            "final_comparison": final_analysis
        }
