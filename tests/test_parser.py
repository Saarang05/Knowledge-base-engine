from app.core.parser import extract_text_from_pdf
import os


def test_extract_text_from_pdf_sample():
    sample_path = os.path.join("example_docs", "sample.pdf")
    text = extract_text_from_pdf(sample_path)
    assert isinstance(text, str)
    assert len(text) > 0

