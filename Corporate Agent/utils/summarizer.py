import json
import os
from datetime import datetime

def generate_summary_json(filename, doc_type, checklist_result, red_flags, save_path="outputs", content="")-> str:
    """
    Generates a structured summary JSON of the review result.

    Args:
        filename (str): Original document filename, used for naming output file
        doc_type (str): Detected document type
        checklist_result (dict): Output from checklist.py
        red_flags (list): Output from redflags.py
        save_path (str): Folder to save the JSON file

    Returns:
        str: Path to the saved summary JSON file
    """

    summary = {
        "document_type": doc_type,
        "checklist_status": checklist_result.get("status", "unknown"),
        "missing_documents": checklist_result.get("missing_docs", []),
        "num_red_flags": len(red_flags),
        "red_flags": []
    }

    for flag in red_flags:
        summary["red_flags"].append({
            "issue": flag.get("issue"),
            "suggestion": flag.get("suggestion"),
            "quote": flag.get("quote")
        })

    # Ensure output directory exists
    os.makedirs(save_path, exist_ok=True)

    safe_name = filename.lower().replace(' ', '_').replace('.docx', '')
    output_filename = f"{safe_name}_review_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    output_file = os.path.join(save_path, output_filename)

    with open(output_file, "w") as f:
        json.dump(summary, f, indent=4)

    print(f"[summarizer.py] Summary saved to {output_file}")
    return output_file
