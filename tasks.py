from flask import Blueprint, request, jsonify
from models import db, ToDoTask
from datetime import datetime
from dateutil import parser  # You need to have python-dateutil installed

tasks_bp = Blueprint('tasks_bp', __name__)

@tasks_bp.route("/tasks", methods=["GET", "POST"])
def tasks_collection():
    if request.method == "GET":
        tasks = ToDoTask.query.order_by(ToDoTask.deadline.asc().nulls_last()).all()
        return jsonify([
            {
                'id': t.id,
                'task_text': t.task_text,
                'category': t.category,
                'priority': t.priority,
                'deadline': t.deadline.isoformat() if t.deadline else None,
                'completed': t.completed,
                'external_data': t.external_data   # Include field here
            } for t in tasks
        ])

    # POST method: create new task
    data = request.json
    try:
        deadline_str = data.get('deadline')
        deadline = parser.isoparse(deadline_str) if deadline_str else None
        task = ToDoTask(
            task_text=data.get('task_text', ''),
            category=data.get('category'),
            priority=int(data.get('priority', 1)),
            deadline=deadline,
            completed=bool(data.get('completed', False)),
            external_data=data.get('external_data')  # Support new field
        )
        db.session.add(task)
        db.session.commit()
        return jsonify({"message": "Task created", "id": task.id}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@tasks_bp.route("/tasks/<int:id>", methods=["PUT", "DELETE"])
def tasks_resource(id):
    task = ToDoTask.query.get_or_404(id)
    if request.method == "PUT":
        data = request.json
        try:
            task.task_text = data.get('task_text', task.task_text)
            task.category = data.get('category', task.category)
            task.priority = int(data.get('priority', task.priority))
            deadline_str = data.get('deadline')
            task.deadline = parser.isoparse(deadline_str) if deadline_str else task.deadline
            task.completed = bool(data.get('completed', task.completed))
            task.external_data = data.get('external_data', task.external_data)  # Update new field
            db.session.commit()
            return jsonify({"message": "Task updated"})
        except Exception as e:
            return jsonify({"error": str(e)}), 400
    elif request.method == "DELETE":
        try:
            db.session.delete(task)
            db.session.commit()
            return jsonify({"message": "Task deleted"})
        except Exception as e:
            return jsonify({"error": str(e)}), 400
