import pytesseract
from PIL import Image

def read_txt_from_image_path(image_path: str):
    # Set the path to the Tesseract executable (change this to your Tesseract installation path)
    pytesseract.pytesseract.tesseract_cmd = 'C:/Program Files/Tesseract-OCR/tesseract.exe'

    # Load an image using PIL (Pillow)
    image = Image.open(image_path)

    # Perform OCR on the image
    text = pytesseract.image_to_string(image, lang='deu')

    return text

def read_txt_from_image(image: Image):
    # Set the path to the Tesseract executable (change this to your Tesseract installation path)
    pytesseract.pytesseract.tesseract_cmd = 'C:/Program Files/Tesseract-OCR/tesseract.exe'

    # Perform OCR on the image
    text = pytesseract.image_to_string(image, lang='deu')

    return text

# # Example usage:
# image_path = '../data/1-Batch/3_Doc_output/page_2.png'
# image_path = 'test/table-test.png'
# extracted_text = read_txt_from_image_path(image_path)
# print(extracted_text)
