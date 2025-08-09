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

# Ensure temp directory exists
os.makedirs("temp", exist_ok=True)

st.set_page_config(page_title="Corporate Agent", layout="wide")
st.title("📄 Corporate Agent – ADGM Legal Document Reviewer")

uploaded_files = st.file_uploader(
    "Upload one or more .docx files", type=["docx"], accept_multiple_files=True
)

if uploaded_files:
    all_docs = []
    doc_types = []

    # Process uploaded files
    for i, file in enumerate(uploaded_files):
        temp_path = os.path.join("temp", file.name)
        with open(temp_path, "wb") as f:
            f.write(file.getbuffer())

        text = extract_text_from_docx(temp_path)
        doc_type = detect_document_type(text)
        flags = detect_red_flags(text, doc_type)
        updated_path = comment_on_docx(temp_path, flags)

        all_docs.append({
            "filename": file.name,
            "type": doc_type,
            "flags": flags,
            "updated_path": updated_path
        })
        doc_types.append(doc_type)

    # Checklist verification after processing all files
    checklist_result = check_required_docs(doc_types)

    st.subheader("📋 Checklist Verification")
    st.write(checklist_result)

    # Generate and display summaries for each document, with download buttons
    st.subheader("🧾 Document Summaries")
    for i, doc in enumerate(all_docs):
        summary_path = generate_summary_json(
            filename=doc['filename'],           # <-- Added filename here
            doc_type=doc['type'],
            checklist_result=checklist_result,
            red_flags=doc['flags'],
            save_path="outputs"
        )
        with open(summary_path, "r") as f:
            summary_json = json.load(f)

        st.markdown(f"### 📑 {doc['filename']} ({doc['type']})")
        st.write("🚩 Issues Found:")
        for flag in doc["flags"]:
            st.warning(f"{flag['issue']} – Suggestion: {flag['suggestion']}")

        st.download_button(
            "⬇️ Download Reviewed Document",
            data=open(doc["updated_path"], "rb").read(),
            file_name=doc["filename"],
            key=f"download_doc_{i}"
        )

        st.subheader("Summary JSON")
        st.json(summary_json)
        st.download_button(
            "⬇️ Download Summary JSON",
            data=json.dumps(summary_json, indent=4),
            file_name=os.path.basename(summary_path),
            key=f"download_summary_{i}"
        )

# Optional Q&A Interface
st.divider()
st.subheader("💬 Ask your Legal Question or Doubt (from ADGM laws)")

question = st.text_input("Ask your question here...")
if question:
    response = query_rag(question)
    st.success(response)
