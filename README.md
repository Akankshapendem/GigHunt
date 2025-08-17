GigHunt 🎯

GigHunt is a career board web app that helps users organize and track job applications, activities, and important contacts — all in one place.

🚀 Features

Job Board – add, edit, and manage job applications.

Metrics Dashboard – track progress and visualize stats.

Activities Tracker – log tasks and follow-ups.

Contacts Manager – save recruiter / company contacts.

Documents Section – keep resumes, cover letters, etc. in one spot.

Drag & Drop – move cards across job stages easily.

Screenshots

<img width="2559" height="1528" alt="Screenshot 2025-08-17 233311" src="https://github.com/user-attachments/assets/ce128fb7-ae42-4112-b5f4-a4975c3600ec" />

<img width="2559" height="1530" alt="Screenshot 2025-08-17 233355" src="https://github.com/user-attachments/assets/360d8f83-7dbc-4bd6-93c5-3ed998da5fcb" />

<img width="2559" height="1525" alt="Screenshot 2025-08-17 233405" src="https://github.com/user-attachments/assets/1688d033-e1d1-4252-9735-ef379cd781b2" />

<img width="2541" height="1521" alt="Screenshot 2025-08-17 233414" src="https://github.com/user-attachments/assets/1acbb6e8-c4dd-482f-925f-65e1f48a677f" />

<img width="2559" height="1528" alt="Screenshot 2025-08-17 233422" src="https://github.com/user-attachments/assets/9c3ee4a3-dd2f-4940-bff6-f133efbca6e7" />

🛠️ Tech Stack

Backend: Flask (Python)

Database: SQLite

Frontend: HTML, CSS, JavaScript

Templating: Jinja2

👥 Team Members

Giridhar Reddy – Backend & Setup (Flask, DB, requirements)

Geetika – UI (HTML templates & structure)

Akanksha - Frontend Styling & Interactivity (CSS + JS)

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
