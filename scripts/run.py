import argparse
from pdf_processor import PDFProcessor  # Import the PDFProcessor class from pdf_processor.py
from eval import query_custom_gpt, convert_json_to_object, save_json_to_file, obj2excel

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

    # Process PDF and Perform OCR
    ocr_output = pdf_processor.read_in_new_penalty(input_file, output_folder)

    # Query custom GPT model
    json_output = query_custom_gpt(ocr_output)

    # Convert JSON output to Python object
    python_object = convert_json_to_object(json_output)

    # Save Python object to JSON file
    save_json_to_file(python_object, output_folder + "result.json")

    # Convert Python object to Excel file
    obj2excel([python_object], output_folder + "TheMachine.xlsx")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process a PDF and output to Excel")
    parser.add_argument("--input_file", help="Path to the input PDF file", default='../data/2-Batch/2_Doc.pdf')
    parser.add_argument("--output_folder", help="Folder to save the OCR output and result files", default='../data/2-Batch/2_Doc_output/')

    args = parser.parse_args()

    process_pdf_and_convert_to_excel(args.input_file, args.output_folder)
