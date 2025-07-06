from PIL import Image
import pytesseract

def extract_text(image_path):
    try:
        img = Image.open(image_path)
        text = pytesseract.image_to_string(img)
        return text
    except Exception as e:
        print(f"[OCR ERROR] {e}")
        return ""