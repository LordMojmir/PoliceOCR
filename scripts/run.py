from pdf_processor import PDFProcessor  # Import the PDFProcessor class from pdf_processor.py

if __name__ == '__main__':
    pdf_processor = PDFProcessor()
    pdf_processor.test_cuda()
    input_file = '../data/3-Batch/3_Doc.pdf'
    output_folder = '../data/3-Batch/3_Doc_output/'
    ocr_output = pdf_processor.read_in_new_penalty(input_file, output_folder)
