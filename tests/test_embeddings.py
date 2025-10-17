from app.core.embeddings import embed_texts


def test_embed_texts_shape():
    texts = ["hello world", "knowledge base"]
    embs = embed_texts(texts)
    assert embs.shape[0] == 2
    # all-MiniLM-L6-v2 has 384 dims
    assert embs.shape[1] == 384

