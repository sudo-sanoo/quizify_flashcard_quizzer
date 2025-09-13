import json
import os
import sys
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QMessageBox, QPushButton,
    QWidget, QTableWidgetItem, QButtonGroup
)
from PySide6.QtCore import Qt
from ui.main_window import Ui_MainWindow
from ui.flashcard_window import Ui_FlashcardWindow
from ui.flashcard_set_view import Ui_MainWindow as Ui_FlashcardSetView
from ui.quizzes_window import Ui_QuizzesWindow
from ui.quizzes_set_view import Ui_MainWindow as Ui_QuizzesSetView
from ui.open_quizzes_set_view import Ui_MainWindow as Ui_OpenQuizzesSetView

FLASHCARD_FILE = "flashcards.json"
QUIZZES_FILE = "quizzes.json"

# ======================
# MAIN WINDOW
# ======================
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setFixedSize(self.size())
        self.setWindowTitle("Quizify")

        self.flashcard_window = None
        self.quizzes_window = None

        if not os.path.exists(FLASHCARD_FILE):
            with open(FLASHCARD_FILE, "w") as f:
                json.dump([], f)

        # Top Navigation Buttons
        self.ui.homePage.clicked.connect(lambda: self.ui.stackedWidget.setCurrentIndex(0))
        self.ui.setPage.clicked.connect(self.show_flashcard_sets)
        self.ui.quizzesPage.clicked.connect(self.show_quizzes)

        self.ui.homePage_2.clicked.connect(lambda: self.ui.stackedWidget.setCurrentIndex(0))
        self.ui.setPage_2.clicked.connect(self.show_flashcard_sets)
        self.ui.quizzesPage_2.clicked.connect(self.show_quizzes)

        self.ui.homePage_3.clicked.connect(lambda: self.ui.stackedWidget.setCurrentIndex(0))
        self.ui.setPage_3.clicked.connect(self.show_flashcard_sets)
        self.ui.quizzesPage_3.clicked.connect(self.show_quizzes)

        # Homepage Buttons -> Open New Windows
        self.ui.flashcardSet.clicked.connect(self.open_flashcards)
        self.ui.quizzesBtn.clicked.connect(self.open_quizzes)

        # Style Tables
        table_style = """
            QTableWidget {
                border: 1px solid #000000;
                gridline-color: #000000;
                color: #000;
            }
            QHeaderView::section {
                background-color: #c0c0c0;
                border: 1px solid #000000;
                color: #000;
            }
        """
        self.ui.tableWidget.setStyleSheet(table_style)
        self.ui.tableWidget_2.setStyleSheet(table_style)

    # Opens Flashcard Creation Window
    def open_flashcards(self):
        if self.flashcard_window is None:
            self.flashcard_window = FlashcardWindow(self)
        self.flashcard_window.show()

    # Show Flashcard Sets Page
    def show_flashcard_sets(self):
        self.ui.stackedWidget.setCurrentIndex(1)
        self.load_flashcard_sets()

    # Load Flashcards into QTableWidget
    def load_flashcard_sets(self):
        if not os.path.exists(FLASHCARD_FILE):
            return

        with open(FLASHCARD_FILE, "r") as f:
            flashcards = json.load(f)

        table = self.ui.tableWidget
        table.setRowCount(len(flashcards))

        for row, flashcard_set in enumerate(flashcards):
            title_item = QTableWidgetItem(flashcard_set["title"])
            title_item.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)
            table.setItem(row, 0, title_item)

            desc_item = QTableWidgetItem(flashcard_set["description"])
            desc_item.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)
            table.setItem(row, 1, desc_item)

            view_btn = QPushButton("View")
            view_btn.setStyleSheet("background-color: rgb(0,0,255); color: #000;")
            view_btn.clicked.connect(lambda _, r=row: self.view_flashcard_set(r))
            table.setCellWidget(row, 2, view_btn)

            del_btn = QPushButton("Delete")
            del_btn.setStyleSheet("background-color: rgb(255,0,0); color: #000;")
            del_btn.clicked.connect(lambda _, r=row: self.delete_flashcard_set(r))
            table.setCellWidget(row, 3, del_btn)

        table.resizeRowsToContents()
        table.resizeColumnsToContents()

    # View Flashcard Set
    def view_flashcard_set(self, index):
        self.viewer_window = FlashcardSetViewWindow(index)
        self.viewer_window.show()

    # Delete Flashcard Set
    def delete_flashcard_set(self, index):
        if not os.path.exists(FLASHCARD_FILE):
            return

        with open(FLASHCARD_FILE, "r") as f:
            data = json.load(f)

        if index >= len(data):
            return

        title = data[index]["title"]
        confirm = QMessageBox(self)
        confirm.setWindowTitle("Delete Flashcard Set")
        confirm.setText(f"Are you sure you want to delete '{title}'?")
        confirm.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        confirm.setStyleSheet(self.msg_box_style())
        result = confirm.exec()

        if result == QMessageBox.Yes:
            data.pop(index)
            with open(FLASHCARD_FILE, "w") as f:
                json.dump(data, f, indent=4)
            self.load_flashcard_sets()

    # Opens Quizzes Window
    def open_quizzes(self):
        if self.quizzes_window is None:
            self.quizzes_window = QuizzesWindow()
        self.quizzes_window.show()

    # Show Quizzes Page
    def show_quizzes(self):
        self.ui.stackedWidget.setCurrentIndex(2)
        self.load_quizzes()

    # Load Quizzes into QTableWidget
    def load_quizzes(self):
        if not os.path.exists(QUIZZES_FILE):
            return

        with open(QUIZZES_FILE, "r") as f:
            quizzes = json.load(f)

        table = self.ui.tableWidget_2
        table.setRowCount(len(quizzes))

        for row, quiz in enumerate(quizzes):
            # Title
            title_item = QTableWidgetItem(quiz["title"])
            title_item.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)
            table.setItem(row, 0, title_item)

            # View button
            view_btn = QPushButton("View")
            view_btn.setStyleSheet("background-color: rgb(0,0,255); color: #fff;")
            view_btn.clicked.connect(lambda _, r=row: self.view_quiz(r))
            table.setCellWidget(row, 1, view_btn)

            # Delete button
            del_btn = QPushButton("Delete")
            del_btn.setStyleSheet("background-color: rgb(255,0,0); color: #fff;")
            del_btn.clicked.connect(lambda _, r=row: self.delete_quiz(r))
            table.setCellWidget(row, 2, del_btn)

        table.resizeRowsToContents()
        table.resizeColumnsToContents()

    # View Quiz
    def view_quiz(self, index):
        with open(QUIZZES_FILE, "r") as f:
            quizzes = json.load(f)

        quiz = quizzes[index]
        if quiz["quiz_type"] == "Multiple Choice (3 Choices)":
            self.quiz_window = QuizzesSetViewWindow(index)
        elif quiz["quiz_type"] == "Open-Ended":
            self.quiz_window = OpenQuizzesSetViewWindow(index)
        else:
            QMessageBox.warning(self, "Error", "Unsupported quiz type!")
            return

        self.quiz_window.show()


    # Delete Quiz
    def delete_quiz(self, index):
        if not os.path.exists(QUIZZES_FILE):
            return

        with open(QUIZZES_FILE, "r") as f:
            data = json.load(f)

        if index >= len(data):
            return

        title = data[index]["title"]
        confirm = QMessageBox(self)
        confirm.setWindowTitle("Delete Quiz")
        confirm.setText(f"Are you sure you want to delete '{title}'?")
        confirm.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        confirm.setStyleSheet(self.msg_box_style())
        result = confirm.exec()

        if result == QMessageBox.Yes:
            data.pop(index)
            with open(QUIZZES_FILE, "w") as f:
                json.dump(data, f, indent=4)
            self.load_quizzes()

    # Common MessageBox Styling
    def msg_box_style(self):
        return """
            QMessageBox {
                background-color: #000000;
                color: #ffffff;
            }
            QLabel {
                color: #ffffff;
                background-color: #000000;
            }
            QPushButton {
                background-color: #333333;
                color: #ffffff;
                border: none;
                padding: 5px 15px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #555555;
            }
        """


