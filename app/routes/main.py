"""
Main routes for home, about, and navigation.
"""
from flask import render_template, session, redirect, url_for
from app.routes import main_bp
from app.models import Child, ReadingPassage
from app import db

@main_bp.route("/")
def index():
    """Home page."""
    return render_template("index.html")

@main_bp.route("/about")
def about():
    """About page."""
    return render_template("about.html")

@main_bp.route("/dashboard")
def dashboard():
    """Parental dashboard (requires authentication)."""
    # TODO: Add authentication middleware
    user_id = session.get("user_id")
    if not user_id:
        return redirect(url_for("main.index"))
    
    children = Child.query.filter_by(parent_id=user_id).all()
    return render_template("dashboard.html", children=children)

@main_bp.route("/select-child")
def select_child():
    """Select a child for reading practice."""
    children = Child.query.all()
    return render_template("select_child.html", children=children)

@main_bp.route("/select-passage/<int:child_id>")
def select_passage(child_id):
    """Select a reading passage."""
    child = Child.query.get_or_404(child_id)
    passages = ReadingPassage.query.filter_by(age_group=f"{child.age}").all()
    return render_template("select_passage.html", child=child, passages=passages)

@main_bp.route("/ask-anything")
def ask_anything():
    """Ask Anything - voice-based Q&A feature."""
    return render_template("ask_anything.html")
