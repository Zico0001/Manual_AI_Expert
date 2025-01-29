import PyPDF2

def extract_text_from_pdf():
    pdf_path = "manual.pdf"
    text = ""
    with open(pdf_path, "rb") as file:
        reader = PyPDF2.PdfFileReader(file)
        for page_num in range(reader.numPages):
            page = reader.getPage(page_num)
            text += page.extract_text()
    return text

if __name__ == "__main__":
    text = extract_text_from_pdf()
    with open("manual_text.txt", "w") as text_file:
        text_file.write(text)
