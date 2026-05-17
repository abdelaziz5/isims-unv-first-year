import os
import io
import csv
import json
from docx import Document # Requires: pip install python-docx
from spire.doc import Document as DocumentDoc
import math


def load_file_content(file_path):
    """
    Reads a file and returns (content, extension).
    Handles .txt, .csv, .json, and .docx.
    """
    if not os.path.exists(file_path):
        return None, None

    # Get the extension (e.g., '.csv', '.txt')
    _, extension = os.path.splitext(file_path.lower())

    try:
        if extension == '.txt':
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read(), extension

        elif extension == '.csv':
            with open(file_path, 'r', encoding='utf-8') as f:
                # Reading as DictReader as requested in the project
                reader = csv.DictReader(f)
                data = list(reader)
                return data, extension

        elif extension == '.json':
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                # Return pretty-printed string for the UI
                return data, extension

        elif extension == '.docx':
            doc = Document(file_path)
            full_text = [para.text for para in doc.paragraphs]
            return '\n'.join(full_text), extension

        elif extension == '.doc':
            return (read_doc_legacy(file_path), extension)
        else:
            return "Unsupported format", extension

    except Exception as e:
        return f"Error: {str(e)}", extension


def convert_txt_to_json(text, file_path):
    """
    Reads a structured text (key:value) and saves it as .json.
    """
    data_dict = {}
    try:

        for line in text.splitlines():
            line = line.strip()
            if ':' in line:
                # Split at the first colon
                key, value = line.split(':', 1)
                data_dict[key.strip()] = value.strip()

        json_output = json.dumps(data_dict, indent=4, ensure_ascii=False)

        # Get the extension (e.g., '.csv', '.txt')
        directory = os.path.dirname(file_path)
        # os.path.basename gives just 'data.txt'
        base_name = os.path.basename(file_path)
        # name_only gives 'data'
        name_only, _ = os.path.splitext(base_name)

        full_path = os.path.join(directory, f"{name_only}.json")

        with open(full_path, 'w', encoding='utf-8') as json_file:
            json_file.write(json_output)
        return json_output
    except Exception as e:
        return f"Error: {str(e)}"


def convert_csv_to_json(csv_data, file_path):
    """
    Takes the list of dicts (csv_data) and saves it as a .json file.
    """
    try:
        # Ensure we are actually dealing with the list of dictionaries
        if not isinstance(csv_data, list):
            print("Error: CSV data must be a list of dictionaries.")
            return

        json_output = json.dumps(csv_data, indent=4, ensure_ascii=False)

        directory = os.path.dirname(file_path)
        base_name = os.path.basename(file_path)
        name_only, _ = os.path.splitext(base_name)

        full_path = os.path.join(directory, f"{name_only}.json")

        # 2. Writing the JSON
        with open(full_path, 'w', encoding='utf-8') as json_file:
            json_file.write(json_output)

        return json_output  # Returning the path so the UI can auto-load it

    except Exception as e:
        return f"Error converting CSV: {str(e)}"


def convert_json_to_csv(json_data, file_path):
    try:
        if not isinstance(json_data, list) or len(json_data) == 0:
            return f"Error: JSON data must be a non-empty list of dictionaries."

        # 1. Generate the CSV text in memory (RAM)
        output = io.StringIO()
        keys = json_data[0].keys()
        writer = csv.DictWriter(output, fieldnames=keys)

        writer.writeheader()
        writer.writerows(json_data)

        csv_text = output.getvalue()  # This is your clean string!

        # 2. Save to disk (Optional)
        directory = os.path.dirname(file_path)
        name_only = os.path.splitext(os.path.basename(file_path))[0]
        full_path = os.path.join(directory, f"{name_only}.csv")

        with open(full_path, 'w', encoding='utf-8', newline='') as csv_file:
            csv_file.write(csv_text)

        # 3. Return the clean text for the UI
        return csv_text

    except Exception as e:
        return f"Error converting to CSV: {str(e)}"

def convert_doc_docx_to_txt(text, file_path):
    directory = os.path.dirname(file_path)
    base_name = os.path.basename(file_path)
    name_only, _ = os.path.splitext(base_name)

    full_path = os.path.join(directory, f"{name_only}.txt")
    with open(full_path, 'w', encoding='utf-8') as text_file:
        text_file.write(text)
    return text


