import cv2
import easyocr
import numpy as np
import os
import io
from PIL import Image
import re
import fitz
import json
import torch
from pdf2image import convert_from_path
from typing import List, Optional

class PDFProcessor:
    def __init__(self):
        self.poppler_path = r"../poppler-23.08.0/Library/bin/"

    def test_cuda(self) -> bool:
        cuda_available = torch.cuda.is_available()
        print(f"CUDA Available: {cuda_available}")
        if cuda_available:
            print(f"CUDA Device Name: {torch.cuda.get_device_name(0)}")
            return True
        else:
            print("CUDA is not available.")
            return False

    def pdf_to_img(self, pdf_path: str, output_folder: str, only_create: bool = True) -> Optional[List[Image.Image]]:
        try:
            os.makedirs(output_folder, exist_ok=True)
            images = convert_from_path(pdf_path, poppler_path=self.poppler_path)

            for i, image in enumerate(images):
                output_file = os.path.join(output_folder, f'page_{i + 1}.png')
                image.save(output_file, 'PNG')

            if only_create:
                return None

            return images
        except Exception as e:
            print(f"An error occurred: {e}")
            return None

    def read_txt_from_image(self, image) -> str:
        image_np = np.array(image)
        reader = easyocr.Reader(['de'], gpu=True)
        result = reader.readtext(image_np, paragraph=False)
        return result

    def extract_txt_from_reader_output(self, output_reader: str) -> str:
        extracted_text = ""
        for detection in output_reader:
            text = detection[1]
            extracted_text += text + " "
        return extracted_text

    def save_string_to_txt(self, content, filename, folder_path):
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
        file_path = os.path.join(folder_path, filename)
        with open(file_path, 'w') as file:
            file.write(content)

    def read_in_new_penalty(self, pdf_path: str, output_folder_str: str):
        images = self.pdf_to_img(pdf_path=pdf_path, output_folder=output_folder_str, only_create=False)
        result: str = ""
        print(f"File has {len(images)} pages")
        for i, image in enumerate(images):
            result += self.extract_txt_from_reader_output(self.read_txt_from_image(image))
            print(f"currently reading page {i}.")
        self.save_string_to_txt(result, "output_ocr.txt", output_folder_str)
        print(result)
        return result

    def read_in_data(self, input_pdf_doc: str, output_folder: str) -> str:
        # self.test_cuda()
        ocr_output = self.read_in_new_penalty(input_pdf_doc, output_folder)
        return ocr_output

# if __name__ == '__main__':
#     pdf_processor = PDFProcessor()
#     pdf_processor.test_cuda()
#     output_folder = '../data/1-Batch/2_Doc_output/'
#     ocr_output = pdf_processor.read_in_new_penalty('../data/1-Batch/2_Doc.pdf', output_folder)
#     # Now you can use pdf_processor to call other functions as needed.
