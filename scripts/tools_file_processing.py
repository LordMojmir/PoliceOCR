import json
import pandas as pd

def json2excel(json_path, excel_path):
    with open(json_path, 'r') as file:
        raw_json_content = file.read()
    parsed_json = json.loads(raw_json_content)

    # Convert the parsed JSON to a DataFrame
    json_df = pd.json_normalize(parsed_json)

    # Convert to Excel and save
    json_df.to_excel(excel_path, index=False)