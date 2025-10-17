# 🧠 Knowledge‑Base Search Engine

A document search system powered by Retrieval‑Augmented Generation (RAG) using OpenAI’s gpt-4o-mini. It allows users to upload PDFs or text files, index them, and query across documents to get concise, synthesized answers directly from your data.

---

## 🚀 Features

- Upload and index multiple documents (PDF or text)
- Automatic text chunking and retrieval using embeddings
- Context‑aware query processing with synthesized answers
- Integration with OpenAI GPT‑4o‑mini via the openai Python SDK
- Static website frontend to showcase the search engine
- Backend implemented using FastAPI

---

## 🏗️ Project Structure

knowledgebase-search/
│
├── app/
│   ├── main.py               # FastAPI app entry point
│   ├── api/
│   │   ├── ingest.py         # Endpoint to upload and index documents
│   │   └── query.py          # Endpoint to handle query requests
│   └── core/
│       └── rag.py            # RAG and LLM integration logic
│
├── static-site/              # Frontend (HTML/CSS/JS)
├── tests/                    # Unit tests
├── venv/                     # Virtual environment
└── .gitignore

---

## 🛠️ Technologies Used

- Backend: Python, FastAPI
- Frontend: Static HTML, CSS, JavaScript
- Database: In‑memory embedding storage
- LLM: OpenAI GPT‑4o‑mini via openai SDK
- Environment Management: python-dotenv

---

## ⚙️ Installation

### 1. Clone the repository
git clone https://github.com/Saarang05/knowledge-base-engine.git 
cd knowledgebase-search

### 2. Create and activate a virtual environment
python -m venv venv
# Windows
venv\Scripts\activate
# macOS / Linux
source venv/bin/activate

### 3. Install dependencies
pip install -r requirements.txt

### 4. Configure environment variables
Create a .env file in the project root and add your OpenAI API key:

OPENAI_API_KEY=your_openai_api_key_here

Ensure .env is listed in .gitignore to protect your API key.

---

## ▶️ Usage

### 1. Run the FastAPI server
uvicorn app.main:app --reload

### 2. API Endpoints

# Upload documents
POST /ingest
Body (form-data):
- file: <PDF or TXT file>

Response:
{
  "message": "Document 'sample.pdf' indexed successfully!",
  "chunks": 1
}

# Query documents
POST /query
Body (JSON):
{
  "query": "Your question here"
}

Response:
{
  "answer": "Synthesized answer based on documents."
}

---

## 🌐 Static Website

Open static-site/index.html in your browser to:
- Upload documents
- Enter queries
- View synthesized answers

---

## 🧩 Notes

- Works with multiple PDFs and text files.
- Automatic text chunking ensures efficient retrieval for large documents.
- Designed for easy deployment and demonstration with static frontend + FastAPI backend.

---

## 🎥 Demo

https://youtu.be/fIKqJ_S-IlM

---

## 👤 Author

Saarang P
