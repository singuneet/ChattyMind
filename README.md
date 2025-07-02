# ChattyMind

ChattyMind is a simple Flask-based chatbot application that leverages spaCy for Natural Language Processing (NLP).

## 🚀 Features

- Web-based chat interface
- Processes user input using spaCy
- Simple and lightweight design

## 🗂️ Project Structure

ChattyMind-main/
├── app.py
├── templates/
│ └── index.html

## ⚙️ Installation

Follow these steps to set up and run the project locally using a virtual environment.

### 1. Clone or Download the Repository

Extract the `ChattyMind-main.zip` file or clone if using git:

```bash
git clone <repo-url>
cd ChattyMind-main
2. Create a Virtual Environment
python3 -m venv venv
source venv/bin/activate  # Mac/Linux

# On Windows:
# .\venv\Scripts\Activate
3. Install Dependencies
pip install flask spacy requests
4. Download spaCy Language Model
python -m spacy download en_core_web_sm
5. Run the Application
python app.py
Open your browser and navigate to http://127.0.0.1:5000 to see the app running.
📁 Requirements
Python 3.x
Flask
spaCy
requests
(Alternatively, install from requirements.txt if generated.)
❗ Troubleshooting
TemplateNotFound Error: Ensure your HTML files are inside the templates/ folder.
Missing spaCy model: Run python -m spacy download en_core_web_sm.
✨ License
This project is for educational purposes. Modify and extend it as per your needs.
