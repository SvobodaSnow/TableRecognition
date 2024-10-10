from PIL import Image
from pytesseract import pytesseract


path_to_tesseract = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
pytesseract.tesseract_cmd = path_to_tesseract


def string_from_image(img: Image):
    text = pytesseract.image_to_string(img, lang='rus')
    return text[:-1]