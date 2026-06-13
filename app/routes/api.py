"""
API routes for AJAX/JS communication.
"""
from flask import request, jsonify
from app.routes import api_bp
from app.models import ReadingSession, SessionFeedback, Child, Question
from app import db
from app.utils.llm_helper import get_correction_and_explanation, answer_question
from app.utils.content_filter import is_safe_for_children
from app.utils.age_detector import detect_age_from_voice
import json

@api_bp.route("/transcribe", methods=["POST"])
def transcribe():
    """
    Receive transcribed audio from client or process speech-to-text.
    """
    data = request.get_json()
    session_id = data.get("session_id")
    word_index = data.get("word_index")
    spoken_word = data.get("spoken_word")
    expected_word = data.get("expected_word")
    
    session_record = ReadingSession.query.get_or_404(session_id)
    
    # Simple word matching (can be enhanced with fuzzy matching)
    is_correct = spoken_word.lower().strip() == expected_word.lower().strip()
    
    if is_correct:
        session_record.words_read_correctly += 1
        encouragement = "Great job!"
    else:
        session_record.words_read_incorrectly += 1
        encouragement = "Good try!"
    
    # Get AI-generated feedback
    correction, explanation = get_correction_and_explanation(
        expected_word=expected_word,
        spoken_word=spoken_word,
        is_correct=is_correct
    )
    
    # Save feedback
    feedback = SessionFeedback(
        session_id=session_id,
        word_index=word_index,
        word_expected=expected_word,
        word_spoken=spoken_word,
        is_correct=is_correct,
        correction=correction,
        explanation=explanation,
        encouragement=encouragement
    )
    db.session.add(feedback)
    db.session.commit()
    
    return jsonify({
        "word_index": word_index,
        "is_correct": is_correct,
        "correction": correction,
        "explanation": explanation,
        "encouragement": encouragement
    })

@api_bp.route("/children", methods=["GET"])
def get_children():
    """Get list of all children."""
    children = Child.query.all()
    return jsonify([{
        "id": c.id,
        "name": c.name,
        "age": c.age,
        "reading_level": c.reading_level
    } for c in children])

@api_bp.route("/child/<int:child_id>/progress", methods=["GET"])
def get_child_progress(child_id):
    """Get child's reading progress."""
    child = Child.query.get_or_404(child_id)
    sessions = ReadingSession.query.filter_by(child_id=child_id).all()
    
    total_sessions = len(sessions)
    total_accuracy = sum(s.accuracy_percentage for s in sessions) / total_sessions if sessions else 0
    
    return jsonify({
        "child_id": child_id,
        "child_name": child.name,
        "sessions_completed": total_sessions,
        "average_accuracy": round(total_accuracy, 2),
        "reading_level": child.reading_level
    })

@api_bp.route("/ask-question", methods=["POST"])
def ask_question():
    """
    Receive a question, detect age, and respond with age-appropriate answer.
    """
    data = request.get_json()
    question_text = data.get("question", "").strip()
    detected_age = data.get("age")
    session_id = data.get("session_id")
    
    if not question_text:
        return jsonify({"error": "Question cannot be empty"}), 400
    
    # Safety check
    if not is_safe_for_children(question_text):
        return jsonify({
            "error": "Unable to process that question",
            "message": "That question contains words I can't respond to."
        }), 400
    
    # If age not provided, detect from question text
    if detected_age is None:
        detected_age, confidence = detect_age_from_voice(question_text)
    else:
        confidence = 1.0
        detected_age = max(5, min(12, int(detected_age)))
    
    # Generate age-appropriate answer
    response_text = answer_question(question_text, detected_age)
    
    # Store in database for history
    try:
        q_record = Question(
            session_id=session_id,
            detected_age=detected_age,
            question_text=question_text,
            answer_text=response_text,
            confidence_score=confidence,
            is_appropriate=True
        )
        db.session.add(q_record)
        db.session.commit()
    except Exception as e:
        print(f"Error saving question: {e}")
    
    return jsonify({
        "question": question_text,
        "answer": response_text,
        "detected_age": detected_age,
        "age_confidence": round(confidence, 2),
        "age_description": get_age_description(detected_age)
    })

def get_age_description(age: int) -> str:
    """Get human-readable age description."""
    from app.utils.age_detector import get_age_description as get_desc
    return get_desc(age)
