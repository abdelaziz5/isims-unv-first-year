
#######################################################################################################################
# For this page to work You need to have words_engine.py & IDF.json & stopwords & Style.qss Files in the same folder! #
#######################################################################################################################

import sys
from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QHBoxLayout,
    QVBoxLayout,
    QTextEdit,
    QPushButton,
    QLabel,
    QTableWidget,
    QHeaderView,
    QTableWidgetItem,
    QShortcut
)
from PyQt5.QtGui import QKeySequence
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from functools import partial
from words_engine import text_analyser, update_tf_idf_numberOfDocuments

def load_stylesheet(app):
    with open("style.qss", "r") as file:
        style = file.read()
        app.setStyleSheet(style)

def mettre_a_jour_compteur(text_edit, label) :
    compteur(text_edit, label)
def compter_mots(texte) :
        return text_analyser(texte)

def compteur(text_edit, label) :
    """
    Lit le texte de la zone de saisie et met
    à jour le label avec le nombre de mots.
    """
    texte = text_edit.toPlainText()
    if texte != "":
        update_tf_idf_numberOfDocuments("IDF.json")
        d,nb = compter_mots(texte)
        label.setText(f"Nombre de mots : {nb}")
        # I'm adding the Qtable next
        if nb != 0:
            table.setRowCount(0)
            for row, (word, prop) in enumerate(d.items()):
                table.insertRow(row)
                table.setItem(row, 0, QTableWidgetItem(word))
                table.setItem(row, 1, QTableWidgetItem(str(prop["count"])))
                table.setItem(row, 2, QTableWidgetItem(str(f"{prop["tf-idf"]:.4f}")))
def effacer_contenu(text_edit, label) :
    """
    Efface la zone de texte et réinitialise le label.
    """
    text_edit.clear()
    table.setRowCount(1)
    table.clearContents()
    label.setText("Nombre de mots : 0")
    # (Optionnel) replacer le focus dans la zone de texte :
    text_edit.setFocus()


app = QApplication(sys.argv)
# Set the style
load_stylesheet(app)
# Fenêtre principale
fen = QWidget()
fen.setWindowTitle("Compteur de mots")
fen.resize(900, 600)

# Mise en page principale verticale
layout = QVBoxLayout(fen)

# Zone de texte très large
text_edit = QTextEdit()
text_edit.setPlaceholderText("Saisissez (ou collez) votre texte ici...")
text_edit.setFont(QFont("Segoe UI", 11))
text_edit.setMinimumHeight(420)

# Zone table
table = QTableWidget()
table.setColumnCount(3)
table.setHorizontalHeaderLabels(["word", "Count", "TF-IDF"])
table.setRowCount(1)
table.verticalHeader().setVisible(True)

header = table.horizontalHeader()
header.setMinimumSectionSize(80)
header.setSectionResizeMode(0,QHeaderView.Stretch)
header.setSectionResizeMode(1,QHeaderView.ResizeToContents)
header.setSectionResizeMode(2,QHeaderView.ResizeToContents)

# layout Text and table together
textable = QHBoxLayout()
textable.addWidget(text_edit, stretch=2)
textable.addWidget(table, stretch=1)

layout.addLayout(textable)

# Ligne de boutons (Calculer + Effacer)
ligne_boutons = QHBoxLayout()
bouton_calculer = QPushButton("Calculer")
bouton_calculer.setFont(QFont("Segoe UI", 11, QFont.Bold))
bouton_calculer.setCursor(Qt.PointingHandCursor)
bouton_calculer.setObjectName("bouton_calculer")

bouton_effacer = QPushButton("Effacer")
bouton_effacer.setFont(QFont("Segoe UI", 11))
bouton_effacer.setCursor(Qt.PointingHandCursor)
bouton_effacer.setObjectName("bouton_effacer")

ligne_boutons.addWidget(bouton_calculer)
ligne_boutons.addWidget(bouton_effacer)
layout.addLayout(ligne_boutons)

# Label de résultat en bas
label = QLabel("Nombre de mots : 0")
label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
label.setFont(QFont("Segoe UI", 11))
layout_labels = QHBoxLayout()
layout_labels.addWidget(label)

layout_labels.addStretch()

# Label note
label_note = QLabel("Use Ctrl+R to reset & Ctrl+E to calculate.")
label_note.setFont(QFont("Segoe UI", 11))
label_note.setStyleSheet("color: #7777ff")

layout_labels.addWidget(label_note)

layout.addLayout(layout_labels)
#User Experience
shortcut_reset = QShortcut(QKeySequence("Ctrl+R"), fen)
shortcut_reset.activated.connect(partial(effacer_contenu, text_edit, label))

shortcut_calculate = QShortcut(QKeySequence("Ctrl+E"), fen)
shortcut_calculate.activated.connect(partial(compteur, text_edit, label))
# Connexions (sans fonction imbriquée)
bouton_calculer.clicked.connect(partial(compteur, text_edit, label))
bouton_effacer.clicked.connect(partial(effacer_contenu, text_edit, label))

# (Optionnel) comptage en temps réel :
# text_edit.textChanged.connect(partial(mettre_a_jour_compteur, text_edit, label))

fen.show()
sys.exit(app.exec_())

