from datetime import datetime
import re
from thefuzz import fuzz
from typing import Tuple

def making_OCR_gdpr_conform(ocr_output: str) -> Tuple[str, str, str, str]:
    name = ""
    bearbeiterIn = ""
    birthdate = ""

    split_string = ocr_output.split("Second OCR:")
    second_String = split_string[-1]

    bearbeiterin_variations = ["Bearbeiterin", "BearbeiterIn", "Bearbeiterlin", "Bearbeitung"]
    name_variations = ["Gegen", "Betrifft", "Herr", "Frau", "Hen"]

    words = second_String.split()

    def is_potential_name(word, next_word):
        non_name_phrases = {"Stadt", "Gemeinde", "Magistrat", "Wien", "Tel", "Fax", "FAX", "Fax:"}
        if word in non_name_phrases or next_word in non_name_phrases:
            return False
        return word[0].isupper() and not word.isupper() and next_word[0].isupper() and not next_word.isupper()


    for i, word in enumerate(words):
        similarity_scores = [fuzz.ratio(word, variation) for variation in name_variations]
        max_similarity = max(similarity_scores)
        if max_similarity >= 80 and i + 2 < len(words):
            potential_name = f"{words[i + 1]} {words[i + 2]}"
            if is_potential_name(words[i + 1], words[i + 2]):
                name = potential_name
                break

    if not name:
        for i, word in enumerate(words):
            similarity_scores = [fuzz.ratio(word, variation) for variation in name_variations]
            max_similarity = max(similarity_scores)
            if max_similarity >= 80:
                words[i] = "name"
                for j in range(i + 1, len(words) - 1):
                    if is_potential_name(words[j], words[j + 1]):
                        name = f"{words[j]} {words[j + 1]}"
                        break
                if name:
                    break


    for i in range(len(words)):
        word = words[i]
        similarity_scores = [fuzz.ratio(word, variation) for variation in bearbeiterin_variations]
        max_similarity = max(similarity_scores)
        if max_similarity >= 80:
            words[i] = "BearbeiterIn"

    true_ocr_output2 = ' '.join(words)

    bearbeiterIn_pattern = r'(BearbeiterIn)\s+([A-Z][a-z]+)\s+([A-Z][a-z]+)'
    date_pattern = r'\d{1,2}\.\d{1,2}\.\d{4}'

    bearbeiterIn_match = re.search(bearbeiterIn_pattern, true_ocr_output2)

    if bearbeiterIn_match:
        bearbeiterIn = f"{bearbeiterIn_match.group(2)} {bearbeiterIn_match.group(3)}"

    birthdate_matches = re.findall(date_pattern, ocr_output)
    if birthdate_matches:
        birthdate_list = [datetime.strptime(date, "%d.%m.%Y") for date in birthdate_matches]
        birthdate = min(birthdate_list).strftime("%d.%m.%Y")

    clean_ocr_output = ocr_output.replace(name, "").replace(bearbeiterIn, "").replace(birthdate, "")

    return clean_ocr_output, name, bearbeiterIn, birthdate



if __name__ == '__main__':

    # clean_ocr_output, name, bearbeiterIn, birthdate = making_OCR_gdpr_conform(text)

    # print(name)