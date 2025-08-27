"""Configuration module for the Flask application.

This module provides environment-based configuration management for the
Kroki diagram generation application, supporting development, production,
and testing environments with appropriate defaults and security settings.
"""

import os
from typing import Dict, Type
from dotenv import load_dotenv

load_dotenv()


class Config:
    """Base configuration class.

    Contains default configuration values that can be overridden by
    environment variables. Serves as the parent class for environment-specific
    configurations.

    Environment Variables:
        KROKI_URL: Kroki service endpoint URL (default: http://localhost:8000)
        REQUEST_TIMEOUT: HTTP request timeout in seconds (default: 10)
        MAX_BYTES: Maximum diagram source size in bytes (default: 1000000)
        FLASK_ENV: Flask environment name (default: development)
        FLASK_DEBUG: Enable Flask debug mode (default: false)
        SECRET_KEY: Flask secret key for session management (required in production)
        DIAGRAM_BACKGROUND_COLOR: Default diagram background color (default: white)
        DIAGRAM_THEME: Default diagram theme (default: default)
    """

    # Kroki service configuration
    KROKI_URL: str = os.getenv("KROKI_URL", "http://localhost:8000")

    # Request settings
    REQUEST_TIMEOUT: int = int(os.getenv("REQUEST_TIMEOUT", "10"))
    MAX_BYTES: int = int(os.getenv("MAX_BYTES", "1000000"))

    # Flask settings
    FLASK_ENV: str = os.getenv("FLASK_ENV", "development")
    DEBUG: bool = os.getenv("FLASK_DEBUG", "false").lower() == "true"

    # Security
    SECRET_KEY: str = os.getenv("SECRET_KEY", "dev-key-change-in-production")

    # Diagram styling
    DIAGRAM_BACKGROUND_COLOR: str = os.getenv("DIAGRAM_BACKGROUND_COLOR", "white")
    DIAGRAM_THEME: str = os.getenv("DIAGRAM_THEME", "default")


class DevelopmentConfig(Config):
    """Development environment configuration.

    Enables debug mode and provides development-friendly settings.
    Used for local development and testing.
    """

    DEBUG: bool = True


class ProductionConfig(Config):
    """Production environment configuration.

    Disables debug mode and provides production-ready settings
    with enhanced security and performance optimizations.
    """

    DEBUG: bool = False


class TestingConfig(Config):
    """Testing environment configuration.

    Enables testing mode and debug mode for comprehensive
    test suite execution with detailed error reporting.
    """

    TESTING: bool = True
    DEBUG: bool = True


config: Dict[str, Type[Config]] = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
    "testing": TestingConfig,
    "default": DevelopmentConfig,
}
