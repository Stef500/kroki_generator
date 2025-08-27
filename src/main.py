"""Main Flask application factory."""

import os
from flask import Flask
from src.config import config


def create_app(config_name=None):
    """Create and configure Flask application."""
    if config_name is None:
        config_name = os.getenv("FLASK_CONFIG", "default")

    app = Flask(__name__, template_folder="../templates", static_folder="../static")

    app.config.from_object(config[config_name])

    # Register blueprints
    from src.routes import main_bp

    app.register_blueprint(main_bp)

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=5000, debug=True)
