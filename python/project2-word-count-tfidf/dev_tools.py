import json
def reset_IDF(json_file):
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump({"total_documents": 0, "weight": {}}, f, indent=4)

if __name__ == "__main__":
    reset_IDF('IDF.json')