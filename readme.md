# Personal Dashboard
visit at : https://personal-dashboard.up.railway.app/
A full-featured personal dashboard web application built with Flask to help organize tasks, habits, events, and weather preferences in one place.

---

## Features

- **Task Management:** Create, update, delete tasks with categories, priority, deadlines, and optional external data.
- **Habit Tracking:** Manage daily/weekly/monthly habits with progress tracking and notes.
- **Event Scheduling:** Add and manage personal events with descriptions, dates, and images.
- **Weather Integration:** Store user location preferences and display cached weather data.
- **RESTful API:** Backend APIs for tasks, habits, events, and weather, accessible via `/api`.
- **Responsive UI:** Multiple HTML pages for easy navigation and interaction.

---

## Technology Stack

- **Backend:** Python, Flask, Flask-SQLAlchemy  
- **Database:** SQLite (file-based local DB)  
- **API:** RESTful APIs with Flask Blueprints  
- **Environment management:** `python-dotenv` for environment variables  
- **Dependencies:** See `requirements.txt`  

---

## Project Structure

├── app.py # Main Flask application and route setup
├── models.py # SQLAlchemy data models and database setup
├── events.py # Events API blueprint and routes
├── tasks.py # Tasks API blueprint and routes
├── habits.py # Habits API blueprint and routes
├── weather.py # Weather API blueprint and routes
├── templates/ # HTML templates (home, events, tasks, habits, weather)
├── static/ # Static files (CSS, JS, images)
├── dashboard.db # SQLite database file (auto-generated)
├── requirements.txt # Python dependencies
├── .env # Environment variables (e.g., API keys)
└── Procfile # Deployment command for production server

## Setup and Installation

1. **Clone the repository:**

git clone https://github.com/shouravmisro/personaldashboard.git
cd personaldashboard


2. **Create and activate a virtual environment:**

python -m venv venv
source venv/bin/activate # On Windows use venv\Scripts\activate

3. **Install dependencies:**

pip install -r requirements.txt

4. **Setup environment variables:**

Create a `.env` file with:

OPENWEATHER_API_KEY=your_api_key_here

5. **Run the app locally:**

python app.py

Open [http://localhost:5000](http://localhost:5000) in your browser.

---

## Deployment

- The app is configured for deployment on platforms like **Railway**.
- Uses Gunicorn as WSGI server via `Procfile`: 

web: gunicorn app:app

- Make sure to set environment variables (e.g., `OPENWEATHER_API_KEY`) in the hosting platform settings.
- The SQLite database file (`dashboard.db`) will be created on deployment.

---

## Usage

- Navigate pages from home to tasks, habits, events, and weather.
- Use provided forms to create, update, or delete entries.
- API endpoints are available under `/api` prefix for programmatic access.

---

Feel free to ask if you need full blueprints for `habits.py`, `weather.py`, or other files!
