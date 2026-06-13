"""
Reading session routes.
"""
from flask import render_template, request, jsonify, redirect, url_for
from app.routes import session_bp
from app.models import ReadingSession, ReadingPassage, Child, SessionFeedback
from app import db
import json

@session_bp.route("/start/<int:passage_id>/<int:child_id>")
def start(passage_id, child_id):
    """Start a new reading session."""
    child = Child.query.get_or_404(child_id)
    passage = ReadingPassage.query.get_or_404(passage_id)
    
    # Create new session
    session_record = ReadingSession(child_id=child_id, passage_id=passage_id)
    session_record.total_words = len(passage.content.split())
    db.session.add(session_record)
    db.session.commit()
    
    return render_template(
        "reading_session.html",
        child=child,
        passage=passage,
        session=session_record
    )

@session_bp.route("/end/<int:session_id>", methods=["POST"])
def end(session_id):
    """End a reading session."""
    session_record = ReadingSession.query.get_or_404(session_id)
    
    data = request.get_json()
    session_record.status = "completed"
    session_record.duration_seconds = data.get("duration", 0)
    session_record.calculate_accuracy()
    
    db.session.commit()
    
    return jsonify({
        "status": "success",
        "session_id": session_id,
        "accuracy": session_record.accuracy_percentage
    })

@session_bp.route("/results/<int:session_id>")
def results(session_id):
    """Display session results."""
    session_record = ReadingSession.query.get_or_404(session_id)
    return render_template("session_results.html", session=session_record)
