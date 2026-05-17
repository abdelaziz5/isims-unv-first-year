import json
from math import log

def update_tf_idf_numberOfDocuments(json_file):
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    data["total_documents"] = data["total_documents"] + 1
    with open("IDF.json", 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4)

def update_tf_idf_word_count(json_file, word):
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    if word in data["weight"]:
        data["weight"][word] = data["weight"][word] + 1
    else:
        data["weight"][word] = 1
    with open("IDF.json", 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4)

def get_tf_idf(word, count, total_count_mots, json_file):
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    TF = count / total_count_mots
    print(data["total_documents"]/ (1 + data["weight"][word]))
    IDF = log(data["total_documents"]/ (1 + data["weight"][word]))
    return TF * IDF

def text_analyser(phrase):
    seperators = " \n,;:!?.-_+-/\\|@#$%^&*()[]{}\"'`~"
    # ok_words = " ".join(["D'ACCORD", "D'ANTAN", "D'HABITUDE", "D'AILLEURS", "D'AVENTURE", "D'EMBLÉE", "D'AUTANT", "AUJOURD'HUI"]).lower().split()
    # print(ok_words)
    ok_words = ["d'accord", "d'antan", "d'habitude", "d'ailleurs", "d'aventure", "d'emblée", "d'autant", "aujourd'hui"]

    with open("stopwords.txt", 'r', encoding='utf-8') as f:
        stopwords = f.read().strip().split("\n")
    long=len(phrase)
    d = {}
    i = 0
    nb = 0
    while i < (long):
        if phrase[i] in seperators:
            i += 1
        else:
            word_begening = i
            while i < long and phrase[i] not in seperators:
                i += 1
            if i < long and phrase[i] == "'":
                placement = i
                i += 1
                while i < long and phrase[i] not in seperators:
                    i += 1
                word_end = i
                if (p:=phrase[word_begening:word_end].lower()) in ok_words:
                    if p not in stopwords:
                        if p not in d:
                            d[p] = {'count': 0, 'tf-idf': 0.0}
                            update_tf_idf_word_count('IDF.json', p)
                        d[p]["count"] = d[p]["count"] + 1
                        nb = nb + 1
                else:
                    if phrase[word_end - 1] in seperators:
                        p = phrase[word_begening:word_end-1].lower()
                        if p not in stopwords:
                            if p not in d:
                                d[p] = {'count': 0, 'tf-idf': 0.0}
                                update_tf_idf_word_count('IDF.json', p)
                            d[p]["count"] = d[p]["count"] + 1
                            nb = nb + 1
                    else:
                        p = phrase[word_begening:placement].lower()
                        if p not in stopwords:
                            if p not in d:
                                d[p] = {'count': 0, 'tf-idf': 0.0}
                                update_tf_idf_word_count('IDF.json', p)
                            d[p]["count"] = d[p]["count"] + 1
                            nb = nb + 1
                        p=phrase[placement+1:word_end].lower()
                        if p not in stopwords:
                            if p not in d:
                                d[p] = {'count': 0, 'tf-idf': 0.0}
                                update_tf_idf_word_count('IDF.json', p)
                            d[p]["count"] = d[p]["count"] + 1
                            nb = nb + 1
            else:
                word_end = i
                p=phrase[word_begening:word_end].lower()
                if p not in stopwords:
                    if p not in d:
                        d[p] = {'count': 0, 'tf-idf': 0.0}
                        update_tf_idf_word_count('IDF.json', p)
                    d[p]["count"] = d[p]["count"] + 1
                    nb = nb + 1

    for word in d:
        d[word]["tf-idf"] = get_tf_idf(word,d[word]["count"],nb, "IDF.json")
    sorted_d = dict(sorted(d.items(), key = lambda item: item[1]["tf-idf"], reverse = True))
    return sorted_d, nb

if __name__ == "__main__":
    phrase = input("Ecrire une phrase: ")
    if phrase != "":
        update_tf_idf_numberOfDocuments("IDF.json")
    d, nb = text_analyser(phrase)
    taille_column=15
    print("┌","─" * taille_column, "┬", "─" * taille_column,"┬", "─" * taille_column, "┐", sep="")
    print(f"│{"Word":^{taille_column}}│{"Count":^{taille_column}}│{"TF-IDF":^{taille_column}}│")
    print("├", "─" * taille_column, "┼", "─" * taille_column,"┼", "─" * taille_column, "┤", sep="")

    for key, value in d.items():
        print(f"│{key:<{taille_column}}│{value["count"]:<{taille_column}}│{value["tf-idf"]:<{taille_column}.10f}│")

    print("└","─" * taille_column, "┴", "─" * taille_column,"┴", "─" * taille_column, "┘", sep="")
    print("Mots totale:", nb)









