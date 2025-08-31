from flask import Blueprint, request, jsonify
from models import db, Habit, HabitProgress
from datetime import datetime, timedelta

habits_bp = Blueprint('habits_bp', __name__)

@habits_bp.route("/habits", methods=["GET", "POST"])
def habits_collection():
    if request.method == "GET":
        habits = Habit.query.all()
        return jsonify([
            {
                "id": h.id,
                "habit_name": h.habit_name,
                "frequency": h.frequency,
                "goal": h.goal,
                "notes": h.notes
            } for h in habits
        ])

    data = request.json
    try:
        habit = Habit(
            habit_name=data.get("habit_name", ""),
            frequency=data.get("frequency"),
            goal=int(data.get("goal", 1)),
            notes=data.get("notes")
        )
        db.session.add(habit)
        db.session.commit()
        return jsonify({"message": "Habit created", "id": habit.id}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@habits_bp.route("/habits/<int:id>", methods=["PUT", "DELETE"])
def habit_resource(id):
    habit = Habit.query.get_or_404(id)
    if request.method == "PUT":
        data = request.json
        try:
            habit.habit_name = data.get("habit_name", habit.habit_name)
            habit.frequency = data.get("frequency", habit.frequency)
            habit.goal = int(data.get("goal", habit.goal))
            habit.notes = data.get("notes", habit.notes)
            db.session.commit()
            return jsonify({"message": "Habit updated"})
        except Exception as e:
            return jsonify({"error": str(e)}), 400
    else:
        try:
            db.session.delete(habit)
            db.session.commit()
            return jsonify({"message": "Habit deleted"})
        except Exception as e:
            return jsonify({"error": str(e)}), 400


@habits_bp.route("/habits/<int:id>/progress", methods=["GET", "POST"])
def habit_progress(id):
    habit = Habit.query.get_or_404(id)
    freq = habit.frequency if habit.frequency else "daily"
    today = datetime.utcnow().date()
    if freq == "daily":
        start_date = today - timedelta(days=29)
        dates = [start_date + timedelta(days=i) for i in range(30)]
    elif freq == "weekly":
        start_date = today - timedelta(weeks=11)
        dates = [start_date + timedelta(weeks=i) for i in range(12)]
    elif freq == "monthly":
        start_date = today.replace(day=1)
        dates = []
        for i in range(6):
            month = (start_date.month - 1 + i) % 12 + 1
            year = start_date.year + ((start_date.month - 1 + i) // 12)
            dates.append(datetime(year, month, 1).date())
    else:
        start_date = today - timedelta(days=29)
        dates = [start_date + timedelta(days=i) for i in range(30)]

    if request.method == "GET":
        progress_data = {d.isoformat(): 0 for d in dates}
        completions = HabitProgress.query.filter(HabitProgress.habit_id == id).all()
        for c in completions:
            key = c.date.isoformat()
            if key in progress_data:
                progress_data[key] = c.count
        return jsonify({
            "progress": progress_data,
            "goal": habit.goal,
            "frequency": habit.frequency
        })

    data = request.json
    try:
        date_str = data.get("date")
        count = int(data.get("count", 1))
        date_obj = datetime.strptime(date_str, "%Y-%m-%d").date()

        progress_entry = HabitProgress.query.filter_by(habit_id=id, date=date_obj).first()
        if progress_entry:
            progress_entry.count = count
        else:
            progress_entry = HabitProgress(habit_id=id, date=date_obj, count=count)
            db.session.add(progress_entry)
        db.session.commit()
        return jsonify({"message": "Progress updated"})
    except Exception as e:
        return jsonify({"error": str(e)}), 400
