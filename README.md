# Setup for the app
## 1. Create a Python virtual environment
python -m venv venv

## 2. Activate the virtual environment and install dependencies
For Windows: venv\Scripts\activate.bat
pip install -r requirements.txt

## 3. Generate UI Python from Qt Designer .ui files
### (run this inside the activated venv)
pyside6-uic ui/main_window.ui -o ui/main_window.py
pyside6-uic ui/flashcard_window.ui -o ui/flashcard_window.py
pyside6-uic ui/quizzes_window.ui -o ui/quizzes_window.py

## 4. Launch the Application
python main.py