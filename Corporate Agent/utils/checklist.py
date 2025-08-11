def check_required_docs(
    detected_docs: list[str],
    process: str = "incorporation",
    checklist: dict = None,
    documents: list[dict] = None
) -> dict:
    """
    Check required documents for a given process with fuzzy matching on types & filenames.
    """

    # Mapping of formal document names to their known variations
    document_mapping = {
        "Articles of Association": ["articles of association", "aoa"],
        "Memorandum of Association": ["memorandum of association", "moa", "mou"],
        "Board Resolution": ["board resolution templates", "board resolution"],
        "Shareholder Resolution": ["shareholder resolution templates", "shareholder resolution"],
        "Incorporation Form": ["incorporation application form", "incorporation form"],
        "UBO Form": ["ubo declaration form", "ubo form"],
        "Register": ["register of members and directors", "register"],
        "Address Notice": ["change of registered address notice", "address notice"]
    }

    # Default required docs for each process
    default_checklists = {
        "incorporation": list(document_mapping.keys())
    }

    process_type = (process or "incorporation").lower()

    # Use checklist-provided docs if given, else default
    if checklist and isinstance(checklist, dict):
        required_docs = checklist.get("required_documents", default_checklists.get(process_type, []))
    else:
        required_docs = default_checklists.get(process_type, [])

    # Gather all uploaded doc types (normalized to lowercase)
    uploaded_from_detected = set([d.lower() for d in (detected_docs or []) if d])
    uploaded_from_documents = set()

    if documents:
        for d in documents:
            dtype = (d.get("type") or "").lower()
            fname = (d.get("filename") or "").lower()
            if dtype and dtype != "unknown":
                uploaded_from_documents.add(dtype)
            elif fname:  # fallback to filename if type is unknown
                uploaded_from_documents.add(fname)

    uploaded_all = list(uploaded_from_detected.union(uploaded_from_documents))

    # Helper to check if a required doc is found
    def doc_found(required_label: str) -> bool:
        variations = document_mapping.get(required_label, [required_label])
        variations = [v.lower() for v in variations]
        return any(
            any(var in uploaded for var in variations)
            for uploaded in uploaded_all
        )

    # Find missing docs
    missing_documents = [doc for doc in required_docs if not doc_found(doc)]

    # Create checklist status list
    status_list = [
        f"{doc} ✓" if doc not in missing_documents else doc
        for doc in required_docs
    ]

    # Optional issues list
    issues = []

    if checklist and documents:
        allowed = set([a.lower() for a in checklist.get("allowed_document_types", [])])
        if allowed:
            for d in documents:
                dtype = (d.get("type") or "unknown").lower()
                if dtype not in allowed:
                    issues.append({
                        "document": d.get("filename", "Unknown"),
                        "section": "Document Type",
                        "description": f"Invalid document type: {dtype}",
                        "severity": "high",
                        "suggestion": f'Upload a valid document type: {", ".join(allowed)}',
                        "reference": "ADGM document requirements"
                    })

        min_len = int(checklist.get("minimum_content_length", 100))
        for d in documents:
            content = (d.get("content") or "")
            if len(content) < min_len:
                issues.append({
                    "document": d.get("filename", "Unknown"),
                    "section": "Content",
                    "description": f"Document content too short ({len(content)} characters)",
                    "severity": "medium",
                    "suggestion": f"Ensure document has at least {min_len} characters",
                    "reference": "ADGM content requirements"
                })

        required_sections = checklist.get("required_sections", {})
        if isinstance(required_sections, dict) and required_sections:
            for d in documents:
                content_lc = (d.get("content") or "").lower()
                for section, requirements in required_sections.items():
                    if section and section.lower() not in content_lc:
                        issues.append({
                            "document": d.get("filename", "Unknown"),
                            "section": section,
                            "description": f"Missing required section: {section}",
                            "severity": "high",
                            "suggestion": f"Add the {section} section as per ADGM requirements",
                            "reference": (requirements or {}).get("reference", "ADGM regulations")
                        })

    compliance_score = max(0, 100 - (len(missing_documents) * 20) - (len(issues) * 10))
    overall_status = "complete" if not missing_documents else "incomplete"

    return {
        "process": process,
        "status": overall_status,
        "required_docs": required_docs,
        "uploaded_docs": uploaded_all,
        "missing_docs": missing_documents,
        "checklist": status_list,
        "total_documents": len(uploaded_all),
        "issues": issues,
        "process_type": process_type,
        "compliance_score": compliance_score
    }
