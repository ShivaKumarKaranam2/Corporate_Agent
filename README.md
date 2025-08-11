# 📄 Corporate Agent – ADGM Legal Document Reviewer

A Streamlit-based web application designed to assist legal professionals in reviewing Abu Dhabi Global Market (ADGM) related legal documents. The app automates document type detection, red flag identification, checklist verification, document annotation, and provides an AI-powered interactive Q&A interface powered by Google Gemini generative AI.

---
## Live Demo

Experience the Corporate Agent app live and interactively here:  
👉 [https://corporateagent-rjbvbwej9mvdzv6qfakidb.streamlit.app/](https://corporateagent-rjbvbwej9mvdzv6qfakidb.streamlit.app/)

---

## Table of Contents

- [Project Overview](#project-overview)
- [Features](#features)
- [Implementation Details](#implementation-details)
- [Tech Stack](#tech-stack)
- [Setup Instructions](#setup-instructions)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Environment Variables & Secrets](#environment-variables--secrets)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)

---

## Project Overview

Legal document review is often tedious and requires subject matter expertise. This application streamlines the review process for ADGM legal documents by automating:

- Document type detection from uploaded `.docx` files
- Identification of potential legal "red flags" with suggestions
- Validation against a checklist of required documents
- Annotating documents with comments highlighting issues
- Providing an interactive AI-powered Q&A interface to clarify ADGM law queries

---

## Features

- Upload multiple `.docx` files simultaneously for batch processing.
- Extract document text and detect document type using custom logic.
- Detect legal red flags with actionable suggestions.
- Generate downloadable annotated documents and JSON summaries.
- Interactive legal Q&A powered by Google Gemini API.
- Persistent temporary and output directories for auditability.

---

## Implementation Details

- **Document Upload & Parsing**: Using Streamlit's file uploader and `python-docx` to extract text.
- **Document Type Detection**: Rule-based or ML-based detection implemented in `type_detector.py`.
- **Red Flag Detection**: Custom heuristics or pattern matching implemented in `redflags.py`.
- **Checklist Validation**: Ensures submission completeness as per ADGM requirements (`checklist.py`).
- **Document Annotation**: Comments added to `.docx` files via `commenter.py`.
- **Summary Generation**: Produces structured JSON summaries for each document (`summarizer.py`).
- **AI Q&A**: Queries Google Gemini model with user input, enhanced by Retrieval-Augmented Generation (RAG) using FAISS vector store (`rag_engine.py`).

---

## Tech Stack

- **Frontend**: Streamlit (Python)
- **Document Processing**: `python-docx`, custom parsers
- **AI Backend**: Google Gemini API (Generative Language Model)
- **RAG Vector Store**: FAISS with HuggingFace Sentence Transformers embeddings
- **Version Control**: Git & GitHub

---

## Setup Instructions

### Prerequisites

- Python 3.8+
- `pip` package manager
- Google Cloud Project with Generative Language API enabled
- Valid Google API Key with access to Gemini model

### Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/2CentsCapitalHR/ai-engineer-task-ShivaKumarKaranam2.git
    cd ai-engineer-task-ShivaKumarKaranam2
    ```

2. Create and activate a virtual environment:
    ```bash
    python -m venv my_env
    # Windows
    my_env\Scripts\activate
    # macOS/Linux
    source my_env/bin/activate
    ```

3. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```
---

## Usage

1. Run the Streamlit app:
    ```bash
    streamlit run app.py
    ```

2. Upload one or multiple `.docx` legal documents for review.

3. View detected document types, red flags with suggestions, and download annotated documents and JSON summaries.

4. Use the Q&A section to ask legal questions related to ADGM laws, powered by Google Gemini.

---

# 📄 Corporate Agent – ADGM Legal Document Reviewer

Welcome to the Corporate Agent project! Below are some screenshots showcasing the app.

---

## Screenshots

### 1. Home Page / Upload Interface

![Upload Interface](Corporate%20Agent/images/Screenshot%202025-08-09%20132533.png)

---

### 2. Document Processing View

![Document Processing](Corporate%20Agent/images/Screenshot%202025-08-09%20132603.png)

---

### 3. Red Flags and Comments Display

![Red Flags Display](Corporate%20Agent/images/Screenshot%202025-08-09%20132629.png)

---

### 4. Checklist Verification

![Checklist Verification](Corporate%20Agent/images/Screenshot%202025-08-09%20132649.png)

---

### 5. Q&A Interface with Gemini AI

![Q&A Interface](Corporate%20Agent/images/Screenshot%202025-08-09%20132716.png)


---


## Contact

Shiva Kumar Karanam  
Email: shivakumarkaranam2005@gmail.com  
GitHub: [ShivaKumarKaranam2](https://github.com/ShivaKumarKaranam2)



