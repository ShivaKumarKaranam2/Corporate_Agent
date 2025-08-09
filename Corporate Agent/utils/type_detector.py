import re

def detect_document_type(text: str, filename: str = "") -> str:
    """
    Detects the type of legal document based on its text content or filename.

    Args:
        text (str): Extracted text from the document
        filename (str): Optional filename for heuristic support

    Returns:
        str: Document type (e.g., 'Articles of Association', 'MoA', 'UBO Form', etc.)
    """

    # Normalize for easier matching
    text = text.lower()
    filename = filename.lower()

    # Priority: Filename hints
    if "articles" in filename or "aoa" in filename:
        return "Articles of Association"
    elif "mou" in filename or "moa" in filename or "memorandum" in filename:
        return "Memorandum of Association"
    elif "ubo" in filename or "ownership" in filename:
        return "UBO Form"
    elif "resolution" in filename:
        return "Board Resolution"
    elif "employment" in filename:
        return "Employment Contract"
    elif "balance" in filename:
        return "Balance Sheet"
    elif "accounts" in filename:
        return "Annual Accounts"
    
    # Fallback: Text-based rules
    if "articles of association" in text:
        return "Articles of Association"
    elif "memorandum of association" in text:
        return "Memorandum of Association"
    elif "beneficial owner" in text or "ultimate beneficial owner" in text:
        return "UBO Form"
    elif "board resolution" in text:
        return "Board Resolution"
    elif "employment contract" in text or "terms of employment" in text:
        return "Employment Contract"
    elif "balance sheet" in text:
        return "Balance Sheet"
    elif "statement of financial position" in text:
        return "Annual Accounts"
    
    return "Unknown"
