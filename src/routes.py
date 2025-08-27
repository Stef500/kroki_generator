"""Route definitions for the Flask application."""

from flask import Blueprint, render_template, jsonify

main_bp = Blueprint("main", __name__)


@main_bp.route("/")
def index():
    """Main page with diagram generation form."""
    return render_template("index.html")


@main_bp.route("/health")
def health():
    """Health check endpoint."""
    return jsonify(
        {"status": "healthy", "service": "kroki-flask-generator", "version": "0.1.0"}
    )