# ======================
# FLASHCARDS WINDOW
# ======================
class FlashcardWindow(QMainWindow, Ui_FlashcardWindow):
    def __init__(self, parent_window=None):
        super().__init__()
        self.setupUi(self)
        self.setFixedSize(self.size())
        self.setWindowTitle("Quizify - Flashcard")
        self.parent_window = parent_window

        self.pushButton.clicked.connect(self.create_flashcard_set)
        self.pushButton_2.clicked.connect(self.reset_inputs)

        self.label_3.setText("")
        self.label_3.setStyleSheet("color: rgb(170, 0, 0);")

        if not os.path.exists(FLASHCARD_FILE):
            with open(FLASHCARD_FILE, "w") as f:
                json.dump([], f)

    # ==============================
    # Create Flashcard Set
    # ==============================
    def create_flashcard_set(self):
        title = self.lineEdit.text().strip()
        description = self.textEdit.toPlainText().strip()

        # Validate
        if not title or not description:
            self.set_error("Title and Description are required!")
            return

        # Get flashcards (4 possible)
        flashcards = []
        cards = [
            (self.textEdit_2, self.textEdit_3),
            (self.textEdit_4, self.textEdit_5),
            (self.textEdit_6, self.textEdit_7),
            (self.textEdit_8, self.textEdit_9)
        ]

        for idx, (item_edit, desc_edit) in enumerate(cards, start=1):
            item = item_edit.toPlainText().strip()
            desc = desc_edit.toPlainText().strip()

            if item and desc:
                flashcards.append({"item": item, "detail": desc})
            elif item or desc:
                self.set_error(f"Flashcard #{idx} is incomplete. Please fill both item and detail or leave both empty.")
                return

        if len(flashcards) < 2:
            self.set_error("You must create at least 2 flashcards!")
            return

        # Save
        self.save_flashcard_set(title, description, flashcards)

        if self.parent_window:
            self.parent_window.load_flashcard_sets()

        QMessageBox.information(self, "Success", "Flashcard set created successfully!")
        self.clear_inputs()
        self.set_success("Successfully created.")

    def set_success(self, message):
        self.label_3.setText(message)
        self.label_3.setStyleSheet("color: rgb(0, 170, 0); font-weight: bold;")

    def clear_inputs(self):
        fields = [
            self.lineEdit, self.textEdit,
            self.textEdit_2, self.textEdit_3,
            self.textEdit_4, self.textEdit_5,
            self.textEdit_6, self.textEdit_7,
            self.textEdit_8, self.textEdit_9
        ]
        for field in fields:
            field.clear()

    def set_error(self, message):
        self.label_3.setText(message)
        self.label_3.setStyleSheet("color: rgb(170, 0, 0); font-weight: bold;")

    def reset_inputs(self):
        fields = [
            self.lineEdit, self.textEdit,
            self.textEdit_2, self.textEdit_3,
            self.textEdit_4, self.textEdit_5,
            self.textEdit_6, self.textEdit_7,
            self.textEdit_8, self.textEdit_9
        ]
        for field in fields:
            field.clear()
        self.set_error("(Successfully resetted.)")

    def save_flashcard_set(self, title, description, flashcards):
        with open(FLASHCARD_FILE, "r") as f:
            data = json.load(f)
        data.append({
            "title": title,
            "description": description,
            "flashcards": flashcards
        })
        with open(FLASHCARD_FILE, "w") as f:
            json.dump(data, f, indent=4)

