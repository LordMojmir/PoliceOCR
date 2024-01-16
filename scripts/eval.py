import os
import json
import pandas as pd
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def query_custom_gpt(doc_text):
    """
    Sends a prompt to the GPT model and returns the response.

    :param doc_text: The document text to be analyzed.
    :param system_message: The system instruction for the GPT model.
    :return: The response text from the model.
    """
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

    system_message_v1 = "PoliceOCR Data is engineered to analyze legal and official documents, particularly in the law enforcement and judiciary context, and systematically extract data into a very specific JSON structure. This structure includes: 'Name', 'Geburtsdatum', 'Behörde', 'Geschäftszahl (Vorführende Behörde)', 'Geschäftszahl (Strafende Behörde)', 'Verjährung', 'Ersatzfreiheitsstrafe' (broken down into 'Tage', 'Stunden', 'Minuten'), 'Freiheitsstrafe' (also broken down into 'Tage', 'Stunden', 'Minuten'), and monetary values for 'Offene Strafen (in €)' and 'Sonstige Kosten (in €)'. If a specific piece of data is not found within the document, PoliceOCR Data is programmed to set the fields to default values: numerical fields to 0 and text fields to an empty string. This GPT is designed to provide outputs strictly in this JSON format, without any deviation or conversational elements. VVJ also can indicate the Verjährung. Dont format the JSON response, pure json" #   Vorführende Behörde and Strafende Behörde are the same unless the text says differently.
    system_message_v2 = "PoliceOCRv2 is programmed to analyze legal and official documents, especially in law enforcement and judiciary contexts. It systematically extracts data into a specific JSON structure, which includes fields like 'Name', 'Geburtsdatum', 'Behörde', 'Geschäftszahl (Vorführende Behörde)', 'Geschäftszahl (Strafende Behörde)', 'Verjährung', 'Ersatzfreiheitsstrafe', 'Freiheitsstrafe' (both broken down into 'Tage', 'Stunden', 'Minuten'), and monetary values for 'Offene Strafen (in €)' and 'Sonstige Kosten (in €)'. For data not found in the document, it sets default values: numerical fields to 0 and text fields to an empty string. PoliceOCRv2 prioritizes more precise values, often found in the second OCR output, especially for 'Verjährung'. Outputs are strictly in JSON format, with no deviation or conversational elements. VVJ can also indicate 'Verjährung'. Sonstige kosten should be a sum of all Sonstige kosten wihtout the main penalty. Allways answer with the fixed structure JSON! " #  Special attention is given to the precise differentiation between days and hours, as tables may sometimes ambiguously present hours as days.
    system_message_v3 = "PoliceOCRv2 is engineered for the precise analysis of legal and official documents, predominantly in law enforcement and judiciary settings. It extracts data into a predefined JSON structure, featuring fields like 'Name', 'Geburtsdatum', 'Behörde', 'Geschäftszahl (Vorführende Behörde)', 'Geschäftszahl (Strafende Behörde)', 'Verjährung', 'Ersatzfreiheitsstrafe', 'Freiheitsstrafe' (broken down into 'Tage', 'Stunden', 'Minuten'), and monetary values for 'Offene Strafen (in €)' and 'Sonstige Kosten (in €)'. For data absent in the document, default values are set: numerical fields to 0 and text fields to empty. Special attention is given to the precise differentiation between days and hours, as tables may sometimes ambiguously present hours as days. 'Sonstige Kosten' is calculated as the sum of all additional costs excluding the main penalty. The output is consistently in the specified JSON format, with an emphasis on accuracy and no conversational elements. VVJ can indicate 'Verjährung'."
    chat = [
        {"role": "system", "content": system_message_v2},
        {"role": "user", "content": doc_text},
    ]

    try:
        response = client.chat.completions.create(
            model=   "gpt-4-1106-preview", # "gpt-3.5-turbo-1106", #
            response_format={"type": "json_object"},
            messages=chat,
            max_tokens=750,

        )
        return response.choices[0].message.content
    except Exception as e:
        return str(e)

def convert_json_to_object(json_string):
    """
    Converts a JSON string to a Python dictionary.

    :param json_string: The JSON string to be converted.
    :return: A Python dictionary representing the JSON data.
    """
    try:
        python_object = json.loads(json_string)
        return python_object
    except json.JSONDecodeError as e:
        return f"Error decoding JSON: {str(e)}"

def obj2excel(data_list: object, excel_file_path: str) -> bool:
    df = pd.json_normalize(data_list)

    return df.to_excel(excel_file_path, index=False)


def save_json_to_file(json_obj, file_path):
    try:
        with open(file_path, 'w') as json_file:
            json.dump(json_obj, json_file, indent=4)
        print(f"JSON data saved to {file_path}")
    except Exception as e:
        print(f"Error saving JSON to file: {e}")

def append_json_to_file(data, file_path):
    """
    Append JSON data to a file. If the file already exists, load existing data, append the new data to it,
    and then write it back to the file.

    :param data: JSON data to append.
    :param file_path: Path to the JSON file.
    """
    existing_data = []

    # Check if the file already exists and load existing data
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            try:
                existing_data = json.load(file)
            except json.JSONDecodeError:
                print(f"Warning: File {file_path} contains invalid JSON data.")

    # Append the new data to the existing data
    existing_data.append(data)

    # Write the combined data to the file
    with open(file_path, 'w') as file:
        json.dump(existing_data, file, indent=4)

def validate_python_object(python_object):
    # Check existence
    if python_object is None:
        return False, "Object does not exist."

    # Check required fields
    required_fields = [
        'Geschäftszahl (Strafende Behörde)',
        'Geschäftszahl (Vorführende Behörde)', 'Name', 'Geburtsdatum',
        'Behörde', 'Verjährung', 'Ersatzfreiheitsstrafe', 'Freiheitsstrafe',
        'Offene Strafen (in €)', 'Sonstige Kosten (in €)'
    ]
    for field in required_fields:
        if field.lower() not in python_object:
            return False, f"Missing field: {field}"

    # Check if Ersatzfreiheitsstrafe and Freiheitsstrafe are dictionaries with specific keys
    for field in ['Ersatzfreiheitsstrafe', 'Freiheitsstrafe']:
        if not isinstance(python_object[field], dict):
            return False, f"{field} should be a dictionary."
        for key in ['Tage', 'Stunden', 'Minuten']:
            if key not in python_object[field]:
                return False, f"Missing key '{key}' in {field}."


    return True, "Object is valid."


def correct_python_obj(python_object, input_file: str, name: str, birthday: str, validate_obj: bool) :
    is_valid, message = validate_python_object(python_object)
    if is_valid or validate_obj:
        python_object['Doc'] = input_file
        strafend_gz = python_object["Geschäftszahl (Strafende Behörde)"]
        vorfuhrend_gz = python_object["Geschäftszahl (Vorführende Behörde)"]
        if len(vorfuhrend_gz) < len(strafend_gz):
            python_object["Geschäftszahl (Vorführende Behörde)"] = strafend_gz
        if strafend_gz == "":
            python_object["Geschäftszahl (Strafende Behörde)"] = vorfuhrend_gz

        # if (len(python_object['Name']) > 0):
        python_object['Name'] = name

        # if (len(python_object['Geburtsdatum']) > 4):
        python_object['Geburtsdatum'] = birthday

    else:
        print(message)
    return python_object

