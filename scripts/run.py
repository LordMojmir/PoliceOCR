import argparse
from pdf_processor import PDFProcessor  # Import the PDFProcessor class from pdf_processor.py
from eval import query_custom_gpt, convert_json_to_object, save_json_to_file, obj2excel, append_json_to_file, correct_python_obj
from gdpr_conform import making_OCR_gdpr_conform
from tools_file_processing import json2excel


def process_pdf_and_convert_to_excel(input_file: str, output_folder: str):
    """
    Processes a PDF file, performs OCR, queries a custom GPT model,
    converts the output to a Python object, saves it as a JSON file,
    and finally converts it to an Excel file.

    :param input_file: Path to the input PDF file.
    :param output_folder: Folder to save the OCR output.
    """
    # Initialize PDF Processor
    pdf_processor = PDFProcessor()
    pdf_processor.test_cuda()

    # Create output_folder
    if output_folder == '':
        output_folder = pdf_processor.create_output_folder_for_input_folder(input_file)
        print(f"Out: {output_folder}")

    # Process PDF and Perform OCR
    ocr_output = pdf_processor.read_in_new_penalty(input_file, output_folder, create_png=False)
    clean_ocr_output, name, bearbeiterIn, birthdate = making_OCR_gdpr_conform(ocr_output)

    # Query custom GPT model
    json_output = query_custom_gpt(clean_ocr_output)

    # Convert JSON output to Python object
    python_object = convert_json_to_object(json_output)
    enhanced_obj = correct_python_obj(python_object, input_file, name, birthdate, True)
    # Save Python object to JSON file
    append_json_to_file(enhanced_obj, output_folder + "result.json")

    # Convert Python object to Excel file
    # obj2excel([python_object], output_folder + "TheMachine.xlsx")

if __name__ == "__main__":
    # parser = argparse.ArgumentParser(description="Process a PDF and output to Excel")
    # parser.add_argument("--input_file", help="Path to the input PDF file", default='../data/2-Batch/2_Doc.pdf')
    # parser.add_argument("--output_folder", help="Folder to save the OCR output and result files", default='../data/2-Batch/2_Doc_output/')
    #
    # args = parser.parse_args()
    #
    # process_pdf_and_convert_to_excel(args.input_file, args.output_folder)


    def single_doc():
        process_pdf_and_convert_to_excel('../data/5-Batch/4_Doc_3.2.pdf', '../data/5-Batch/4_Doc_output/')


    def multiple_doc():
        input_files = ['../data/5-Batch/1_Doc_2.2.pdf', '../data/1-Batch/1_Doc.pdf']
        common_output_folder = '../data/common_output_folder/'

        for input_file in input_files:
            process_pdf_and_convert_to_excel(input_file, common_output_folder)

    def make_excel_from_json():
        common_output_folder = '../data/common_output_folder/'
        file_path = common_output_folder + 'result.json'

        excel_saved = json2excel(file_path, common_output_folder + "TheMachine.xlsx")
        print(f"Json saved to excel {excel_saved}")


    single_doc()
#
# from typing import Tuple
#
# def making_OCR_gdpr_conform(ocr_output: str) -> Tuple[str, str]:
#     clean_ocr_output = ocr_output
#     name = "Paul Wenth"
#     return clean_ocr_output, name


