import re

def detect_red_flags(text: str, doc_type: str = "Unknown") -> list:
    """
    Basic heuristics to detect simple 'red flags' in a document.
    Returns list of dicts with issue/suggestion.
    """
    flags = []
    if not text:
        return flags

    t = text.lower()

    # example heuristics
    if "indemnity" in t and "limit" not in t:
        flags.append({
            "issue": "Uncapped indemnity clause",
            "suggestion": "Consider adding a monetary cap to indemnity clauses where appropriate."
        })

    # check for governing law presence
    if "governing law" not in t and "governed by" not in t:
        flags.append({
            "issue": "Missing governing law clause",
            "suggestion": "Add a governing law clause specifying the applicable jurisdiction."
        })

    # check for termination notice period
    if "termination" in t and not re.search(r'notice\s+period', t):
        flags.append({
            "issue": "Termination clause without clear notice period",
            "suggestion": "Specify notice period and termination conditions."
        })

    # short doc
    if len(t) < 200:
        flags.append({
            "issue": "Very short document",
            "suggestion": "Document content seems short; verify completeness."
        })

    return flags
