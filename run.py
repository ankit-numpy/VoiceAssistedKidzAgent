"""
Entry point for the Voice Assisted KidzAgent Flask application.
"""
import os
from app import create_app, db
from app.models import User, ReadingSession, SessionFeedback

app = create_app(os.getenv("FLASK_ENV", "development"))

@app.shell_context_processor
def make_shell_context():
    return {
        "db": db,
        "User": User,
        "ReadingSession": ReadingSession,
        "SessionFeedback": SessionFeedback,
    }

@app.cli.command()
def init_db():
    """Initialize the database."""
    db.create_all()
    print("Database initialized!")

@app.cli.command()
def seed_db():
    """Seed the database with sample reading passages."""
    from app.models import ReadingPassage
    
    passages = [
        ReadingPassage(
            title="The Little Red Cat",
            content="The little red cat sat on the mat. She was very happy. She liked to play with her toy.",
            difficulty_level="easy",
            age_group="5-6"
        ),
        ReadingPassage(
            title="A Day at the Zoo",
            content="Today we went to the zoo. We saw many animals. The zebras were running fast. The lions were sleeping under the trees.",
            difficulty_level="easy",
            age_group="6-7"
        ),
    ]
    
    for passage in passages:
        if not ReadingPassage.query.filter_by(title=passage.title).first():
            db.session.add(passage)
    
    db.session.commit()
    print(f"Seeded {len(passages)} passages!")

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
