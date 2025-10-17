from sentence_transformers import SentenceTransformer
import numpy as np

_model = None

def get_model(name="all-MiniLM-L6-v2"):
    global _model
    if _model is None:
        _model = SentenceTransformer(name)
    return _model

def embed_texts(texts):
    model = get_model()
    return model.encode(texts, convert_to_numpy=True, show_progress_bar=False)
