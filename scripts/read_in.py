import cv2
import easyocr
import numpy as np
import matplotlib.pyplot as plt
from typing import List, Dict, Any, Optional
import os
import io
from PIL import Image, ImageDraw, ImageFont
# import IPython.display as display
import re
import fitz  # PyMuPDF
import json
import torch
from pdf2image import convert_from_path
# from openAI import make_LLM_prompt, make_request_to_OpenAI, str2json, save_json_to_file, remove_text_before_character

def test_cuda() -> bool:
    # Check if CUDA is available
    cuda_available = torch.cuda.is_available()
    print(f"CUDA Available: {cuda_available}")

    # If CUDA is available, display the CUDA device name
    if cuda_available:
        print(f"CUDA Device Name: {torch.cuda.get_device_name(0)}")
        return True
    else:
        print("CUDA is not available.")
        return False
def pdf_to_img(pdf_path: str, output_folder: str, only_create: bool = True, poppler_path: str = r"../poppler-23.08.0/Library/bin/") -> Optional[List[Image.Image]]:
    try:
        os.makedirs(output_folder, exist_ok=True)

        images = convert_from_path(pdf_path, poppler_path=poppler_path)

        for i, image in enumerate(images):
            # Save pages as images in the pdf
            output_file = os.path.join(output_folder, f'page_{i + 1}.png')
            image.save(output_file, 'PNG')

        if only_create:
            return None

        return images
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

def read_txt_from_image(image) -> str:
    image_np = np.array(image)

    reader = easyocr.Reader(['de'], gpu=True)

    result = reader.readtext(image_np, paragraph=False)
    return result

def extract_txt_from_reader_output(output_reader: str) -> str:
    extracted_text = ""
    for detection in output_reader:
        text = detection[1]
        extracted_text += text + " "
    return extracted_text

def save_string_to_txt(content, filename, folder_path):
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    file_path = os.path.join(folder_path, filename)
    with open(file_path, 'w') as file:
        file.write(content)

def read_in_new_penalty(pdf_path: str, output_folder_str: str):
    images = pdf_to_img(pdf_path=pdf_path, output_folder=output_folder_str, only_create=False)
    result: str = ""
    print(f"File has {len(images)} pages")
    for i, image in enumerate(images):
        result += extract_txt_from_reader_output(read_txt_from_image(image))
        print(f"currently reading page {i}.")
    save_string_to_txt(result, "output_ocr.txt", output_folder_str)
    print(result)
    return result


def read_in_data(output_folder: str, input_pdf_doc: str) -> str:
    test_cuda()
    ocr_output = read_in_new_penalty(input_pdf_doc, output_folder)
    return ocr_output


if __name__ == '__main__':
    test_cuda()
    output_folder = '../data/1-Batch/2_Doc_output/'
    ocr_output = read_in_new_penalty('../data/1-Batch/2_Doc.pdf', output_folder)
    #Multea ~ BH Mo BEZIRKSHAUPTMANNSCHAFT NEUNKIRCHEN Fachgebiet Strafen N 2620 Neunkirchen; Peischingerstraße 17 Bezirkshauptmannschaft Neunkirchen 2620 Landespolizeidirektion Wien Polizeianhaltezentrum Roßauer Lände Abteilung für fremdenpolizeiliche Maßnahmen und Anhaltevollzug Roßauer Lände 9 1090 Wien Beilagen E-Mail: strafen.bhnk@noel.gv.at Fax: 02635/9025-35341 Burgerservice: 02742/9005-9005 NKS2-V-22 38030/3 Internet: www.noe.gv.at ww.noe. gv.atdatenschutz Kennzeichen (bei Antwort bitte angeben) ((0 26 35) 9025 Bearbeitung Durchwahl Datum Bezug 35358 18.09.2023 Betrifft Ersuchen um Anschlussvollzug der Ersatzfreiheitsstrafe SEP. dzt. PAZ Wien, 1090 Wien, Roßauer Lände 9. Es wird um Aushändigung der beiliegenden Verständigung an die oben genannte Partei und Veranlassung der Vorführung ersucht. Das Polizeianhaltezentrum Wien wird um Anschlussvollzug der Ersatzfreiheitsstrafe ersucht. Auf Grund des Strafbescheides vom 02.08.2022, Zahl NKS2-V-22 38030/3, ist noch folgende rechtskräftig verhängte (Rest-)Strafe zu vollstrecken: Geldstrafe: Ersatzfreiheitsstrafe: Übertretung gemäß: 1 . $ 52 lit.a 210a StVO 1960, $ 99 Abs.3 lit.a StVO € 110,00 50 Stunden 1960 Offene Geldstrafe gesamt: € 110,00 Offene Ersatzfreiheitsstrafe gesamt: 2 Tage 2 Stunden Außerdem sind noch € als Beitrag zu den Kosten des Verfahrens, Mahngebühren in der Höhe von € 5,00 sowie Barauslagen von € und Exekutionskosten im Ausmaß von € 45,50 zu bezahlen. Offener Gesamtbetrag (Geldstrafe inkl. Kosten): € 160,50 782 418 2 Strafbeginn am: verjährt am: 23.08.2025 Auf die Bestimmungen des $ 36 und $ 36a Verwaltungsstrafgesetz 1991 (VStG) darf hingewiesen werden. Die Vorführung hinsichtlich der Ersatzfreiheitsstrafe hat zu unterbleiben; wenn der Strafbetrag anlässlich der Abholung zur Vorführung bezahlt wird (bitte uns mit dem beiliegenden Zahlschein bzw. auf das nachfolgend angeführte Konto überweisen) oder nachweislich bereits vorher bezahlt wurde. Bankverbindung für die Überweisung von hereingebrachten Beträgen: Offener Gesamtbetrag: € 160,50 Empfänger: BH Neunkirchen Verwaltungsstrafen Bank: Raiffeisenbank Wr. Neustadt-Schneebergland eGen IBAN: AT59 3293 7000 0364 0372 BIC (= SWIFT-Code): RLNWATWRN (SEPA-Überweisungl) Zahlungsreferenz: GFN: 2023 1638 Es wird ersucht; die Zahlungsreferenz (falls vorhanden) und als Verendungszweck den Namen derls Verpflichteten sowie das Aktenkennzeichen anzugeben. Für die Bezirkshauptfrau SDEAOSTERRFIC> Dieses Schriftstück wurde amtssigniert. Hinweise finden Sie unter: www.noe.gv.atlamtssignatur Aktssignatur




# def ai_future():
#     ai_result = make_request_to_OpenAI(make_LLM_prompt(ocr_output))
#     print(f"AI output: \n {ai_result}")
#     json_obj = str2json(remove_text_before_character(ai_result, "{"))
#
#     save_json_to_file(json_obj, output_folder + "output.json")
#     print(f"JSON Output: \n{json_obj}")