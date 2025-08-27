"""Main Flask application factory.

This module provides the Flask application factory pattern for creating
and configuring the Kroki diagram generation web application.
"""

import os
from flask import Flask
from typing import Optional
from src.config import config


def create_app(config_name: Optional[str] = None) -> Flask:
    """Create and configure Flask application.

    Factory function to create a Flask application instance with proper
    configuration and blueprint registration.

    Args:
        config_name: Configuration name to use. If None, uses FLASK_CONFIG
                    environment variable or defaults to 'default'.
                    Valid values: 'development', 'production', 'testing', 'default'

    Returns:
        Flask: Configured Flask application instance

    Example:
        >>> app = create_app('development')
        >>> app.run(debug=True)
    """
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
    port = int(os.getenv("FLASK_PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
