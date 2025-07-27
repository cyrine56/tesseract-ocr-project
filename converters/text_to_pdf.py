# converters/text_to_pdf.py
import fitz  # PyMuPDF

def txt_to_pdf(txt_file_path, pdf_output_path):
    with open(txt_file_path, 'r', encoding='utf-8') as f:
        text = f.read()

    doc = fitz.open()
    page = doc.new_page()
    page.insert_text((72, 72), text, fontsize=12)
    doc.save(pdf_output_path)
    doc.close()
