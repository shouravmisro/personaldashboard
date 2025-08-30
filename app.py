import os
from flask import Flask, render_template
from dotenv import load_dotenv

load_dotenv()

from models import db

app = Flask(__name__)

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///dashboard.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# Import API blueprints
from events import events_bp
from tasks import tasks_bp
from habits import habits_bp
from weather import weather_bp

# Register API blueprints under '/api' prefix
app.register_blueprint(events_bp, url_prefix='/api')
app.register_blueprint(tasks_bp, url_prefix='/api')
app.register_blueprint(habits_bp, url_prefix='/api')
app.register_blueprint(weather_bp, url_prefix='/api')
import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

# Serve frontend pages
@app.route("/")
def home():
    return render_template("home.html")

@app.route("/events")
def events():
    return render_template("events.html")

@app.route("/tasks")
def tasks():
    return render_template("tasks.html")

@app.route("/habits")
def habits():
    return render_template("habits.html")

@app.route("/weather")
def weather():
    return render_template("weather.html")

if __name__ == "__main__":
    with app.app_context():
        db.create_all()  # Create tables if they don't exist
    app.run(debug=True)