# =============================
#  VIEW FLASHCARD SET WINDOW
# =============================

class FlashcardSetViewWindow(QMainWindow, Ui_FlashcardSetView):
    def __init__(self, set_index):
        super().__init__()
        self.setupUi(self)
        self.setFixedSize(self.size())
        self.set_index = set_index

        # Load flashcards
        with open(FLASHCARD_FILE, "r") as f:
            data = json.load(f)

        if set_index >= len(data):
            self.close()
            return

        self.flashcard_set = data[set_index]
        self.flashcards = self.flashcard_set["flashcards"]
        self.setWindowTitle(f"{self.flashcard_set['title']}")

        self.current_page = 0
        self.total_pages = len(self.flashcards) * 2 

        self.update_page()

        self.continueBtn.clicked.connect(self.next_page)
        self.continueBtn_2.clicked.connect(self.next_page)
        self.returnBtn.clicked.connect(self.prev_page)
        self.returnBtn_2.clicked.connect(self.prev_page)

    def update_page(self):
        """Update UI for current page."""
        flashcard_index = self.current_page // 2
        is_item_page = self.current_page % 2 == 0

        if flashcard_index >= len(self.flashcards):
            return

        if is_item_page:
            self.item_text.setText(self.flashcards[flashcard_index]["item"])
            self.stackedWidget.setCurrentWidget(self.title_page)
        else:
            self.detail_text.setText(self.flashcards[flashcard_index]["detail"])
            self.stackedWidget.setCurrentWidget(self.detail_page)

    def next_page(self):
        """Go to next page if available."""
        if self.current_page < self.total_pages - 1:
            self.current_page += 1
            self.update_page()

    def prev_page(self):
        """Go to previous page if available."""
        if self.current_page > 0:
            self.current_page -= 1
            self.update_page()



