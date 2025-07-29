
import sys
from pdf2docx import Converter
import PyPDF2
import pytesseract
from pdf2image import convert_from_path
from docx import Document
import os

pdf_file = sys.argv[1]
docx_file = sys.argv[2]

try:
    # Check if PDF is encrypted
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    if pdf_reader.is_encrypted:
        print("error: Password-protected PDF is not supported.")
        sys.exit(1)

    # Check if PDF has extractable text
    has_text = False
    for page in pdf_reader.pages:
        text = page.extract_text()
        if text and text.strip():
            has_text = True
            break

    if has_text:
        # Use pdf2docx for text-based PDFs
        cv = Converter(pdf_file)
        cv.convert(docx_file, start=0, end=None)
        cv.close()
        print("success")
    else:
        # Use OCR for scanned/image-based PDFs
        doc = Document()
        images = convert_from_path(pdf_file)
        for image in images:
            text = pytesseract.image_to_string(image)
            doc.add_paragraph(text)
        doc.save(docx_file)
        print("success")

except Exception as e:
    print(f"error: {str(e)}")
    sys.exit(1)
