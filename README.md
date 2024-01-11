# PDF Processing and Data Extraction Script

This script is designed to process a PDF file using OCR (Optical Character Recognition), extract relevant information, query a custom GPT model with the extracted text, and then output the result to both a JSON file and an Excel spreadsheet.

## Requirements

- Python 3.11
- Required Python packages: `pymupdf`, `easyOCR`, `torch`, `argparse`, `pandas`, `openpyxl`, `json`, `pdf_processor`, `pymupdf` and `eval` modules. 
- A custom GPT model setup for querying (handled by \`query_custom_gpt\` function).

## Installation

Before running the script, make sure to install the required Python packages using pip:

``` bash
pip install pandas openpyxl argparse easyocr matplotlib openai pdf2image pymupdf python-dotenv opencv-python torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
```

## Usage

The script can be executed from the command line. It accepts two optional named arguments:

- `--input_file\`: The path to the input PDF file that you want to process.
- `--output_folder\`: The folder path where the OCR output, JSON, and Excel files will be saved.

### Command Line Syntax

``` bash
python run.py --input_file 'path_to_input.pdf' --output_folder 'path_to_output_folder/'
```


### Examples

Running the script with default values (defined inside the script):

``` bash
python run.py
``` 

Running the script with custom input file and output folder:

``` bash
python run.py --input_file '../data/new_batch/new_doc.pdf' --output_folder '../data/new_batch/output/'
``` 
### Output

The script will produce three output files:
1. `page{i}.png`: All the pdf pages converted into single png files
2. `output_ocr.txt`: An txt file with the OCR-Output
3. `result.json`: Contains the JSON output from the custom GPT model.
4. `TheMachine.xlsx`: An Excel file with the data structured in a tabular form.

Both files will be saved in the directory specified by `--output_folder`.

## Notes

- Ensure the `pdf_processor` and `eval` modules are correctly configured and accessible in your script's directory.
- The script assumes that `PDFProcessor` has methods `test_cuda` and `read_in_new_penalty` for processing the PDF and that `eval` contains the necessary functions for processing the output.

For any issues or further customization, refer to the documentation provided for the `pdf_processor` and `eval` modules, or contact the support team.
