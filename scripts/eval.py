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
    system_message_v1 = "PoliceOCR Data is engineered to analyze legal and official documents, particularly in the law enforcement and judiciary context, and systematically extract data into a very specific JSON structure. This structure includes: 'Name', 'Geburtsdatum', 'Behörde', 'Geschäftszahl (Vorführende Behörde)', 'Geschäftszahl (Strafende Behörde)', 'Verjährung', 'Ersatzfreiheitsstrafe' (broken down into 'Tage', 'Stunden', 'Minuten'), 'Freiheitsstrafe' (also broken down into 'Tage', 'Stunden', 'Minuten'), and monetary values for 'Offene Strafen (in €)' and 'sonstige Kosten (in €)'. If a specific piece of data is not found within the document, PoliceOCR Data is programmed to set the fields to default values: numerical fields to 0 and text fields to an empty string. This GPT is designed to provide outputs strictly in this JSON format, without any deviation or conversational elements. VVJ also can indicate the Verjährung. Dont format the JSON response, pure json" #   Vorführende Behörde and Strafende Behörde are the same unless the text says differently.
    system_message_v2 = "PoliceOCRv2 is programmed to analyze legal and official documents, especially in law enforcement and judiciary contexts. It systematically extracts data into a specific JSON structure, which includes fields like 'Name', 'Geburtsdatum', 'Behörde', 'Geschäftszahl (Vorführende Behörde)', 'Geschäftszahl (Strafende Behörde)', 'Verjährung', 'Ersatzfreiheitsstrafe', 'Freiheitsstrafe' (both broken down into 'Tage', 'Stunden', 'Minuten'), and monetary values for 'Offene Strafen (in €)' and 'sonstige Kosten (in €)'. For data not found in the document, it sets default values: numerical fields to 0 and text fields to an empty string. PoliceOCRv2 prioritizes more precise values, often found in the second OCR output, especially for 'Verjährung'. Outputs are strictly in JSON format, with no deviation or conversational elements. VVJ can also indicate 'Verjährung'. Sonstige kosten should be a sum of all sonstige kosten wihtout the main strafe. Allways answer with the fixed structure JSON! Special attention is given to the precise differentiation between days and hours, as tables may sometimes ambiguously present hours as days.  "
    system_message_v3 = "PoliceOCRv2 is engineered for the precise analysis of legal and official documents, predominantly in law enforcement and judiciary settings. It extracts data into a predefined JSON structure, featuring fields like 'Name', 'Geburtsdatum', 'Behörde', 'Geschäftszahl (Vorführende Behörde)', 'Geschäftszahl (Strafende Behörde)', 'Verjährung', 'Ersatzfreiheitsstrafe', 'Freiheitsstrafe' (broken down into 'Tage', 'Stunden', 'Minuten'), and monetary values for 'Offene Strafen (in €)' and 'sonstige Kosten (in €)'. For data absent in the document, default values are set: numerical fields to 0 and text fields to empty. Special attention is given to the precise differentiation between days and hours, as tables may sometimes ambiguously present hours as days. 'Sonstige Kosten' is calculated as the sum of all additional costs excluding the main penalty. The output is consistently in the specified JSON format, with an emphasis on accuracy and no conversational elements. VVJ can indicate 'Verjährung'."
    chat = [
        {"role": "system", "content": system_message_v2},
        {"role": "user", "content": doc_text},
    ]

    try:
        response = client.chat.completions.create(
            model=  "gpt-3.5-turbo-1106", # "gpt-4-1106-preview",
            response_format={"type": "json_object"},
            messages=chat,
            max_tokens=750
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

# doc_text = "BEZIRKSHAUPTMANNSCHAFT BADEN Fachgebiet Strafen 2500 Baden, Schwartzstraße 50 Bezirkshauptmannschaft_Baden 2500 Herrn 1230 Wien, Liesing E-Mail: strafen Bhbn@noel. gv.at Beilagen Fax: 02252/9025-22341 Bürgerservice: 02742/9005-9005 BNS2-V-22 73325/3 Internet: www.noe.gv.at www.noe.gv atldatenschutz Kennzeichen (bei Antwort bitte angeben) (0 22 52) 9025 Durchwahl Datum Bezug Bearbeitung 22347 12.09.2023 Betrifft Aufforderung zum Antritt der Ersatzfreiheitsstrafe Auf_Grund des Strafbescheides vom 09.12.2022, ZahLBNS2-V-22.73325/3, ist noch folgende gegen Sie rechtskräftig verhängte (Rest-)Strafe zu vollstrecken: Geldstrafe: Ersatzfreiheitsstrafe: Übertretung gemäß: 1 $ 103 Abs.2, $ 134 Abs.1 KFG 1967 € 225,00 22 Stunden Offene Geldstrafe gesamt: € 225,00 Offene Ersatzfreiheitsstrafe gesamt: 22 Stunden noch € als Beitrag zu den Kosten des Verfahrens. Mahngebühren in der Außerdem sind € und Exekutionskosten im Ausmaß von Höhe von € 5,00 sowie Barauslagen von € 67,50 zu bezahlen. Offener Gesamtbetrag (Geldstrafe inkI. Kosten): € 297, Annahme besteht; dass die Geldstrafe uneinbringlich ist; muss nunmehr die Da Grund zur Ersatzfreiheitsstrafe vollstreckt werden. Wir fordern Sie auf, die Strafe binnen 14 Tagen nach Erhalt dieses Schreibens beim Polizeianhaltezentrum Wien, 1090 Wien; Roßauer Lände 7-9 anzutreten. Vori e ,50 2 Melden Sie sich dort in der Zeit von Mo-Do 8-15 Uhr; Fr. 8-13 Uhr und bringen Sie beim Strafantritt dieses Schreiben sowie einen amtlichen Lichtbildausweis mit:. Rechtsgrundlagen: $S 53b/54b des Verwaltungsstrafgesetzes 1991 Bitte beachten Sie: Wenn Sie diese Aufforderung nicht befolgen; müssen Sie damit rechnen; dass Sie zum Strafantritt zwangsweise vorgeführt werden. Den Vollzug einer Ersatzfreiheitsstrafe können Sie dadurch abwenden; dass Sie die ausstehende Geldstrafe sofort einzahlen. Bei Begleichung nur eines Teils der ausstehenden Geldstrafe auch noch während des Strafvollzugs vermindert sich die Dauer der Ersatzfreiheitsstrafe aliquot. Zahlungshinweise: Offener Gesamtbetrag: € 297,50 Empfänger: BH Baden Verwaltungsstrafen Bank: Raiffeisenbank Region Baden IBAN: ATO9 3204 5000 0101 6450 BIC (= SWIFT-Code): RLNWATWBAD (SEPA-Überweisungl) Zahlungsreferenz: BNS2-V-2273325/3 GFN: 2023 32867 Es wird ersucht; die Zahlungsreferenz (falls vorhanden) und als Verwendungszweck den Namen derls Verpflichteten sowie das Aktenkennzeichen anzugeben. Das Polizeianhaltezentrum Wien wird um Vollstreckung der Ersatzfreiheitsstrafe ersucht Für die Bezirkshauptfrau 4eeROsTERRei+ Dieses Schriftstück wurde amtssigniert:. Hinweise finden Sie unter: Www.noe.gv.atamtssignatur AlatssignatUR "
#
# json_output = query_custom_gpt(doc_text)
# print(json_output)
# python_object = convert_json_to_object(json_output)
# print(python_object)