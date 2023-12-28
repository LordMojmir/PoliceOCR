import easyocr
import numpy as np
import IPython.display as display
from PIL import Image, ImageDraw, ImageFont

# Create a reader instance for German language
reader = easyocr.Reader(['de'])

# Read from an image file
image_path = "C:/Users/horva/Documents/3AHIF/PRE/Police-OCR/data/3-Batch/1_Doc_output/page_1.png"
result = reader.readtext(image_path, paragraph=False)


def draw_output_to_image(ocr_results: str, save_location: str = '../data/output_images/test.png', save: bool = False):
    image_width = 2000
    image_height = int(np.round(2000 * 1.4142))

    font_path = "C:/Users/horva/anaconda3/Lib/site-packages/matplotlib/mpl-data/fonts/ttf/DejaVuSans.ttf"
    font = ImageFont.truetype(font_path, 20)  # You may need to adjust the font size

    # Create a new white image
    new_image = Image.new('RGB', (image_width, image_height), 'white')
    draw = ImageDraw.Draw(new_image)

    #     # OCR results
    #     ocr_results = read_txt_from_image_path('./output_images_test_2/page_1.png')

    for result in ocr_results:
        coords = result[0]
        text = result[1]
        # Get the bounding box coordinates
        top_left = coords[0]
        bottom_right = coords[2]
        # Draw text
        draw.text(top_left, text, (0, 0, 0), font=font)

    if save:
        save_image(new_image, save_location)
    display.display(new_image)

def save_image(new_image: Image.Image, file_path: str) -> None:
    """
    Save the given image to a file.

    :param new_image: The image to save.
    :param file_path: The path where to save the image.
    """
    new_image.save(file_path)

draw_output_to_image(result, 'clean.png', True)

for detection in result:
    text = detection[1]
    print(text)
