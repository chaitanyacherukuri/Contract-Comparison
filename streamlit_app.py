#!/usr/bin/env python3
"""
Contract Comparison Streamlit Web UI

This application provides a web interface for comparing two legal documents and
generating a detailed summary of changes and potential risk areas using LangGraph and LLMs.
"""

import os
import tempfile
import io
import streamlit as st
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from src.document_loaders.loader import DocumentLoader
from src.workflow.contract_comparison_workflow import ContractComparisonWorkflow

# Note: We're using Streamlit secrets instead of environment variables
# for deployment on Streamlit Cloud

# Set page configuration
st.set_page_config(
    page_title="Contract Comparison",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main {
        padding: 2rem;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 2rem;
    }
    .stTabs [data-baseweb="tab"] {
        height: 4rem;
        white-space: pre-wrap;
        background-color: #f0f2f6;
        border-radius: 4px;
        padding: 1rem;
        font-weight: 600;
    }
    .stTabs [aria-selected="true"] {
        background-color: #e6f0ff;
    }
    .risk-high {
        color: #dc3545;
        font-weight: bold;
    }
    .risk-medium {
        color: #fd7e14;
        font-weight: bold;
    }
    .risk-low {
        color: #28a745;
        font-weight: bold;
    }
    .document-container {
        border: 1px solid #e6e6e6;
        border-radius: 5px;
        padding: 1rem;
        background-color: #f9f9f9;
        height: 400px;
        overflow-y: auto;
    }
</style>
""", unsafe_allow_html=True)

def check_api_key():
    """Check if the GROQ API key is set in Streamlit secrets or prompt the user for it."""
    # Try to get the API key from Streamlit secrets
    try:
        api_key = st.secrets["api_keys"]["groq"]
        if api_key and api_key != "your_groq_api_key_here":
            # Set the environment variable for any libraries that use it
            os.environ["GROQ_API_KEY"] = api_key
            return True
    except (KeyError, TypeError):
        # If the key is not in secrets or has the default value, continue to the input prompt
        pass

    # If we get here, we need to ask the user for the API key
    st.error("⚠️ GROQ API key is not set in Streamlit secrets. Please enter it below.")
    api_key = st.text_input("Enter your GROQ API key:", type="password")
    if api_key:
        os.environ["GROQ_API_KEY"] = api_key
        return True
    return False

def save_uploaded_file(uploaded_file):
    """Save an uploaded file to a temporary file and return the path."""
    with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(uploaded_file.name)[1]) as tmp:
        tmp.write(uploaded_file.getvalue())
        return tmp.name

def format_comparison_results(result):
    """Format the comparison results for display."""
    summary = result.get("summary", "")

    # Extract different sections from the summary
    sections = {}
    current_section = "Executive Summary"
    sections[current_section] = []

    for line in summary.split('\n'):
        if line.startswith('##'):
            current_section = line.replace('#', '').strip()
            sections[current_section] = []
        else:
            sections[current_section].append(line)

    return sections

def create_risk_table(risk_analysis):
    """Create a formatted risk table from the risk analysis."""
    risks = risk_analysis.get("risks", [])
    if not risks:
        return "No risks identified."

    # Create a table header
    table = """
    | Risk | Severity | Description | Mitigation |
    | ---- | -------- | ----------- | ---------- |
    """

    # Add each risk to the table
    for risk in risks:
        severity = risk.get("severity", "").lower()
        severity_class = f"risk-{severity}" if severity in ["high", "medium", "low"] else ""

        table += f"| {risk.get('category', '')} | <span class='{severity_class}'>{risk.get('severity', '')}</span> | {risk.get('description', '')} | {risk.get('mitigation', '')} |\n"

    return table

def generate_pdf_report(summary):
    """Generate a PDF report from the summary markdown."""
    # Create a buffer for the PDF
    buffer = io.BytesIO()

    # Create the PDF document
    doc = SimpleDocTemplate(buffer, pagesize=letter,
                           rightMargin=72, leftMargin=72,
                           topMargin=72, bottomMargin=72)

    # Get styles
    styles = getSampleStyleSheet()
    title_style = styles['Title']
    heading_style = styles['Heading2']
    normal_style = styles['Normal']

    # Create custom styles
    section_title_style = ParagraphStyle(
        'SectionTitle',
        parent=styles['Heading1'],
        fontSize=16,
        textColor=colors.blue,
        spaceAfter=12
    )

    # Create the content elements
    elements = []

    # Parse the markdown content
    lines = summary.split('\n')

    # Add the title (first line)
    if lines:
        title_text = lines[0].replace('#', '').strip()
        elements.append(Paragraph(title_text, title_style))
        elements.append(Spacer(1, 12))

    # Process the rest of the content
    current_section = None
    section_content = []

    for line in lines[1:]:
        # Check if this is a section heading
        if line.startswith('##'):
            # If we have content from a previous section, add it
            if current_section and section_content:
                elements.append(Paragraph(current_section, section_title_style))

                # Add the section content
                for content in section_content:
                    if content.strip():
                        elements.append(Paragraph(content, normal_style))
                        elements.append(Spacer(1, 6))

                # Add a spacer between sections
                elements.append(Spacer(1, 12))

                # Reset for the new section
                section_content = []

            # Set the new section title
            current_section = line.replace('#', '').strip()

        # Check if this is a subsection heading
        elif line.startswith('#'):
            # Add the subsection heading
            heading_text = line.replace('#', '').strip()
            elements.append(Paragraph(heading_text, heading_style))

        # Skip horizontal lines
        elif line.strip() == '---' or line.strip() == '---------------':
            continue

        # Regular content
        else:
            if current_section:
                section_content.append(line)

    # Add the last section if there is one
    if current_section and section_content:
        elements.append(Paragraph(current_section, section_title_style))

        # Add the section content
        for content in section_content:
            if content.strip():
                elements.append(Paragraph(content, normal_style))
                elements.append(Spacer(1, 6))

    try:
        # Build the PDF
        doc.build(elements)

        # Get the PDF data
        pdf_data = buffer.getvalue()
        buffer.close()

        return pdf_data
    except Exception as e:
        # If PDF generation fails, return None
        print(f"Error generating PDF: {e}")
        return None

def main():
    """Main function for the Streamlit app."""
    st.title("📄 AI-Powered Contract Comparison")
    st.markdown("""
    Upload two versions of a contract to compare them, identify changes and potential risks.
    The tool will analyze structural and semantic differences and provide a detailed report.
    """)

    # Check if API key is set
    if not check_api_key():
        st.warning("Please set your GROQ API key to continue.")
        return

    # Set default values for session state
    if "show_raw_json" not in st.session_state:
        st.session_state.show_raw_json = False

    # File upload section
    st.header("Document Upload")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Original Document")
        doc1 = st.file_uploader("Upload the original document",
                               type=["pdf", "docx", "txt"],
                               help="Supported formats: PDF, DOCX, TXT")

    with col2:
        st.subheader("Modified Document")
        doc2 = st.file_uploader("Upload the modified document",
                               type=["pdf", "docx", "txt"],
                               help="Supported formats: PDF, DOCX, TXT")

    # Sample documents option
    use_samples = st.checkbox("Use sample documents instead")

    # Sample document format selection (only shown when use_samples is checked)
    sample_format = None
    if use_samples:
        sample_format = st.radio(
            "Select sample document format:",
            ["TXT", "PDF", "DOCX"],
            horizontal=True,
            help="Choose which format of sample documents to use for comparison"
        )

    # Process button
    process_clicked = st.button("Compare Documents", type="primary", disabled=(not doc1 or not doc2) and not use_samples)

    # Process documents
    if process_clicked:
        try:
            with st.spinner("Processing documents... This may take a minute."):
                loader = DocumentLoader()

                if use_samples:
                    # Use sample documents with the selected format
                    file_ext = sample_format.lower()
                    doc1_path = f"data/sample_documents/contract_v1.{file_ext}"
                    doc2_path = f"data/sample_documents/contract_v2.{file_ext}"
                    doc1_content = loader.load_document(doc1_path)
                    doc2_content = loader.load_document(doc2_path)
                    doc1_name = f"contract_v1.{file_ext}"
                    doc2_name = f"contract_v2.{file_ext}"
                else:
                    # Save uploaded files to temporary files
                    doc1_path = save_uploaded_file(doc1)
                    doc2_path = save_uploaded_file(doc2)

                    # Load documents
                    doc1_content = loader.load_document(doc1_path)
                    doc2_content = loader.load_document(doc2_path)
                    doc1_name = doc1.name
                    doc2_name = doc2.name

                # Run the workflow
                workflow = ContractComparisonWorkflow()
                result = workflow.run(doc1_content, doc2_content)

                # Store the result in session state
                st.session_state.comparison_result = result
                st.session_state.doc1_content = doc1_content
                st.session_state.doc2_content = doc2_content
                st.session_state.doc1_name = doc1_name
                st.session_state.doc2_name = doc2_name

                # Clean up temporary files if not using samples
                if not use_samples:
                    os.unlink(doc1_path)
                    os.unlink(doc2_path)

                st.success("Comparison completed successfully!")

        except Exception as e:
            st.error(f"Error processing documents: {e}")
            return

    # Display results if available
    if 'comparison_result' in st.session_state:
        st.header("Comparison Results")

        # Create tabs for different views
        tab1, tab2 = st.tabs(["Summary", "Detailed Analysis"])

        with tab1:
            # Display summary with custom formatting
            summary = st.session_state.comparison_result.get("summary", "")

            # Define the main section headings we want to separate
            main_sections = ["Executive Summary", "Detailed Changes Analysis", "Risk Assessment", "Recommendations"]

            # Process the summary to identify main sections and their content
            processed_content = []
            current_main_section = None

            for line in summary.split('\n'):
                # Check if this is a main section heading
                if line.startswith('##'):
                    section_name = line.replace('#', '').strip()

                    # If we're starting a new main section and already have content
                    if section_name in main_sections:
                        # If we already have content and are starting a new main section, add a separator
                        if processed_content and current_main_section:
                            processed_content.append("\n---\n")
                        current_main_section = section_name

                    # Add the heading (without any horizontal line after it)
                    processed_content.append(line)
                else:
                    # Skip horizontal lines that might appear after headings
                    if line.strip() == '---' or line.strip() == '---------------':
                        continue

                    # Add regular content
                    processed_content.append(line)

            # Display the processed content
            st.markdown('\n'.join(processed_content))

        with tab2:
            # Create expandable sections for each part of the analysis
            with st.expander("Structural Changes", expanded=True):
                structural_comparison = st.session_state.comparison_result.get("structural_comparison", {})

                # Create a better layout for structural changes
                col1, col2 = st.columns(2)

                # Display added sections in first column
                with col1:
                    st.subheader("Added Sections")
                    if "added_sections" in structural_comparison and structural_comparison["added_sections"]:
                        for section in structural_comparison.get("added_sections", []):
                            st.success(f"➕ {section}")
                    else:
                        st.info("No sections were added")

                # Display removed sections in second column
                with col2:
                    st.subheader("Removed Sections")
                    if "removed_sections" in structural_comparison and structural_comparison["removed_sections"]:
                        for section in structural_comparison.get("removed_sections", []):
                            st.error(f"➖ {section}")
                    else:
                        st.info("No sections were removed")

                # Display modified sections in full width
                st.subheader("Modified Sections")
                if "modified_sections" in structural_comparison and structural_comparison["modified_sections"]:
                    # Create a table-like display for modified sections
                    for i, section in enumerate(structural_comparison.get("modified_sections", [])):
                        if i % 2 == 0:
                            st.markdown(f"""
                            <div style="background-color: #f8f9fa; padding: 10px; border-radius: 5px; margin-bottom: 10px;">
                                <strong>{section}</strong>
                            </div>
                            """, unsafe_allow_html=True)
                        else:
                            st.markdown(f"""
                            <div style="background-color: #e9ecef; padding: 10px; border-radius: 5px; margin-bottom: 10px;">
                                <strong>{section}</strong>
                            </div>
                            """, unsafe_allow_html=True)
                else:
                    st.info("No sections were modified")

                # Display the raw JSON if requested
                if st.session_state.show_raw_json:
                    st.json(structural_comparison)

            with st.expander("Semantic Changes", expanded=True):
                semantic_comparison = st.session_state.comparison_result.get("semantic_comparison", {})

                # Display significant changes in a more organized way
                if "significant_changes" in semantic_comparison and semantic_comparison["significant_changes"]:
                    st.subheader("Significant Changes")

                    # Group changes by category
                    changes_by_category = {}
                    for change in semantic_comparison.get("significant_changes", []):
                        category = change.get("category", "Other")
                        if category not in changes_by_category:
                            changes_by_category[category] = []
                        changes_by_category[category].append(change)

                    # Display each category in its own section
                    for category, changes in changes_by_category.items():
                        st.markdown(f"#### {category} Changes")

                        # Create a clean list of changes
                        for i, change in enumerate(changes):
                            description = change.get("description", "")
                            impact = change.get("impact", "")

                            # Create a container for each change
                            with st.container():
                                # Add a subtle divider between changes
                                if i > 0:
                                    st.divider()

                                # Display description with bold label
                                st.markdown(f"**Description:** {description}")

                                # Display impact with bold label and emphasis
                                st.markdown(f"**Impact:** *{impact}*")
                else:
                    st.info("No significant semantic changes identified")

                # Display the raw JSON if requested
                if st.session_state.show_raw_json:
                    st.json(semantic_comparison)

            with st.expander("Risk Analysis", expanded=True):
                risk_analysis = st.session_state.comparison_result.get("risk_analysis", {})

                # Display risks as a table
                risk_table = create_risk_table(risk_analysis)
                st.markdown(risk_table, unsafe_allow_html=True)

                # Display the raw JSON if requested
                if st.session_state.show_raw_json:
                    st.json(risk_analysis)

            # Display final comparison
            with st.expander("Final Comparison", expanded=True):
                final_comparison = st.session_state.comparison_result.get("final_comparison", {})

                # Display overall assessment first
                if "overall_assessment" in final_comparison:
                    st.subheader("Overall Assessment")
                    st.info(final_comparison.get("overall_assessment", ""))

                # Display significant changes in a more organized way
                if "significant_changes" in final_comparison and final_comparison["significant_changes"]:
                    st.subheader("Significant Changes")

                    # Group changes by category
                    changes_by_category = {}
                    for change in final_comparison.get("significant_changes", []):
                        category = change.get("category", "Other")
                        if category not in changes_by_category:
                            changes_by_category[category] = []
                        changes_by_category[category].append(change)

                    # Display each category in its own section
                    for category, changes in changes_by_category.items():
                        st.markdown(f"#### {category} Changes")

                        # Create a clean list of changes
                        for i, change in enumerate(changes):
                            description = change.get("description", "")
                            impact = change.get("impact", "")

                            # Create a container for each change
                            with st.container():
                                # Add a subtle divider between changes
                                if i > 0:
                                    st.divider()

                                # Display description with bold label
                                st.markdown(f"**Description:** {description}")

                                # Display impact with bold label and emphasis
                                st.markdown(f"**Impact:** *{impact}*")

                # Display potential inconsistencies in a more readable format
                if "potential_inconsistencies" in final_comparison and final_comparison["potential_inconsistencies"]:
                    st.subheader("Potential Inconsistencies")

                    # Create a table for inconsistencies
                    inconsistency_data = []
                    for inconsistency in final_comparison.get("potential_inconsistencies", []):
                        inconsistency_data.append({
                            "Location": inconsistency.get("location", ""),
                            "Description": inconsistency.get("description", "")
                        })

                    if inconsistency_data:
                        st.table(inconsistency_data)

                # Display the raw JSON if requested
                if st.session_state.show_raw_json:
                    st.json(final_comparison)

        # Add a download button for the report below the tabs
        st.markdown("---")
        _, center_col, _ = st.columns([1, 2, 1])
        with center_col:
            # Try to generate PDF
            summary = st.session_state.comparison_result.get("summary", "")
            pdf_data = generate_pdf_report(summary)

            if pdf_data:
                # If PDF generation was successful, offer PDF download
                st.download_button(
                    label="Download Comparison Report (PDF)",
                    data=pdf_data,
                    file_name="comparison_report.pdf",
                    mime="application/pdf",
                    use_container_width=True
                )
            else:
                # Fallback to markdown if PDF generation failed
                st.download_button(
                    label="Download Comparison Report (Markdown)",
                    data=summary,
                    file_name="comparison_report.md",
                    mime="text/markdown",
                    use_container_width=True
                )

if __name__ == "__main__":
    main()
