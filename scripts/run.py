from pdf_processor import PDFProcessor  # Import the PDFProcessor class from pdf_processor.py
from eval import query_custom_gpt, convert_json_to_object, save_json_to_file, obj2excel

def process_pdf_and_convert_to_excel(input_file: str, output_folder: str, json_file_path: str, excel_file_path: str):
    """
    Processes a PDF file, performs OCR, queries a custom GPT model,
    converts the output to a Python object, saves it as a JSON file,
    and finally converts it to an Excel file.

    :param input_file: Path to the input PDF file.
    :param output_folder: Folder to save the OCR output.
    :param json_file_path: Path to save the JSON file.
    :param excel_file_path: Path to save the Excel file.
    """
    # Initialize PDF Processor
    pdf_processor = PDFProcessor()
    pdf_processor.test_cuda()

    # Process PDF and Perform OCR
    ocr_output = pdf_processor.read_in_new_penalty(input_file, output_folder)

    # Query custom GPT model
    json_output = query_custom_gpt(ocr_output)

    # Convert JSON output to Python object
    python_object = convert_json_to_object(json_output)

    # Save Python object to JSON file
    save_json_to_file(python_object, json_file_path)

    # Convert Python object to Excel file
    obj2excel([python_object, python_object], excel_file_path)

# Example usage
input_file = '../data/3-Batch/3_Doc.pdf'
output_folder = '../data/3-Batch/3_Doc_output/'
json_file_path = './json/test.json'
excel_file_path = './excel/Test.xlsx'

process_pdf_and_convert_to_excel(input_file, output_folder, json_file_path, excel_file_path)
