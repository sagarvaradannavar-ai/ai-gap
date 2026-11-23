
import fitz


def extract_pdf_text(pdf_bytes):

    document = fitz.open(
        stream=pdf_bytes,
        filetype="pdf"
    )

    text = ""

    for page in document:
        text += page.get_text() + "\n"

    document.close()

    if not text.strip():
        raise ValueError("No readable text found in PDF.")

    return text
