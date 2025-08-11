import streamlit as st
import os
import json
from utils.parser import extract_text_from_docx
from utils.type_detector import detect_document_type
from utils.checklist import check_required_docs
from utils.redflags import detect_red_flags
from utils.commenter import comment_on_docx
from utils.summarizer import generate_summary_json
from utils.rag_engine import query_rag

# Ensure directories exist
os.makedirs("temp", exist_ok=True)
os.makedirs("outputs", exist_ok=True)

st.set_page_config(page_title="Corporate Agent", layout="wide")
st.title("📄 Corporate Agent – ADGM Legal Document Reviewer")

uploaded_files = st.file_uploader(
    "Upload one or more .docx files", type=["docx"], accept_multiple_files=True
)

if uploaded_files:
    all_docs = []
    doc_types = []

    with st.spinner("Processing uploaded documents..."):
        for uploaded in uploaded_files:
            temp_path = os.path.join("temp", uploaded.name)
            with open(temp_path, "wb") as f:
                f.write(uploaded.getbuffer())

            # extract text
            text = extract_text_from_docx(temp_path) or ""
            doc_type = detect_document_type(text) or "Unknown"
            flags = detect_red_flags(text, doc_type) or []

            # attempt to add comments (safe implementation)
            try:
                updated_path = comment_on_docx(temp_path, flags)
            except Exception as e:
                st.error(f"Failed to add comments to {uploaded.name}: {e}")
                updated_path = temp_path

            all_docs.append({
                "filename": uploaded.name,
                "type": doc_type,
                "flags": flags,
                "updated_path": updated_path,
                "content": text
            })
            doc_types.append(doc_type)

    # Checklist verification
    checklist_result = check_required_docs(doc_types, "incorporation", documents=all_docs)

    st.subheader("📋 Checklist Verification")
    st.write({
        "status": checklist_result.get("status"),
        "process": checklist_result.get("process"),
        "required_docs": checklist_result.get("required_docs"),
        "uploaded_docs": checklist_result.get("uploaded_docs"),
        "missing_docs": checklist_result.get("missing_docs"),
        "checklist": checklist_result.get("checklist"),
        "compliance_score": checklist_result.get("compliance_score"),
        "issues": checklist_result.get("issues"),
    })

    # Summaries
    st.subheader("🧾 Document Summaries")
    for i, doc in enumerate(all_docs):
        try:
            summary_path = generate_summary_json(
                filename=doc["filename"],
                doc_type=doc["type"],
                checklist_result=checklist_result,
                red_flags=doc["flags"],
                save_path="outputs",
                content=doc.get("content", "")
            )
        except TypeError:
            summary_path = generate_summary_json(
                doc["filename"], doc["type"], checklist_result, doc["flags"], "outputs", doc.get("content", "")
            )

        try:
            with open(summary_path, "r", encoding="utf-8") as f:
                summary_json = json.load(f)
        except Exception:
            summary_json = {"error": "Failed to load summary JSON."}

        st.markdown(f"### 📑 {doc['filename']} ({doc['type']})")
        if doc["flags"]:
            st.write("🚩 Issues Found:")
            for flag in doc["flags"]:
                issue_txt = flag.get("issue") or flag.get("description") or "Issue"
                suggestion_txt = flag.get("suggestion") or "No suggestion provided."
                st.warning(f"{issue_txt} – Suggestion: {suggestion_txt}")
        else:
            st.info("No red flags detected.")

        try:
            with open(doc["updated_path"], "rb") as fh:
                reviewed_bytes = fh.read()
            reviewed_name = os.path.splitext(doc["filename"])[0] + "_reviewed.docx"
            st.download_button(
                "⬇️ Download Reviewed Document",
                data=reviewed_bytes,
                file_name=reviewed_name,
                key=f"download_doc_{i}",
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            )
        except Exception as e:
            st.error(f"Unable to prepare reviewed document for download: {e}")

        st.subheader("Summary JSON")
        st.json(summary_json)
        st.download_button(
            "⬇️ Download Summary JSON",
            data=json.dumps(summary_json, ensure_ascii=False, indent=4),
            file_name=os.path.basename(summary_path),
            key=f"download_summary_{i}",
            mime="application/json",
        )

    # RAG
    st.subheader("🤖 RAG Engine (local)")
    query = st.text_input("Ask a question about the uploaded docs (e.g. 'Does the AoA mention quorum?'):")

    if query:
        response = query_rag(query)
        st.success(response)
else:
    st.info("Upload one or more .docx files to start the review.")
