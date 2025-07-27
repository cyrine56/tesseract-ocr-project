# converters/image_to_text.py
from PIL import Image
import pytesseract
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

def image_to_text(image_path):
    text = pytesseract.image_to_string(Image.open(image_path))
    return text