# ======================
# QUIZZES WINDOW
# ======================
class QuizzesWindow(QMainWindow, Ui_QuizzesWindow):
    def __init__(self, parent=None):
        super().__init__()
        self.setupUi(self)
        self.setFixedSize(self.size())
        self.setWindowTitle("Quizify - Create Quiz")
        self.parent_window = parent

        if not os.path.exists(QUIZZES_FILE):
            with open(QUIZZES_FILE, "w") as f:
                json.dump([], f)

        self.load_flashcard_titles()

        self.error_message.setText("")

        self.pushButton.clicked.connect(self.create_quiz)

    # Load Flashcard Titles into Dropdown
    def load_flashcard_titles(self):
        self.flashcard_titles.clear()
        if not os.path.exists(FLASHCARD_FILE):
            return

        with open(FLASHCARD_FILE, "r") as f:
            flashcards = json.load(f)

        if not flashcards:
            self.flashcard_titles.addItem("No flashcard sets available")
            self.flashcard_titles.setEnabled(False)
            return

        self.flashcard_titles.setEnabled(True)
        for flashcard_set in flashcards:
            self.flashcard_titles.addItem(flashcard_set["title"])


    # Create Quiz
    def create_quiz(self):
        title = self.lineEdit.text().strip()
        flashcard_title = self.flashcard_titles.currentText()
        quiz_type = self.comboBox.currentText()
        num_questions = self.spinBox.value()

        # Validate title
        if not title:
            return self.show_error("Quiz title is required!")

        # Validate flashcard set
        if not os.path.exists(FLASHCARD_FILE):
            return self.show_error("No flashcard sets available!")

        with open(FLASHCARD_FILE, "r") as f:
            flashcards_data = json.load(f)

        if not flashcards_data:
            return self.show_error("Please create at least one flashcard set first!")

        # Find the selected flashcard set
        selected_set = next(
            (fs for fs in flashcards_data if fs["title"] == flashcard_title), None
        )

        if not selected_set:
            return self.show_error("Invalid flashcard set selected!")

        # Validate question count
        if num_questions > len(selected_set["flashcards"]):
            return self.show_error(
                f"Questions cannot exceed the number of flashcards. ({len(selected_set['flashcards'])} flashcards)"
            )

        quiz = {
            "title": title,
            "flashcard_title": flashcard_title,
            "quiz_type": quiz_type,
            "num_questions": num_questions,
        }

        # Save to quizzes.json
        with open(QUIZZES_FILE, "r") as f:
            quizzes = json.load(f)

        quizzes.append(quiz)

        with open(QUIZZES_FILE, "w") as f:
            json.dump(quizzes, f, indent=4)

        msg = QMessageBox(self)
        msg.setWindowTitle("Success")
        msg.setText("Quiz created successfully!")
        msg.setStyleSheet(self.msg_box_style())
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec()

        self.reset_inputs()

        if self.parent_window:
            self.parent_window.load_quizzes()

    # Show Error Message
    def show_error(self, message):
        self.error_message.setText(message)
        self.error_message.setStyleSheet("color: rgb(170, 0, 0); border: none; font-weight: bold;")

    # Reset Inputs
    def reset_inputs(self):
        self.lineEdit.clear()
        self.flashcard_titles.setCurrentIndex(0)
        self.comboBox.setCurrentIndex(0)
        self.spinBox.setValue(1)
        self.error_message.setText("")

    # Common MessageBox Styling
    def msg_box_style(self):
        return """
            QMessageBox {
                background-color: #000000;
                color: #ffffff;
            }
            QLabel {
                color: #ffffff;
                background-color: #000000;
            }
            QPushButton {
                background-color: #333333;
                color: #ffffff;
                border: none;
                padding: 5px 15px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #555555;
            }
        """


