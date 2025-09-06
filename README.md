# Quizify - Setup Guide
## 1. Create a Python virtual environment
python -m venv venv

## 2. Activate the virtual environment and install dependencies
For Windows: venv\Scripts\activate.bat  
pip install -r requirements.txt

## 3. Generate UI Python from Qt Designer .ui files
### (run these commands inside the activated venv)
pyside6-uic ui/main_window.ui -o ui/main_window.py  
pyside6-uic ui/flashcard_window.ui -o ui/flashcard_window.py  
pyside6-uic ui/quizzes_window.ui -o ui/quizzes_window.py

## 4. Setting Up Flashcards Storage
Before running the app, create your own `flashcards.json` file.

You can do this manually or copy the example file:
```bash
cp flashcards.example.json flashcards.json
```
```powershell
copy flashcards.example.json flashcards.json
```

## 5. Launch the Application
python main.py