# def insert_line_to_csv(data_dict, file_path):
#     """
#     Appends a new dictionary as a row to the CSV.
#     data_dict: e.g., {'nom': 'Masmoudi', 'prenom': 'Abdelaziz', 'note': '18'}
#     """
#     try:
#         # 1. We need to know the existing headers to align the new row
#         with open(file_path, 'r', encoding='utf-8') as f:
#             reader = csv.DictReader(f)
#             fieldnames = reader.fieldnames
#
#         # 2. Append the new data
#         with open(file_path, 'a', encoding='utf-8', newline='') as f:
#             writer = csv.DictWriter(f, fieldnames=fieldnames)
#             writer.writerow(data_dict)
#
#         return True, "Insertion successful"
#     except Exception as e:
#         return False, str(e)
#
#
# def delete_line_from_csv(file_path, row_index):
#     """
#     Deletes a specific row from a CSV based on its index.
#     row_index: The integer index of the row to remove (0-based).
#     """
#     try:
#         # 1. Read all existing data into a list
#         rows = []
#         fieldnames = []
#         with open(file_path, 'r', encoding='utf-8') as f:
#             reader = csv.DictReader(f)
#             fieldnames = reader.fieldnames
#             rows = list(reader)
#
#         # 2. Check if the index is valid
#         if 0 <= row_index < len(rows):
#             # Remove the row from the list
#             rows.pop(row_index)
#         else:
#             return False, "Index out of range."
#
#         # 3. Overwrite the file with the remaining rows
#         with open(file_path, 'w', encoding='utf-8', newline='') as f:
#             writer = csv.DictWriter(f, fieldnames=fieldnames)
#             writer.writeheader()
#             writer.writerows(rows)
#
#         return True, "Line deleted successfully."
#     except Exception as e:
#         return False, str(e)


def sauvegarder_csv(data, file_path):
    """
    Saves a list of dictionaries back to a CSV file.
    """
    try:
        if not data:
            return False, "Aucune donnée à sauvegarder."

        # Get headers from the first dictionary
        headers = list(data[0].keys())

        with open(file_path, 'w', encoding='utf-8', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=headers)
            writer.writeheader()
            writer.writerows(data)

        return True, "Fichier sauvegardé avec succès."
    except Exception as e:
        return False, str(e)

def obtenir_stats_fichier(path):
    """
    Calcule les statistiques et les retourne sous forme de dictionnaire.
    """
    if os.path.exists(path) and path.endswith(".txt"):
        n_lines = 0
        n_caracters_with_spaces = 0
        n_caracters_without_spaces = 0
        all_words = []
        longest_line_len = 0

        try:
            with open(path, 'r', encoding="utf-8") as file:
                for line in file:
                    n_lines += 1
                    line_len = len(line)
                    if line_len > longest_line_len:
                        longest_line_len = line_len

                    n_caracters_with_spaces += line_len
                    words_in_line = line.split()
                    for word in words_in_line:
                        all_words.append(word.lower())
                        n_caracters_without_spaces += len(word)

            # Analyse de fréquence
            word_freq = {}
            for word in all_words:
                word_freq[word] = word_freq.get(word, 0) + 1

            sorted_words = sorted(word_freq.items(), key=lambda item: item[1], reverse=True)
            top_5 = sorted_words[:5]

            return {
                "lignes": n_lines,
                "mots": len(all_words),
                "carac_espaces": n_caracters_with_spaces,
                "carac_sans_espaces": n_caracters_without_spaces,
                "ligne_longue": longest_line_len,
                "top_mots": top_5
            }
        except Exception as e:
            print(f"Erreur de lecture : {e}")
            return None
    return None


def calculer_stats_csv(data_list):
    if not data_list or not isinstance(data_list, list):
        return None

    # Identify columns that contain numbers
    headers = data_list[0].keys()
    numeric_stats = {}

    for header in headers:
        # Extract values and try to convert to float
        valeurs = []
        for row in data_list:
            try:
                val = float(row[header])
                valeurs.append(val)
            except (ValueError, TypeError):
                continue

        # Only calculate if we found numeric data in this column
        if valeurs:
            N = len(valeurs)
            moy = sum(valeurs) / N
            v_min = min(valeurs)
            v_max = max(valeurs)

            # Standard Deviation (Écart-type) formula: sqrt( sum((xi - moy)²) / N )
            variance = sum((x - moy) ** 2 for x in valeurs) / N
            ecart_type = math.sqrt(variance)

            numeric_stats[header] = {
                "moyenne": round(moy, 2),
                "min": round(v_min, 2),
                "max": round(v_max, 2),
                "ecart_type": round(ecart_type, 2)
            }

    return {"total_lignes": len(data_list), "colonnes": numeric_stats}
# Help functions

def read_doc_legacy(file_path):
    """
    Simplest way to read .doc on Windows without needing MS Word installed.
    """
    try:
        # Load the document
        doc = DocumentDoc()
        doc.LoadFromFile(file_path)

        # Get the entire text content in one go
        text = doc.GetText()

        doc.Close()

        # Remove watermark
        lines = text.split("\n")
        if "Evaluation" in lines[0]:
            text = "\n".join(lines[1:])

        return text
    except Exception as e:
        return f"Error reading .doc file: {str(e)}"