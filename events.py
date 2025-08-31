from flask import Blueprint, request, jsonify
from models import db, Event
from dateutil import parser

events_bp = Blueprint('events_bp', __name__)

@events_bp.route("/events", methods=["GET", "POST"])
def events_collection():
    if request.method == "GET":
        events = Event.query.order_by(Event.event_date.asc()).all()
        return jsonify([
            {
                'id': e.id,
                'title': e.title,
                'description': e.description,
                'event_date': e.event_date.isoformat() if e.event_date else None,
                'image_url': e.image_url
            } for e in events
        ])

    data = request.json
    try:
        event_date_str = data.get('event_date')
        event_date = parser.isoparse(event_date_str) if event_date_str else None
        event = Event(
            title=data.get('title', ''),
            description=data.get('description', ''),
            event_date=event_date,
            image_url=data.get('image_url')
        )
        db.session.add(event)
        db.session.commit()
        return jsonify({"message": "Event created", "id": event.id}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@events_bp.route("/events/<int:id>", methods=["PUT", "DELETE"])
def events_resource(id):
    event = Event.query.get_or_404(id)
    if request.method == "PUT":
        data = request.json
        try:
            event.title = data.get('title', event.title)
            event.description = data.get('description', event.description)
            event_date_str = data.get('event_date')
            event.event_date = parser.isoparse(event_date_str) if event_date_str else event.event_date
            event.image_url = data.get('image_url', event.image_url)
            db.session.commit()
            return jsonify({"message": "Event updated"})
        except Exception as e:
            return jsonify({"error": str(e)}), 400
    elif request.method == "DELETE":
        try:
            db.session.delete(event)
            db.session.commit()
            return jsonify({"message": "Event deleted"})
        except Exception as e:
            return jsonify({"error": str(e)}), 400
