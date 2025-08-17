GigHunt 🎯

GigHunt is a career board web app that helps users organize and track job applications, activities, and important contacts — all in one place.

🚀 Features

Job Board – add, edit, and manage job applications.

Metrics Dashboard – track progress and visualize stats.

Activities Tracker – log tasks and follow-ups.

Contacts Manager – save recruiter / company contacts.

Documents Section – keep resumes, cover letters, etc. in one spot.

Drag & Drop – move cards across job stages easily.

🛠️ Tech Stack

Backend: Flask (Python)

Database: SQLite

Frontend: HTML, CSS, JavaScript

Templating: Jinja2

👥 Team Members

Giridhar Reddy – Backend & Setup (Flask, DB, requirements)

Akanksha – UI (HTML templates & structure)

[Teammate 3 Name] – Frontend Styling & Interactivity (CSS + JS)

📂 Project Structure
GigHunt/
│── app.py                # Flask backend
│── requirements.txt       # Dependencies
│── database.db            # SQLite database
│── README.md              # Documentation
│
├── templates/             # HTML templates (board, metrics, activities, contacts, documents)
│── static/
    ├── css/style.css      # Styling
    └── js/board.js        # Frontend interactivity

⚡ Getting Started

Clone the repo:

git clone https://github.com/Akankshapendem/GigHunt.git
cd GigHunt


Create and activate a virtual environment:

python -m venv venv
venv\Scripts\activate   # On Windows
source venv/bin/activate # On Mac/Linux


Install dependencies:

pip install -r requirements.txt


Run the app:

python app.py


Open in browser:

http://127.0.0.1:5000/
