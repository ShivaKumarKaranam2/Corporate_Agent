def check_required_docs(detected_docs: list[str], process: str = "incorporation") -> dict:
 

    document_mapping = {
        "Articles of Association": ["Articles of Association", "AoA"],
        "Memorandum of Association": ["Memorandum of Association", "MoA", "MoU"],
        "Board Resolution": ["Board Resolution Templates", "Board Resolution"],
        "Shareholder Resolution": ["Shareholder Resolution Templates"],
        "Incorporation Form": ["Incorporation Application Form"],
        "UBO Form": ["UBO Declaration Form", "UBO Form"],
        "Register": ["Register of Members and Directors"],
        "Address Notice": ["Change of Registered Address Notice"]
    }

    checklists = {
        "incorporation": list(document_mapping.keys())
        # Add other processes as needed
    }

    required = checklists.get(process.lower(), [])
    uploaded = list(set(detected_docs))
    
    # Check for document matches including variations
    status_list = []
    missing = []
    
    for doc in required:
        variations = document_mapping[doc]
        found = any(var in uploaded for var in variations)
        status = f"{doc} ✓" if found else f"{doc}"
        status_list.append(status)
        if not found:
            missing.append(doc)

    return {
        "process": process,
        "status": "complete" if not missing else "incomplete",
        "required_docs": required,
        "uploaded_docs": uploaded,
        "missing_docs": missing,
        "checklist": status_list
    }
