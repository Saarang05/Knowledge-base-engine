from app.core.vector_store import VectorStore
import numpy as np


def test_vector_store_add_and_search(tmp_path):
    # Create a temporary index path to avoid clobbering real index
    index_path = tmp_path / "test.index"
    meta_path = tmp_path / "test.pkl"
    vs = VectorStore(dim=4, path=str(index_path), meta_path=str(meta_path))

    embeddings = np.array([[0.0, 0.0, 0.0, 1.0], [1.0, 0.0, 0.0, 0.0]], dtype="float32")
    chunks = ["chunk A", "chunk B"]
    vs.add(embeddings, chunks, doc_id="doc")

    q = np.array([[0.0, 0.0, 0.0, 1.0]], dtype="float32")
    results = vs.search(q, k=1)
    assert len(results) == 1
    assert results[0]["text"] in chunks