# ==============================
# QUIZZES SET VIEW WINDOW
# ==============================
class QuizzesSetViewWindow(QMainWindow):
    def __init__(self, quiz_index, parent=None):
        super().__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui = Ui_QuizzesSetView()
        self.ui.setupUi(self)
        self.setFixedSize(self.size())
        
        # Example: list of questions (replace with your actual quiz data)
        self.questions = [
            {"question": "Question 1?", "options": ["A", "B", "C"], "correct": 0},
            {"question": "Question 2?", "options": ["X", "Y", "Z"], "correct": 1},
            {"question": "Question 3?", "options": ["M", "N", "O"], "correct": 2},
        ]
        
        self.answers = [None] * len(self.questions)
        self.current_index = 0
        
        self.option_group = QButtonGroup(self)
        self.option_group.setExclusive(True)
        self.option_group.addButton(self.ui.checkBox, 0)
        self.option_group.addButton(self.ui.checkBox_2, 1)
        self.option_group.addButton(self.ui.checkBox_3, 2)

        self.ui.nextBtn.clicked.connect(self.next_question)
        self.ui.prevBtn.clicked.connect(self.prev_question)
        self.ui.prevBtn_2.clicked.connect(self.prev_question)
        
        self.update_page()

    def update_page(self):
        total_pages = len(self.questions)
        if self.current_index < total_pages:
            # Update question page
            q = self.questions[self.current_index]
            self.ui.question.setText(q["question"])
            self.ui.checkBox.setText(q["options"][0])
            self.ui.checkBox_2.setText(q["options"][1])
            self.ui.checkBox_3.setText(q["options"][2])
            
            self.option_group.setExclusive(False)
            self.ui.checkBox.setChecked(False)
            self.ui.checkBox_2.setChecked(False)
            self.ui.checkBox_3.setChecked(False)
            self.option_group.setExclusive(True)
            
            self.ui.stackedWidget.setCurrentIndex(0)
            
            # Update progress bar
            progress = int((self.current_index / total_pages) * 100)
            self.ui.progressBar.setValue(progress)

            self.ui.questions_track.setText(f"Question {self.current_index + 1} of {total_pages}")
            
        else:
            # Show results page
            score = sum(1 for i, a in enumerate(self.answers) if a == self.questions[i]["correct"])
            self.ui.result_text.setText(f"You scored {score} out of {len(self.questions)}")
            self.ui.stackedWidget.setCurrentIndex(1)
            self.ui.progressBar.setValue(100)

    def next_question(self):
        if self.current_index < len(self.questions):
            if self.ui.checkBox.isChecked():
                self.answers[self.current_index] = 0
            elif self.ui.checkBox_2.isChecked():
                self.answers[self.current_index] = 1
            elif self.ui.checkBox_3.isChecked():
                self.answers[self.current_index] = 2
            else:
                self.answers[self.current_index] = None

        self.current_index += 1
        self.update_page()

    def prev_question(self):
        if self.current_index > 0:
            self.current_index -= 1
        self.update_page()


