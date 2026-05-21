from pypdf import PdfReader

def extracted_text_from_pdf(file):

    reader = PdfReader(file.file)

    text = ""

    for page in reader.pages:
        extracted = page.extract_text()

        if extracted:
            text += extracted

    return text

    