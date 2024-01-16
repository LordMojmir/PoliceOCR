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
    second_String = second_String.replace("Datum", "")
    second_String = second_String.replace("Durchwahl", "")
    second_String = second_String.replace("Bezug", "")

    bearbeiterin_variations = ["Bearbeiterin", "BearbeiterIn", "Bearbeiterlin", "Bearbeitung"]
    name_variations = ["Gegen", "Betrifft", "Herr", "Frau", "Hen", "Erstzfreiheitsstrafe"]

    words = second_String.split()

    def is_potential_name(word, next_word):
        non_name_phrases = {"Stadt", "Gemeinde", "Magistrat", "Wien", "Tel", "Fax", "FAX", "Fax:", "Delikt", "LPD", "BearbeiterIn", "Herr", "Frau"}
        if word in non_name_phrases or next_word in non_name_phrases:
            return False
        return word[0].isupper() and len(word) > 2 and next_word[0].isupper()

    def is_not_Bearbeiterin(word) -> bool:
        word_list = ["Retouren", "Herr"]
        return word not in word_list

    for i in range(len(words)):
        word = words[i]
        similarity_scores = [fuzz.ratio(word, variation) for variation in bearbeiterin_variations]
        max_similarity = max(similarity_scores)
        if max_similarity >= 80:
            words[i] = "BearbeiterIn"

    true_ocr_output2 = ' '.join(words)

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
                #words[i] = "name"
                for j in range(i + 1, len(words) - 1):
                    if(words[j] == "BearbeiterIn"):
                        j = j+3
                    if is_potential_name(words[j], words[j + 1]):
                        name = f"{words[j]} {words[j + 1]}"
                        break
                if name:
                    break

    bearbeiterIn_pattern = r'(BearbeiterIn)\s+([A-Z\u00C4\u00D6\u00DC\u00E4\u00F6\u00FC\u00DF][a-zA-Z\u00E4\u00F6\u00FC\u00DF.]+)\s+([A-Z\u00C4\u00D6\u00DC\u00E4\u00F6\u00FC\u00DF][a-zA-Z\u00E4\u00F6\u00FC\u00DF.]+)'
    date_pattern = r'\d{1,2}\.\d{1,2}\.\d{4}'

    bearbeiterIn_match = re.search(bearbeiterIn_pattern, true_ocr_output2)

    if bearbeiterIn_match:
        if(is_not_Bearbeiterin(bearbeiterIn_match.group(3))):
            bealastname = bearbeiterIn_match.group(3)
        else:
            bealastname = ""
    bearbeiterIn = f"{bearbeiterIn_match.group(2)} {bealastname}"

    birthdate_matches = re.findall(date_pattern, ocr_output)
    if birthdate_matches:
        birthdate_list = [datetime.strptime(date, "%d.%m.%Y") for date in birthdate_matches]
        birthdate = min(birthdate_list).strftime("%d.%m.%Y")

    words = ocr_output.split()

    # Function to check if any fuzz ratio is above 80
    def is_fuzz_ratio_high(word, targets):
        # Remove punctuation from the word
        for punctuation in [",", "."]:
            word = word.replace(punctuation, "")

        for target in targets:
            if fuzz.ratio(word, target) > 80:
                return True

        return False

    firstname, lastname = name.split(" ")
    b_firstname, b_lastname = bearbeiterIn.split(" ")

    # List of target words
    targets = [firstname, lastname, b_firstname, b_lastname]

    # Replace words with high fuzz ratio
    clean_ocr_output = " ".join(["" if is_fuzz_ratio_high(word, targets) else word for word in words])

    # clean_ocr_output = ocr_output.replace(firstname, "").replace(lastname, "").replace(b_firstname, "").replace(b_firstname, "").replace(birthdate, "")

    def correct_name_order(full_name):
        # Teile den Namen in Vor- und Nachnamen
        parts = full_name.split()
        if len(parts) != 2:
            return full_name  # Keine Änderung, wenn das Format nicht passt

        first_name, last_name = parts

        uppercase_count_firstname = sum(1 for c in first_name if c.isupper())
        uppercase_count_lastname = sum(1 for c in last_name if c.isupper())

        if uppercase_count_firstname > uppercase_count_lastname:
            return f"{last_name} {first_name}"

        return full_name

    finalName = correct_name_order(name).replace(",", "").replace(";", "")

    return clean_ocr_output, finalName , bearbeiterIn.replace(",", "") ,birthdate

