
def check_required_docs(detected_docs: list[str], process: str = "incorporation") -> dict:
    """
    Checks if required documents for a specific ADGM process are uploaded.

    Args:
        detected_docs (list): List of document types detected (e.g., from type_detector)
        process (str): Type of legal process (default is 'incorporation')

    Returns:
        dict: {
            "process": str,
            "status": "complete" | "incomplete",
            "required_docs": [...],
            "uploaded_docs": [...],
            "missing_docs": [...]
        }
    """

    checklists = {
        "incorporation": [
            "Articles of Association",
            "Memorandum of Association",
            "UBO Form",
            "Board Resolution",
            "Employment Contract"
        ],
        "annual_compliance": [
            "Annual Accounts",
            "Balance Sheet",
            "Board Resolution"
        ]
        # You can add more legal processes here later
    }

    required = checklists.get(process.lower(), [])
    uploaded = list(set(detected_docs))  # remove duplicates
    missing = [doc for doc in required if doc not in uploaded]

    return {
        "process": process,
        "status": "complete" if not missing else "incomplete",
        "required_docs": required,
        "uploaded_docs": uploaded,
        "missing_docs": missing
    }
