"""
Database models for Voice Assisted KidzAgent.
"""
from datetime import datetime
from app import db

class User(db.Model):
    """User model for parents/guardians."""
    __tablename__ = "users"
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    name = db.Column(db.String(120), nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    children = db.relationship("Child", backref="parent", lazy=True, cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<User {self.email}>"

class Child(db.Model):
    """Child/Student model."""
    __tablename__ = "children"
    
    id = db.Column(db.Integer, primary_key=True)
    parent_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    name = db.Column(db.String(120), nullable=False)
    age = db.Column(db.Integer, nullable=False)  # 5-8
    reading_level = db.Column(db.String(50), default="beginner")  # beginner, intermediate, advanced
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    reading_sessions = db.relationship("ReadingSession", backref="child", lazy=True, cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Child {self.name}>"

class ReadingPassage(db.Model):
    """Reading passages for children."""
    __tablename__ = "reading_passages"
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    difficulty_level = db.Column(db.String(50), nullable=False)  # easy, medium, hard
    age_group = db.Column(db.String(50), nullable=False)  # 5-6, 6-7, 7-8
    estimated_duration = db.Column(db.Integer, default=5)  # minutes
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    reading_sessions = db.relationship("ReadingSession", backref="passage", lazy=True, cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<ReadingPassage {self.title}>"

class ReadingSession(db.Model):
    """A reading practice session."""
    __tablename__ = "reading_sessions"
    
    id = db.Column(db.Integer, primary_key=True)
    child_id = db.Column(db.Integer, db.ForeignKey("children.id"), nullable=False)
    passage_id = db.Column(db.Integer, db.ForeignKey("reading_passages.id"), nullable=False)
    
    # Session metadata
    started_at = db.Column(db.DateTime, default=datetime.utcnow)
    ended_at = db.Column(db.DateTime, nullable=True)
    duration_seconds = db.Column(db.Integer, default=0)
    status = db.Column(db.String(50), default="in_progress")  # in_progress, completed, abandoned
    
    # Performance metrics
    words_read_correctly = db.Column(db.Integer, default=0)
    words_read_incorrectly = db.Column(db.Integer, default=0)
    total_words = db.Column(db.Integer, default=0)
    accuracy_percentage = db.Column(db.Float, default=0.0)
    
    # Relationships
    feedback_items = db.relationship("SessionFeedback", backref="session", lazy=True, cascade="all, delete-orphan")
    
    def calculate_accuracy(self):
        """Calculate reading accuracy percentage."""
        if self.total_words > 0:
            self.accuracy_percentage = (self.words_read_correctly / self.total_words) * 100
        return self.accuracy_percentage
    
    def __repr__(self):
        return f"<ReadingSession {self.id} - Child {self.child_id}>"

class SessionFeedback(db.Model):
    """Word-level feedback during a reading session."""
    __tablename__ = "session_feedback"
    
    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.Integer, db.ForeignKey("reading_sessions.id"), nullable=False)
    
    word_index = db.Column(db.Integer, nullable=False)
    word_expected = db.Column(db.String(120), nullable=False)
    word_spoken = db.Column(db.String(120), nullable=True)
    is_correct = db.Column(db.Boolean, default=False)
    
    # AI-generated feedback
    correction = db.Column(db.Text, nullable=True)  # e.g., "Almost there! It's pronounced 'but-er-fly'"
    explanation = db.Column(db.Text, nullable=True)  # e.g., "A butterfly is a pretty insect with colorful wings!"
    encouragement = db.Column(db.String(255), nullable=True)  # e.g., "Great effort!"
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f"<SessionFeedback {self.id} - Word '{self.word_expected}'>"

class ProgressMetric(db.Model):
    """Aggregate progress metrics for a child."""
    __tablename__ = "progress_metrics"
    
    id = db.Column(db.Integer, primary_key=True)
    child_id = db.Column(db.Integer, db.ForeignKey("children.id"), nullable=False)
    
    sessions_completed = db.Column(db.Integer, default=0)
    total_words_read = db.Column(db.Integer, default=0)
    average_accuracy = db.Column(db.Float, default=0.0)
    vocabulary_learned = db.Column(db.Integer, default=0)
    
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f"<ProgressMetric Child {self.child_id}>"

class Question(db.Model):
    """User questions and AI responses from Ask Anything feature."""
    __tablename__ = "questions"
    
    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.String(50), nullable=True)  # UUID for anonymous sessions
    detected_age = db.Column(db.Integer, nullable=True)  # Detected or provided age (5-12)
    
    question_text = db.Column(db.Text, nullable=False)
    answer_text = db.Column(db.Text, nullable=False)
    
    # Metadata
    confidence_score = db.Column(db.Float, default=0.0)  # Age detection confidence
    is_appropriate = db.Column(db.Boolean, default=True)  # Content safety flag
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f"<Question Age {self.detected_age}: '{self.question_text[:50]}'>"
