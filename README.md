# Quizify - Setup Guide
## Python Interpreter
For the best performance, install **Python 3.11.9**. You can download it from the official Python website:  
[Download Python 3.11.9](https://www.python.org/downloads/release/python-3119/)

## 1. Create a Python virtual environment
```terminal
python3.11 -m venv venv
```

## 2. Activate the virtual environment and install dependencies
***For Windows: Powershell/Command Prompt***
```powershell
venv\Scripts\activate.bat  
pip install -r requirements.txt
```
## 3. Generate UI Python from Qt Designer .ui files
### (run these commands inside the activated venv)
```
pyside6-uic ui/main_window.ui -o ui/main_window.py  
pyside6-uic ui/flashcard_window.ui -o ui/flashcard_window.py  
pyside6-uic ui/flashcard_set_view.ui -o ui/flashcard_set_view.py  
pyside6-uic ui/quizzes_window.ui -o ui/quizzes_window.py  
pyside6-uic ui/quizzes_set_view.ui -o ui/quizzes_set_view.py
pyside6-uic ui/open_quizzes_set_view.ui -o ui/open_quizzes_set_view.py
```

## 4. Setting Up Flashcards Storage
Before running the app, create your own `flashcards.json`, `quizzes.json` files.

You can do this manually or copy the example file:  
***bash***
```bash
cp flashcards.example.json flashcards.json
cp quizzes.example.json quizzes.json
```
***powershell***
```powershell
copy flashcards.example.json flashcards.json
copy quizzes.example.json quizzes.json
```

## 5. Launch the Application
```
python main.py
```