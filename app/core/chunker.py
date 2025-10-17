import re

def chunk_text(text: str, max_chars: int = 1000, overlap: int = 200):
    """Split text into overlapping chunks for embedding."""
    paragraphs = [p.strip() for p in re.split(r'\n{1,}', text) if p.strip()]
    chunks = []
    current = ""

    for para in paragraphs:
        if len(current) + len(para) < max_chars:
            current += " " + para
        else:
            chunks.append(current.strip())
            current = para
    if current:
        chunks.append(current.strip())

    # add overlap
    final_chunks = []
    for i, chunk in enumerate(chunks):
        if i == 0:
            final_chunks.append(chunk)
        else:
            final_chunks.append(chunks[i-1][-overlap:] + " " + chunk)
    return final_chunks
