from docx import Document
import re

def extract_text_from_docx(file_path: str) -> str:
    """
    Extracts and cleans text from a .docx file.

    Args:
        file_path (str): Path to the .docx file

    Returns:
        str: Cleaned text content
    """
    try:
        doc = Document(file_path)
        full_text = []

        for para in doc.paragraphs:
            if para.text.strip():  # Skip empty lines
                full_text.append(para.text.strip())

        raw_text = "\n".join(full_text)
        cleaned_text = clean_text(raw_text)

        return cleaned_text
    
    except Exception as e:
        print(f"[parser.py] Error reading {file_path}: {e}")
        return ""

def clean_text(text: str) -> str:
    """
    Cleans extracted text by removing extra whitespace, line breaks, tabs, etc.

    Args:
        text (str): Raw extracted text

    Returns:
        str: Cleaned text
    """
    text = re.sub(r'\n+', '\n', text)  # Remove excessive newlines
    text = re.sub(r'\t+', ' ', text)  # Replace tabs with space
    text = re.sub(r' +', ' ', text)   # Collapse multiple spaces
    return text.strip()
