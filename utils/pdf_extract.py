import fitz  # PyMuPDF
from PIL import Image
import os

def convert_pdf_to_image(pdf_path, output_folder):
    doc = fitz.open(pdf_path)
    if doc.page_count == 0:
        raise ValueError("Empty PDF")

    page = doc.load_page(0)
    pix = page.get_pixmap(dpi=200)
    img_path = os.path.join(output_folder, "converted_page.jpg")
    pix.save(img_path)
    return img_path
