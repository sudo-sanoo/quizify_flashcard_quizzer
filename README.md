# Quizify - Setup Guide
## Python Interpreter
For the best performance, install **Python 3.11.9**. You can download it from the official Python website:  
[Download Python 3.11.9](https://www.python.org/downloads/release/python-3119/)

## 1. Create a Python virtual environment
```bash
python3.11 -m venv venv
```
OR  
1. Ctrl+Shift+P
2. Select "Python: Create Environment"
3. Select "Venv"
4. Select "Python 3.11.9"
5. Install requirement.txt
6. Click "OK"

## 2. Activate the virtual environment and install dependencies
***For Windows: Powershell/Command Prompt***
```powershell
venv\Scripts\activate.bat  
pip install -r requirements.txt
```
***For macOS/Linux***
```bash
source venv/bin/activate
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
***powershell***
```powershell
copy flashcards.example.json flashcards.json
copy quizzes.example.json quizzes.json
```
***bash***
```bash
cp flashcards.example.json flashcards.json
cp quizzes.example.json quizzes.json
```

## 5. Configure Gemini API for Smart Quiz Generation System (SQGS)
To use the Smart MCQ Generator, you must set up your own Gemini API key.  
1. Get an API key from Google AI Studio: (https://aistudio.google.com/prompts/new_chat)  
2. Create a file named .env in the project root and add:  
```ini
GEMINI_API_KEY="your_api_key_here"
```

## 6. Launch the Application
```
python main.py
```