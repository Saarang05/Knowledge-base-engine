from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.core.embeddings import embed_texts
from app.core.vector_store import VectorStore
from app.core.rag import synthesize_answer

router = APIRouter()

class QueryRequest(BaseModel):
    query: str
    top_k: int = 3

@router.post("/query")
def query_docs(req: QueryRequest):
    vs = VectorStore(dim=384)  # same dim as embedding model
    if vs.count() == 0:
        raise HTTPException(status_code=400, detail="The index is empty. Ingest documents first.")
    query_emb = embed_texts([req.query])
    results = vs.search(query_emb, k=req.top_k)
    # Build context texts from results
    context_chunks = [r["text"] for r in results]
    answer = synthesize_answer(req.query, context_chunks)
    return {
        "answer": answer,
        "sources": results
    }
