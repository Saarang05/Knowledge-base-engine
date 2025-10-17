import faiss
import numpy as np
import pickle
import os

class VectorStore:
    def __init__(self, dim, path="vector.index", meta_path="meta.pkl"):
        self.dim = dim
        self.path = path
        self.meta_path = meta_path
        if os.path.exists(path) and os.path.exists(meta_path):
            self.index = faiss.read_index(path)
            # If existing meta is a list of strings, coerce to dicts for backward compatibility
            loaded_meta = pickle.load(open(meta_path, "rb"))
            if loaded_meta and isinstance(loaded_meta[0], str):
                self.meta = [{"text": m, "doc_id": None, "chunk_id": idx} for idx, m in enumerate(loaded_meta)]
            else:
                self.meta = loaded_meta or []
            # Ensure dimension matches loaded index
            try:
                self.dim = self.index.d
            except Exception:
                pass
        else:
            self.index = faiss.IndexFlatL2(dim)
            self.meta = []

    def add(self, embeddings, chunks, doc_id=None):
        if embeddings is None or len(embeddings) == 0:
            return
        # Ensure shapes align
        embeddings = np.asarray(embeddings, dtype="float32")
        if embeddings.shape[1] != self.dim:
            raise ValueError(f"Embedding dim {embeddings.shape[1]} does not match index dim {self.dim}")
        # Add to FAISS
        self.index.add(embeddings)
        # Store metadata entries
        start_idx = len(self.meta)
        for offset, chunk in enumerate(chunks):
            self.meta.append({
                "text": chunk,
                "doc_id": doc_id,
                "chunk_id": start_idx + offset
            })
        self.save()

    def search(self, query_emb, k=3):
        if getattr(self.index, 'ntotal', 0) == 0:
            return []
        query_emb = np.asarray(query_emb, dtype="float32")
        D, I = self.index.search(query_emb, k)
        indices = I[0]
        distances = D[0]
        results = []
        for idx, dist in zip(indices, distances):
            if idx < 0 or idx >= len(self.meta):
                continue
            item = dict(self.meta[idx])
            item["score"] = float(dist)
            results.append(item)
        return results

    def count(self):
        return getattr(self.index, 'ntotal', 0)

    def save(self):
        faiss.write_index(self.index, self.path)
        pickle.dump(self.meta, open(self.meta_path, "wb"))
