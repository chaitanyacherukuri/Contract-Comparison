"""
Document Loader Module

This module handles loading documents from various file formats.
"""

import os
from typing import Dict, Any, Optional
from pypdf import PdfReader
from docx import Document


class DocumentLoader:
    """
    A class for loading documents from various file formats.
    """
    
    def load_document(self, file_path: str) -> str:
        """
        Load a document from a file path.
        
        Args:
            file_path: Path to the document file
            
        Returns:
            The text content of the document
        
        Raises:
            ValueError: If the file format is not supported
        """
        _, file_extension = os.path.splitext(file_path)
        file_extension = file_extension.lower()
        
        if file_extension == '.pdf':
            return self._load_pdf(file_path)
        elif file_extension == '.docx':
            return self._load_docx(file_path)
        elif file_extension == '.txt':
            return self._load_txt(file_path)
        else:
            raise ValueError(f"Unsupported file format: {file_extension}")
    
    def _load_pdf(self, file_path: str) -> str:
        """Load text from a PDF file."""
        reader = PdfReader(file_path)
        text = ""
        for page in reader.pages:
            text += page.extract_text() + "\n"
        return text
    
    def _load_docx(self, file_path: str) -> str:
        """Load text from a DOCX file."""
        doc = Document(file_path)
        text = ""
        for paragraph in doc.paragraphs:
            text += paragraph.text + "\n"
        return text
    
    def _load_txt(self, file_path: str) -> str:
        """Load text from a plain text file."""
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
