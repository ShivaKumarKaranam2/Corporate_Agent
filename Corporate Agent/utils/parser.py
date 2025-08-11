from docx import Document
import re
from typing import List

def extract_text_from_docx(file_path: str) -> str:
    """Args:
        file_path (str): Path to the .docx file

    Returns:
        str: Cleaned text content"""
    try:
        doc = Document(file_path)

        paragraphs: List[str] = []
        for p in doc.paragraphs:
            text = (p.text or "").strip()
            if not text:
                continue
            paragraphs.append(text)

    
        raw_text = "\n".join(paragraphs)

        raw_text = _ensure_section_line_breaks(raw_text)

        return clean_text(raw_text)

    except Exception as e:
        print(f"[parser.py] Error reading {file_path}: {e}")
        return ""


def clean_text(text: str) -> str:
    """
    Args:
    text (str): Raw extracted text

    Returns:
        str: Cleaned text
    """
    text = text.replace("\r\n", "\n").replace("\r", "\n")

    
    text = re.sub(r"\n{3,}", "\n\n", text)

    text = re.sub(r"\t+", " ", text)


    text = re.sub(r"[ \u00A0]{2,}", " ", text)  # handle non-breaking spaces too


    text = "\n".join(line.strip() for line in text.split("\n"))


    text = re.sub(r"\n{3,}", "\n\n", text)

    return text.strip()


def _ensure_section_line_breaks(text: str) -> str:

    section_pattern = re.compile(r'^\d+\.\s+[A-Z]') 
    numbered_only = re.compile(r'^\d+\.$')  
    
    lines = text.split('\n')
    out_lines = []
    
    for i, line in enumerate(lines):
        l = line.strip()
        if not l:
            out_lines.append(line)
            continue
            
        is_upper = (l.isupper() and len(l) > 1 and any(c.isalpha() for c in l))
        ends_colon = l.endswith(":")
        is_numbered_title = bool(section_pattern.match(l)) or bool(numbered_only.match(l))

        if is_upper or ends_colon or is_numbered_title:
            # Ensure it is separated clearly; add line breaks before section headers
            if i > 0 and out_lines and out_lines[-1].strip():
                out_lines.append("")  # Add blank line before section
            out_lines.append(line)
        else:
            out_lines.append(line)

    return "\n".join(out_lines)
