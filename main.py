import json
import os
import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QMessageBox
from PySide6.QtCore import Qt
from ui.main_window import Ui_MainWindow
from ui.flashcard_window import Ui_FlashcardWindow
from ui.quizzes_window import Ui_QuizzesWindow

FLASHCARD_FILE = "flashcards.json"

# Main Window
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowTitle("Quizify")

        self.flashcard_window = None
        self.quizzes_window = None

        # When user clicks one of the PushButtons, open the window for it
        self.ui.flashcardSet.clicked.connect(self.open_flashcards)
        self.ui.quizzesBtn.clicked.connect(self.open_quizzes)

    def open_flashcards(self):
        if self.flashcard_window is None:
            self.flashcard_window = FlashcardWindow()
        self.flashcard_window.show()

    def open_quizzes(self):
        if self.quizzes_window is None:
            self.quizzes_window = QuizzesWindow()
        self.quizzes_window.show()


# Flashcards Window
class FlashcardWindow(QMainWindow, Ui_FlashcardWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("Quizify - Flashcard")

        # Buttons
        self.pushButton.clicked.connect(self.create_flashcard_set)   # "Create Flashcard Set"
        self.pushButton_2.clicked.connect(self.reset_inputs)         # "Reset"

        # Error label (label_3)
        self.label_3.setText("")
        self.label_3.setStyleSheet("color: rgb(170, 0, 0);")

        # JSON file initialization
        if not os.path.exists(FLASHCARD_FILE):
            with open(FLASHCARD_FILE, "w") as f:
                json.dump([], f)

    def create_flashcard_set(self):
        title = self.lineEdit.text().strip()
        description = self.lineEdit_2.text().strip()

        # Validate title & description
        if not title or not description:
            self.set_error("Title and Description are required!")
            return

        # Get flashcards (4 possible)
        flashcards = []
        cards = [
            (self.lineEdit_3, self.lineEdit_4),
            (self.lineEdit_5, self.lineEdit_6),
            (self.lineEdit_7, self.lineEdit_8),
            (self.lineEdit_9, self.lineEdit_10)
        ]

        for item_edit, desc_edit in cards:
            item = item_edit.text().strip()
            desc = desc_edit.text().strip()
            if item and desc:
                flashcards.append({"item": item, "description": desc})

        # Must have at least 2 flashcards
        if len(flashcards) < 2:
            self.set_error("You must create at least 2 flashcards!")
            return

        # Save the flashcard set
        self.save_flashcard_set(title, description, flashcards)

        # Success message
        QMessageBox.information(self, "Success", "Flashcard set created successfully!")

        # Reset after success
        self.reset_inputs()

    def set_error(self, message):
        """Show error messages on label_3"""
        self.label_3.setText(message)
        self.label_3.setStyleSheet("color: rgb(170, 0, 0); font-weight: bold;")

    def reset_inputs(self):
        """Clear all LineEdit contents"""
        fields = [
            self.lineEdit, self.lineEdit_2,
            self.lineEdit_3, self.lineEdit_4,
            self.lineEdit_5, self.lineEdit_6,
            self.lineEdit_7, self.lineEdit_8,
            self.lineEdit_9, self.lineEdit_10
        ]
        for field in fields:
            field.clear()
        self.set_error("(You must create 2 Flashcards to make a set.)")

    def save_flashcard_set(self, title, description, flashcards):
        """Save flashcard set to flashcards.json"""
        with open(FLASHCARD_FILE, "r") as f:
            data = json.load(f)

        data.append({
            "title": title,
            "description": description,
            "flashcards": flashcards
        })

        with open(FLASHCARD_FILE, "w") as f:
            json.dump(data, f, indent=4)
        

# Quizzes Window
class QuizzesWindow(QMainWindow, Ui_QuizzesWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("Quizify - Quiz")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
