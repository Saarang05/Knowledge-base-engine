from fastapi import APIRouter, UploadFile, File
from typing import List
import os
import uuid
from app.core.parser import extract_text_from_pdf
from app.core.chunker import chunk_text
from app.core.embeddings import embed_texts
from app.core.vector_store import VectorStore

router = APIRouter()

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/ingest")
async def ingest_documents(files: List[UploadFile] = File(...)):
    vs = None
    total_chunks = 0
    indexed_docs = []
    for file in files:
        file_path = os.path.join(UPLOAD_DIR, file.filename)
        with open(file_path, "wb") as f:
            f.write(await file.read())

        # Currently supporting PDF; extension-based branch for future text/docx
        text = extract_text_from_pdf(file_path)
        chunks = chunk_text(text)
        if not chunks:
            continue
        embeddings = embed_texts(chunks)

        if vs is None:
            vs = VectorStore(dim=embeddings.shape[1])
        vs.add(embeddings, chunks, doc_id=file.filename)
        total_chunks += len(chunks)
        indexed_docs.append({"filename": file.filename, "chunks": len(chunks)})

    return {"message": "Documents indexed successfully!", "total_chunks": total_chunks, "documents": indexed_docs}
