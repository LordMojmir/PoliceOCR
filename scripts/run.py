from pdf_processor import PDFProcessor  # Import the PDFProcessor class from pdf_processor.py
from eval import *

if __name__ == '__main__':
    pdf_processor = PDFProcessor()
    pdf_processor.test_cuda()
    input_file = '../data/3-Batch/3_Doc.pdf'
    output_folder = '../data/3-Batch/3_Doc_output/'
    ocr_output = pdf_processor.read_in_new_penalty(input_file, output_folder)
    json_output = query_custom_gpt(ocr_output)
    print(json_output)
    python_object = convert_json_to_object(json_output)
    save_json_to_file(python_object, "test.json")
    obj2excel([python_object, python_object],"./excel/Test.xlsx")