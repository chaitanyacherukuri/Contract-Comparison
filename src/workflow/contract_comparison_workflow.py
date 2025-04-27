"""
Contract Comparison Workflow

This module implements a unified workflow for contract comparison using LangGraph.
The workflow includes document loading, structure analysis, semantic analysis,
final analysis, risk analysis, and summary generation.
"""

import json
from typing import Dict, List, Any, TypedDict, Annotated
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langgraph.graph import StateGraph, END


# Define the state schema
class ContractComparisonState(TypedDict):
    """State for the contract comparison workflow."""
    doc1_content: str
    doc2_content: str
    structural_comparison: Dict[str, Any]
    semantic_comparison: Dict[str, Any]
    final_comparison: Dict[str, Any]
    risk_analysis: Dict[str, Any]
    summary: str


class ContractComparisonWorkflow:
    """
    A unified workflow for contract comparison using LangGraph.
    """

    def __init__(self):
        """Initialize the contract comparison workflow."""
        self.llm = ChatGroq(model="meta-llama/llama-4-scout-17b-16e-instruct", temperature=0)
        self.graph = self._build_graph()

    def _build_graph(self) -> StateGraph:
        """
        Build the workflow graph.

        Returns:
            A StateGraph object representing the workflow
        """
        # Create the graph
        graph = StateGraph(ContractComparisonState)

        # Add nodes
        graph.add_node("structural_analysis", self._structural_analysis)
        graph.add_node("semantic_analysis", self._semantic_analysis)
        graph.add_node("final_analysis", self._final_analysis)
        graph.add_node("risk_analyzer", self._risk_analysis)
        graph.add_node("summary_generation", self._summary_generation)

        # Define the edges
        graph.add_edge("structural_analysis", "semantic_analysis")
        graph.add_edge("semantic_analysis", "final_analysis")
        graph.add_edge("final_analysis", "risk_analyzer")
        graph.add_edge("risk_analyzer", "summary_generation")
        graph.add_edge("summary_generation", END)

        # Set the entry point
        graph.set_entry_point("structural_analysis")

        # Compile the graph
        return graph.compile()

    def _structural_analysis(self, state: ContractComparisonState) -> ContractComparisonState:
        """
        Perform structural analysis on the documents.

        Args:
            state: The current state

        Returns:
            The updated state
        """
        doc1 = state["doc1_content"]
        doc2 = state["doc2_content"]

        # Create the structural comparison prompt
        structural_comparison_prompt = ChatPromptTemplate.from_template(
            """You are a legal document structure analyzer.
            I have two versions of a legal document and need to understand the structural changes between them.

            # Document 1:
            {doc1}

            # Document 2:
            {doc2}

            Please analyze the structural differences between these documents. Focus on:
            1. Added sections in Document 2 that weren't in Document 1
            2. Removed sections that were in Document 1 but aren't in Document 2
            3. Reorganized sections (sections that moved to different places)

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

        # Parse the result
        try:
            # Check if the result contains a JSON code block
            if "```json" in structural_result:
                # Extract the JSON part
                json_part = structural_result.split("```json")[1].split("```")[0].strip()
                structural_analysis = json.loads(json_part)
            else:
                structural_analysis = json.loads(structural_result)
        except json.JSONDecodeError:
            structural_analysis = {"error": "Failed to parse structural analysis result", "raw_result": structural_result}

        # Update the state
        return {**state, "structural_comparison": structural_analysis}

    def _semantic_analysis(self, state: ContractComparisonState) -> ContractComparisonState:
        """
        Perform semantic analysis on the documents.

        Args:
            state: The current state

        Returns:
            The updated state
        """
        doc1 = state["doc1_content"]
        doc2 = state["doc2_content"]

        # Create the semantic comparison prompt
        semantic_comparison_prompt = ChatPromptTemplate.from_template(
            """You are a legal document semantic analyzer.
            I have two versions of a legal document and need to understand the semantic changes between them.

            # Document 1:
            {doc1}

            # Document 2:
            {doc2}

            Please analyze the semantic differences between these documents. Focus on:
            1. Changes in defined terms
            2. Changes in obligations for each party
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

        # Parse the result
        try:
            # Check if the result contains a JSON code block
            if "```json" in semantic_result:
                # Extract the JSON part
                json_part = semantic_result.split("```json")[1].split("```")[0].strip()
                semantic_analysis = json.loads(json_part)
            else:
                semantic_analysis = json.loads(semantic_result)
        except json.JSONDecodeError:
            semantic_analysis = {"error": "Failed to parse semantic analysis result", "raw_result": semantic_result}

        # Update the state
        return {**state, "semantic_comparison": semantic_analysis}

    def _final_analysis(self, state: ContractComparisonState) -> ContractComparisonState:
        """
        Perform final analysis on the documents.

        Args:
            state: The current state

        Returns:
            The updated state
        """
        structural_result = state["structural_comparison"]
        semantic_result = state["semantic_comparison"]

        # Convert to string if they are dictionaries
        structural_str = json.dumps(structural_result) if isinstance(structural_result, dict) else str(structural_result)
        semantic_str = json.dumps(semantic_result) if isinstance(semantic_result, dict) else str(semantic_result)

        # Create the final comparison prompt
        final_comparison_prompt = ChatPromptTemplate.from_template(
            """You are a legal document analysis expert.
            I have performed structural and semantic analyses of two versions of a legal document.

            # Structural Analysis:
            {structural_comparison}

            # Semantic Analysis:
            {semantic_comparison}

            Please provide a final comprehensive analysis of the changes between these documents. Focus on:
            1. The most significant changes and their potential impact
            2. An overall assessment of how substantially the document has changed
            3. Any potential inconsistencies or issues created by the changes

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
            "structural_comparison": structural_str,
            "semantic_comparison": semantic_str
        })

        # Parse the result
        try:
            # Check if the result contains a JSON code block
            if "```json" in final_result:
                # Extract the JSON part
                json_part = final_result.split("```json")[1].split("```")[0].strip()
                final_analysis = json.loads(json_part)
            else:
                final_analysis = json.loads(final_result)
        except json.JSONDecodeError:
            final_analysis = {"error": "Failed to parse final analysis result", "raw_result": final_result}

        # Update the state
        return {**state, "final_comparison": final_analysis}

    def _risk_analysis(self, state: ContractComparisonState) -> ContractComparisonState:
        """
        Perform risk analysis on the documents.

        Args:
            state: The current state

        Returns:
            The updated state
        """
        doc1 = state["doc1_content"]
        doc2 = state["doc2_content"]
        structural_comparison = state["structural_comparison"]
        semantic_comparison = state["semantic_comparison"]
        final_comparison = state["final_comparison"]

        # Convert to string if they are dictionaries
        structural_str = json.dumps(structural_comparison) if isinstance(structural_comparison, dict) else str(structural_comparison)
        semantic_str = json.dumps(semantic_comparison) if isinstance(semantic_comparison, dict) else str(semantic_comparison)
        final_str = json.dumps(final_comparison) if isinstance(final_comparison, dict) else str(final_comparison)

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
            "structural_comparison": structural_str,
            "semantic_comparison": semantic_str,
            "final_comparison": final_str
        })

        # Parse the result
        try:
            # Check if the result contains a JSON code block
            if "```json" in risk_analysis_result:
                # Extract the JSON part
                json_part = risk_analysis_result.split("```json")[1].split("```")[0].strip()
                risk_analysis = json.loads(json_part)
            else:
                risk_analysis = json.loads(risk_analysis_result)
        except json.JSONDecodeError:
            risk_analysis = {"error": "Failed to parse risk analysis result", "raw_result": risk_analysis_result}

        # Update the state
        return {**state, "risk_analysis": risk_analysis}

    def _summary_generation(self, state: ContractComparisonState) -> ContractComparisonState:
        """
        Generate a summary of the changes and risks.

        Args:
            state: The current state

        Returns:
            The updated state
        """
        final_comparison = state["final_comparison"]
        risk_analysis = state["risk_analysis"]

        # Convert to string if they are dictionaries
        final_str = json.dumps(final_comparison) if isinstance(final_comparison, dict) else str(final_comparison)
        risk_analysis_str = json.dumps(risk_analysis) if isinstance(risk_analysis, dict) else str(risk_analysis)

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
            "final_comparison": final_str,
            "risk_analysis": risk_analysis_str
        })

        # Update the state
        return {**state, "summary": summary}

    def run(self, doc1_content: str, doc2_content: str) -> Dict[str, Any]:
        """
        Run the contract comparison workflow.

        Args:
            doc1_content: Content of the first document
            doc2_content: Content of the second document

        Returns:
            A dictionary containing the workflow results
        """
        # Initialize the state
        initial_state = {
            "doc1_content": doc1_content,
            "doc2_content": doc2_content,
            "structural_comparison": {},
            "semantic_comparison": {},
            "final_comparison": {},
            "risk_analysis": {},
            "summary": ""
        }

        # Run the workflow
        result = self.graph.invoke(initial_state)

        return result
