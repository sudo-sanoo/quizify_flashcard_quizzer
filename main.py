import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget
from PyQt6.QtCore import Qt
from ui.main_window import Ui_MainWindow
from ui.flashcard_window import Ui_FlashcardWindow
from ui.quizzes_window import Ui_QuizzesWindow

# Main Window
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowTitle("Quizify")

        self.flashcard_window = None
        self.quizzes_window = None

        # When user clicks one of the PushButton, open the window for the parts
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
