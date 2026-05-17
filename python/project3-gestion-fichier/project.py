import sys
import os
from PyQt5.QtWidgets import (QApplication,
                             QWidget,
                             QVBoxLayout,
                             QPushButton,
                             QTextEdit,
                             QSplitter,
                             QLabel,
                             QFileDialog,
                             QDialog,
                             QTableWidget,
                             QHBoxLayout,
                             QTableWidgetItem,
                             QMessageBox)
from PyQt5.QtCore import Qt

from functions import ( load_file_content,
                        obtenir_stats_fichier,
                        convert_txt_to_json,
                        convert_csv_to_json,
                        convert_json_to_csv,
                        convert_doc_docx_to_txt,
                        sauvegarder_csv,
                        calculer_stats_csv,)





class FileManagerApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # --- Window Configuration ---
        self.setWindowTitle('=== Application de Gestion de Fichiers ===')
        self.setGeometry(100, 100, 900, 700)

        # 1. Create the Main Layout
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        # 2. Define the Buttons
        self.btn_read = QPushButton("1. Lire et afficher un fichier (txt / csv / json / docx / doc)")
        self.btn_stats = QPushButton("2. Afficher les statistiques d'un fichier texte")
        self.btn_conv_txt_json = QPushButton("3a. Convertir TXT → JSON")
        self.btn_conv_csv_json = QPushButton("3b. Convertir CSV → JSON")
        self.btn_conv_json_csv = QPushButton("3c. Convertir JSON → CSV")
        self.btn_conv_docx_txt = QPushButton("3d. Convertir DOCX/DOC → TXT")
        self.btn_modify_csv = QPushButton("4. Modifier un fichier CSV (ajout / suppression)")

        # 3. Add Buttons to the Layout
        self.layout.addWidget(self.btn_read)
        self.layout.addWidget(self.btn_stats)
        self.layout.addWidget(self.btn_conv_txt_json)
        self.layout.addWidget(self.btn_conv_csv_json)
        self.layout.addWidget(self.btn_conv_json_csv)
        self.layout.addWidget(self.btn_conv_docx_txt)
        self.layout.addWidget(self.btn_modify_csv)

        # --- Path Display ---
        self.label_path = QLabel("Aucun fichier sélectionné")

        # 1. Center the text
        self.label_path.setAlignment(Qt.AlignCenter)

        # 2. Fix the height so it doesn't take extra vertical space
        self.label_path.setFixedHeight(30)

        self.layout.addWidget(self.label_path)

        self.label_csv = QLabel("")
        self.label_csv.setFixedHeight(60)
        self.label_csv.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.label_csv)
        # 4. --- The Affichage Area (Split View) ---
        # 1. Create the Splitter (Horizontal means the divider is vertical)
        self.container_affichage = QSplitter(Qt.Horizontal)

        # 2. Left Display (The "Before" / Original)
        self.zone_gauche = QTextEdit()
        self.zone_gauche.setReadOnly(True)
        self.zone_gauche.setPlaceholderText("Affichage (Original)...")

        # 3. Right Display (The "After" / Result)
        self.zone_droite = QTextEdit()
        self.zone_droite.setReadOnly(True)
        self.zone_droite.setPlaceholderText("Affichage (Résultat)...")

        # 4. Add the zones into the splitter
        self.container_affichage.addWidget(self.zone_gauche)
        self.container_affichage.addWidget(self.zone_droite)

        # 5. Add the splitter to the main vertical layout
        self.layout.addWidget(self.container_affichage)

        # Chosing the path
        self.btn_read.clicked.connect(self.open_file)
        # Display the stats of a text file
        self.btn_stats.clicked.connect(self.display_stats)
        # Convert text to json
        self.btn_conv_txt_json.clicked.connect(self.handle_txt_to_json)
        # Convert CSV to json
        self.btn_conv_csv_json.clicked.connect(self.handle_csv_to_json)
        # Convert json to CSV
        self.btn_conv_json_csv.clicked.connect(self.handle_json_to_csv)
        # Convert Docx/Doc to txt
        self.btn_conv_docx_txt.clicked.connect(self.handle_docx_doc_to_txt)
        # Edit CSV file
        self.btn_modify_csv.clicked.connect(self.handle_modify_csv)
        # disable buttons
        self.update_button_states(None)

    def update_button_states(self, extension):
        """
        Enables or disables buttons based on the file extension.
        """
        # First, disable all conversion/stats buttons by default
        self.btn_stats.setEnabled(False)
        self.btn_conv_txt_json.setEnabled(False)
        self.btn_conv_csv_json.setEnabled(False)
        self.btn_conv_json_csv.setEnabled(False)
        self.btn_conv_docx_txt.setEnabled(False)
        self.btn_modify_csv.setEnabled(False)

        # Now, enable only what makes sense
        if extension == ".txt":
            self.btn_stats.setEnabled(True)
            self.btn_conv_txt_json.setEnabled(True)
        elif extension == ".csv":
            self.btn_conv_csv_json.setEnabled(True)
            self.btn_modify_csv.setEnabled(True)
        elif extension == ".json":
            self.btn_conv_json_csv.setEnabled(True)
        elif extension in [".docx", ".doc"]:
            self.btn_conv_docx_txt.setEnabled(True)

    def open_file(self):
        self.label_csv.setText("")
        self.zone_droite.clear()
        filters = "Tous les fichiers supportés (*.txt *.csv *.json *.docx *.doc);;..."
        path, _ = QFileDialog.getOpenFileName(self, "Ouvrir un fichier", "", filters)

        if path:
            self.current_file_path = path
            extension = os.path.splitext(path)[1].lower()  # Gets '.csv', '.txt', etc.

            self.label_path.setText(f"Fichier : {os.path.basename(path)}")

            # 1. Update Buttons
            self.update_button_states(extension)

            # 2. Show content on the LEFT
            try:
                # Using the function we built in the previous sessions
                self.content, _ = load_file_content(path)

                # If it's a list (CSV/JSON data), format it nicely for the text box
                if extension == ".csv" and isinstance(self.content, list) and len(self.content) > 0:
                    # 1. Get headers from the first dictionary
                    headers = self.content[0].keys()
                    display_text = " , ".join(headers) + "\n"  # Add header row

                    # 2. Add each row's values
                    for row in self.content:
                        # row.values() gives us the data without the keys/colons
                        display_text += " , ".join(map(str, row.values())) + "\n"

                    self.zone_gauche.setPlainText(display_text)
                    self.update_csv_stats_display()
                elif isinstance(self.content, list):
                    display_text = ""
                    for row in self.content:
                        display_text += str(row) + "\n"
                    self.zone_gauche.setPlainText(display_text)
                else:
                    self.zone_gauche.setPlainText(str(self.content))


                self.zone_droite.setPlaceholderText("En attente de l'opération...")

            except Exception as e:
                self.zone_gauche.setPlainText(f"Erreur : {e}")

    def display_stats(self):
        # We use the path we saved earlier!
        stats = obtenir_stats_fichier(self.current_file_path)

        if stats:
            # We format the dictionary into a readable string
            res = "=== STATISTIQUES DU FICHIER ===\n\n"
            res += f"• Nombre de lignes : {stats['lignes']}\n"
            res += f"• Nombre de mots : {stats['mots']}\n"
            res += f"• Caractères (avec espaces) : {stats['carac_espaces']}\n"
            res += f"• Caractères (sans espaces) : {stats['carac_sans_espaces']}\n"
            res += f"• Ligne la plus longue : {stats['ligne_longue']} car.\n\n"

            res += "--- TOP 5 MOTS LES PLUS FRÉQUENTS ---\n"
            for word, freq in stats['top_mots']:
                res += f"- {word} : {freq} fois\n"

            self.zone_droite.setPlainText(res)
        else:
            self.zone_droite.setPlainText("Erreur : Impossible de calculer les stats.")

    def handle_txt_to_json(self):
        # 1. Call the logic function
        json_result = convert_txt_to_json(self.content,self.current_file_path)

        # 2. Show the result on the RIGHT side
        self.zone_droite.setPlainText(json_result)

        # 3. Optional: Add a little status message
        self.label_path.setText(f"Converting : {os.path.basename(self.current_file_path)} → JSON")
    def handle_csv_to_json(self):
        json_result = convert_csv_to_json(self.content, self.current_file_path)

        self.zone_droite.setPlainText(json_result)

        self.label_path.setText(f"Converting : {os.path.basename(self.current_file_path)} → JSON")
    def handle_json_to_csv(self):
        csv_result = convert_json_to_csv(self.content, self.current_file_path)

        self.zone_droite.setPlainText(csv_result)

        self.label_path.setText(f"Converting : {os.path.basename(self.current_file_path)} → CSV")

    def handle_docx_doc_to_txt(self):
        txt_output = convert_doc_docx_to_txt(self.content, self.current_file_path)
        self.zone_droite.setPlainText(txt_output)
        self.label_path.setText(f"Converting : {os.path.basename(self.current_file_path)} → TXT")

    def handle_modify_csv(self):
        # 1. (Keep your existing display logic)
        display_text = "--- Données CSV Actuelles ---\n"
        for row in self.content:
            display_text += str(row) + "\n"
        self.zone_droite.setPlainText(display_text)

        # 2. Open the Editor Window
        self.editor = CSVEditorWindow(self.content, self)

        # If the user clicks "Save and Close" (self.accept() was called)
        if self.editor.exec_() == QDialog.Accepted:
            success, message = sauvegarder_csv(self.content, self.current_file_path)

            if success:
                # 4. Refresh the displays to show the new data
                self.label_path.setText(f"Modifié : {os.path.basename(self.current_file_path)}")

                # Update the LEFT zone with the new content
                new_display = ""
                header = self.content[0].keys()
                new_display += " , ".join(header) + "\n"
                for row in self.content:
                    new_display +=  " , ".join(map(str, row.values())) + "\n"
                self.zone_droite.setPlainText(new_display)
                self.update_csv_stats_display()
            else:
                QMessageBox.critical(self, "Erreur", f"Échec de la sauvegarde : {message}")

    def update_csv_stats_display(self):
        stats = calculer_stats_csv(self.content)

        if not stats:
            return

        res = f"=== ANALYSE CSV (N={stats['total_lignes']}) ===\n"
        for col, s in stats['colonnes'].items():
            res += f"• {col} -> Moy: {s['moyenne']} | Min: {s['min']} | Max: {s['max']} | σ: {s['ecart_type']}\n"

        # You can display this in the zone_droite or a new label
        self.label_csv.setText(res)


