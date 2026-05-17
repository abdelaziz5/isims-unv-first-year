import sys

from PyQt5.QtGui import QKeySequence
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QMessageBox, QShortcut

#function for loading the style of the application
def load_style(app):
    with open("style.qss", "r") as file:
        style = file.read()
        app.setStyleSheet(style)

# Function to calculate
def calculer():
    try:
        entier_a = int(window.champ_entier_a.text())
        entier_b = int(window.champ_entier_b.text())
    except ValueError:
        window.champ_entier_a.clear()
        window.champ_entier_b.clear()
        QMessageBox.critical(None, "Error", "Saisir un nombre de type entier.")
    else:
        label_somme_result.setText(f"<b>{entier_a + entier_b}</b>")
        label_diffirence_result.setText(f"<b>{entier_a - entier_b}</b>")
        label_produit_result.setText(f"<b>{entier_a * entier_b}</b>")
        if entier_b != 0:
            label_division_result.setText(f"<b>{entier_a / entier_b}</b>")
            label_division_result.setProperty("status", "normal")
        else:
            label_division_result.setText("Division Impossible (division par zéro)")
            label_division_result.setProperty("status", "error")
        label_division_result.style().unpolish(label_division_result)
        label_division_result.style().polish(label_division_result)


def effacer():
    label_division_result.setProperty("status", "normal")
    label_division_result.style().unpolish(label_division_result)
    label_division_result.style().polish(label_division_result)
    window.champ_entier_a.clear()
    window.champ_entier_b.clear()
    label_somme_result.clear()
    label_diffirence_result.clear()
    label_produit_result.clear()
    label_division_result.clear()
    window.champ_entier_a.setFocus()

def quitter():
    app.quit()
    print(window.width(), window.height())
# Creating the application
app = QApplication(sys.argv)
# Creating the style of the application
load_style(app)
# Creating the window
window = QWidget()
window.setWindowTitle("Calculatrice d'entier")

# Creating widgets
label_entier_a = QLabel("Entier A: ")
window.champ_entier_a = QLineEdit()
window.champ_entier_a.setPlaceholderText("Write a number")
window.champ_entier_a.setFixedWidth(150)
label_entier_b = QLabel("Entier B: ")
window.champ_entier_b = QLineEdit()
window.champ_entier_b.setPlaceholderText("Write a number")
window.champ_entier_b.setFixedWidth(150)

btn_calculer = QPushButton("Calculer")
btn_Effacer = QPushButton("Effacer")
btn_quitter = QPushButton("Quitter")

label_somme = QLabel("Somme: ")
label_somme.setFixedWidth(80)
label_diffirence = QLabel("Diffirence: ")
label_diffirence.setFixedWidth(80)
label_produit = QLabel("Produit: ")
label_produit.setFixedWidth(80)
label_division = QLabel("Division: ")
label_division.setFixedWidth(80)

label_somme_result = QLabel()
label_diffirence_result = QLabel()
label_produit_result = QLabel()
label_division_result = QLabel()

label_note1 = QLabel("Utilisez le raccourci Ctrl+R pour réinitialiser et Ctrl+Q pour quitter.")
label_note1.setObjectName("note1")
label_note2 = QLabel("Appuyez sur Entrée après avoir écrit le premier nombre pour passer au deuxième nombre, et appuyez sur Entrée après avoir écrit le deuxième nombre pour calculer.")
label_note2.setObjectName("note2")
label_note2.setWordWrap(True)
label_note2.setFixedWidth(430)
# Adding the buttons functionality
btn_calculer.clicked.connect(calculer)
btn_Effacer.clicked.connect(effacer)
btn_quitter.clicked.connect(quitter)

# Show widgets and set the layout for the window
layoutV = QVBoxLayout()

layout_row_a = QHBoxLayout()
layout_row_a.addWidget(label_entier_a)
layout_row_a.addWidget(window.champ_entier_a)
layout_row_a.setSpacing(20)
layout_row_a.addStretch()

layout_row_b = QHBoxLayout()
layout_row_b.addWidget(label_entier_b)
layout_row_b.addWidget(window.champ_entier_b)
layout_row_b.setSpacing(20)
layout_row_b.addStretch()


layout_row_btn = QHBoxLayout()
layout_row_btn.addWidget(btn_calculer)
layout_row_btn.addWidget(btn_Effacer)
layout_row_btn.addWidget(btn_quitter)

layout_row_somme = QHBoxLayout()
layout_row_somme.addWidget(label_somme)
layout_row_somme.addWidget(label_somme_result)
layout_row_somme.setSpacing(20)
layout_row_somme.addStretch()

layout_row_difference = QHBoxLayout()
layout_row_difference.addWidget(label_diffirence)
layout_row_difference.addWidget(label_diffirence_result)
layout_row_difference.setSpacing(20)
layout_row_difference.addStretch()

layout_row_produit = QHBoxLayout()
layout_row_produit.addWidget(label_produit)
layout_row_produit.addWidget(label_produit_result)
layout_row_produit.setSpacing(20)
layout_row_produit.addStretch()

layout_row_division = QHBoxLayout()
layout_row_division.addWidget(label_division)
layout_row_division.addWidget(label_division_result)
layout_row_division.setSpacing(20)
layout_row_division.addStretch()

layoutV.addWidget(label_note1)
layoutV.addWidget(label_note2)
layoutV.addLayout(layout_row_a)
layoutV.addLayout(layout_row_b)
layoutV.addLayout(layout_row_btn)
layoutV.addLayout(layout_row_somme)
layoutV.addLayout(layout_row_difference)
layoutV.addLayout(layout_row_produit)
layoutV.addLayout(layout_row_division)

window.setLayout(layoutV)
# User experience
window.champ_entier_a.setFocus()
window.champ_entier_a.returnPressed.connect(window.champ_entier_b.setFocus)
window.champ_entier_b.returnPressed.connect(btn_calculer.click)

shortcut_reset = QShortcut(QKeySequence("Ctrl+R"), window)
shortcut_reset.activated.connect(effacer)

shortcut_quit = QShortcut(QKeySequence("Ctrl+Q"), window)
shortcut_quit.activated.connect(quitter)
# Window dynamic size
window.resize(438, 324)
# Open the window
window.show()
# Exit the application
sys.exit(app.exec_())
