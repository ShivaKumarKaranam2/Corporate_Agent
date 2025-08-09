
from docx import Document
import os
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
import uuid

def comment_on_docx(file_path: str, flags: list[dict]) -> str:
    """
    Inserts comments into a .docx file based on detected red flags.

    Args:
        file_path (str): Path to the original .docx file
        flags (list): List of red flags with 'quote' and 'suggestion'

    Returns:
        str: Path to the updated .docx file with comments
    """

    doc = Document(file_path)
    comments_added = 0

    for para in doc.paragraphs:
        for flag in flags:
            quote = flag.get("quote")
            suggestion = flag.get("suggestion")
            if quote and quote.lower() in para.text.lower():
                # Insert comment (using OXML)
                _add_comment_to_paragraph(para, suggestion)
                comments_added += 1
                break  # One comment per paragraph max

    reviewed_path = file_path.replace(".docx", "_reviewed.docx")
    doc.save(reviewed_path)

    print(f"[commenter.py] {comments_added} comments added to {os.path.basename(file_path)}")

    return reviewed_path

def _add_comment_to_paragraph(paragraph, comment_text):
    """
    Internal helper to insert comment into a paragraph (OXML hack).
    """

    comment_id = str(uuid.uuid4().int)[:6]

    # Create the comment range start
    start = OxmlElement('w:commentRangeStart')
    start.set(qn('w:id'), comment_id)
    paragraph._p.insert(0, start)

    # Create the comment range end
    end = OxmlElement('w:commentRangeEnd')
    end.set(qn('w:id'), comment_id)
    paragraph._p.append(end)

    # Create the actual comment
    comment = OxmlElement('w:comment')
    comment.set(qn('w:author'), 'CorporateAgent')
    comment.set(qn('w:date'), '2025-08-08T00:00:00Z')
    comment.set(qn('w:id'), comment_id)
    
    p = OxmlElement('w:p')
    r = OxmlElement('w:r')
    t = OxmlElement('w:t')
    t.text = comment_text

    r.append(t)
    p.append(r)
    comment.append(p)


    paragraph.text += " 🔍"
