# extract_text.py
import fitz  # PyMuPDF

def extract_text_from_pdf():
    pdf_path = "manual.pdf"
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text()
    return text

if __name__ == "__main__":
    text = extract_text_from_pdf()
    with open("manual_text.txt", "w") as text_file:
        text_file.write(text)