# ==============================
# OPEN-ENDED QUIZZES SET VIEW WINDOW
# ==============================
class OpenQuizzesSetViewWindow(QMainWindow):
    def __init__(self, quiz_index, parent=None):
        super().__init__(parent)
        self.ui = Ui_OpenQuizzesSetView()
        self.ui.setupUi(self)
        self.setFixedSize(self.size())

        # Load quizzes.json
        with open(QUIZZES_FILE, "r") as f:
            quizzes = json.load(f)

        if quiz_index >= len(quizzes):
            self.close()
            return

        self.quiz = quizzes[quiz_index]

        with open(FLASHCARD_FILE, "r") as f:
            flashcards = json.load(f)

        selected_set = next((fs for fs in flashcards if fs["title"] == self.quiz["flashcard_title"]), None)
        if not selected_set:
            self.close()
            return

        # Prepare questions (use "item" as question, "detail" as correct answer)
        flashcards_list = selected_set["flashcards"][: self.quiz["num_questions"]]
        self.questions = [
            {"question": f["item"], "answer": f["detail"]}
            for f in flashcards_list
        ]

        self.answers = [None] * len(self.questions)
        self.current_index = 0

        self.ui.nextBtn.clicked.connect(self.next_question)
        self.ui.prevBtn.clicked.connect(self.prev_question)
        self.ui.prevBtn_2.clicked.connect(self.prev_question)

        self.update_page()

    def update_page(self):
        total_pages = len(self.questions)
        if self.current_index < total_pages:

            q = self.questions[self.current_index]
            self.ui.question.setText(q["question"])

            if self.answers[self.current_index] is not None:
                self.ui.answer.setText(self.answers[self.current_index])
            else:
                self.ui.answer.clear()

            self.ui.stackedWidget.setCurrentIndex(0)

            progress = int((self.current_index / total_pages) * 100)
            self.ui.progressBar.setValue(progress)

            self.ui.questions_track.setText(f"Question {self.current_index + 1} of {total_pages}")

        else:
            score = sum(
                1
                for i, a in enumerate(self.answers)
                if a is not None and a.strip().lower() == self.questions[i]["answer"].strip().lower()
            )
            self.ui.result_text.setText(f"You scored {score} out of {len(self.questions)}")

            self.ui.stackedWidget.setCurrentIndex(1)
            self.ui.progressBar.setValue(100)
            self.ui.questions_track.setText("Results")

    def next_question(self):
        if self.current_index < len(self.questions):
            self.answers[self.current_index] = self.ui.answer.toPlainText().strip()

        self.current_index += 1
        self.update_page()

    def prev_question(self):
        if self.ui.stackedWidget.currentIndex() == 1 and len(self.questions) > 0:
            self.current_index = len(self.questions) - 1
            self.update_page()
            return

        if self.current_index > 0:
            self.current_index -= 1
        self.update_page()


# ======================
# MAIN ENTRY POINT
# ======================
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())