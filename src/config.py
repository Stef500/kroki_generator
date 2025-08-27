"""Configuration module for the Flask application."""

import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    """Base configuration class."""

    # Kroki service configuration
    KROKI_URL = os.getenv("KROKI_URL", "http://localhost:8000")

    # Request settings
    REQUEST_TIMEOUT = int(os.getenv("REQUEST_TIMEOUT", "10"))
    MAX_BYTES = int(os.getenv("MAX_BYTES", "1000000"))

    # Flask settings
    FLASK_ENV = os.getenv("FLASK_ENV", "development")
    DEBUG = os.getenv("FLASK_DEBUG", "false").lower() == "true"

    # Security
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-key-change-in-production")


class DevelopmentConfig(Config):
    """Development configuration."""

    DEBUG = True


class ProductionConfig(Config):
    """Production configuration."""

    DEBUG = False


class TestingConfig(Config):
    """Testing configuration."""

    TESTING = True
    DEBUG = True


config = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
    "testing": TestingConfig,
    "default": DevelopmentConfig,
}