class CSVEditorWindow(QDialog):
    def __init__(self, data, parent=None):
        super().__init__(parent)
        self.data = data  # This is your list of dicts
        self.setWindowTitle("Éditeur de données CSV")
        self.resize(600, 400)

        self.layout = QVBoxLayout(self)

        # 1. The Table
        self.table = QTableWidget()
        self.setup_table()
        self.layout.addWidget(self.table)

        # 2. Buttons Layout
        self.buttons_layout = QHBoxLayout()
        self.btn_add = QPushButton("Ajouter une ligne")
        self.btn_delete = QPushButton("Supprimer la sélection")
        self.btn_save = QPushButton("Enregistrer les modifications")

        self.buttons_layout.addWidget(self.btn_add)
        self.buttons_layout.addWidget(self.btn_delete)
        self.buttons_layout.addWidget(self.btn_save)
        self.layout.addLayout(self.buttons_layout)

        self.btn_add.clicked.connect(self.add_row)
        self.btn_delete.clicked.connect(self.delete_row)
        self.btn_save.clicked.connect(self.save_and_close)

    def setup_table(self):
        if not self.data: return

        # Set Column Headers
        headers = list(self.data[0].keys())
        self.table.setColumnCount(len(headers))
        self.table.setHorizontalHeaderLabels(headers)

        # Set Row Count and Data
        self.table.setRowCount(len(self.data))
        for i, row_dict in enumerate(self.data):
            for j, (key, value) in enumerate(row_dict.items()):
                self.table.setItem(i, j, QTableWidgetItem(str(value)))

        # Make the columns stretch to fit
        self.table.horizontalHeader().setStretchLastSection(True)

    def delete_row(self):
        # Get the current selected row index
        current_row = self.table.currentRow()

        # If no row is selected, currentRow() returns -1
        if current_row < 0:
            QMessageBox.warning(self, "Sélection", "Veuillez sélectionner une ligne à supprimer.")
            return

        # The confirmation message
        reply = QMessageBox.question(self, 'Confirmation',
                                     "Êtes-vous sûr de vouloir supprimer cette ligne ?",
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            # 1. Remove from the visual table
            self.table.removeRow(current_row)
            # 2. Remove from the internal list (self.data)
            self.data.pop(current_row)

            QMessageBox.information(self, "Succès", "Ligne supprimée avec succès.")

    def add_row(self):
        row_count = self.table.rowCount()
        self.table.insertRow(row_count)

        # # We also need to add an empty dictionary to our internal data
        # # so it stays synchronized with the number of rows
        # new_empty_dict = {key: "" for key in self.data[0].keys()}
        # self.data.append(new_empty_dict)

        # Scroll to the new row so the user sees it
        self.table.scrollToBottom()

    def save_and_close(self):
        # Extract data from table rows
        new_data = []
        for i in range(self.table.rowCount()):
            row_dict = {}
            for j in range(self.table.columnCount()):
                header = self.table.horizontalHeaderItem(j).text()
                item = self.table.item(i, j)
                row_dict[header] = item.text() if item else ""
            new_data.append(row_dict)

        # Update the reference
        self.data.clear()
        self.data.extend(new_data)

        self.accept()  # This tells the main window "The user is done and wants to save"

# --- Execution ---
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = FileManagerApp()
    ex.show()
    sys.exit(app.exec_())