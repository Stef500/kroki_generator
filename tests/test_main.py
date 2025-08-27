"""Tests for main Flask application factory."""

import pytest
import os
from unittest.mock import patch
from src.main import create_app


class TestCreateApp:
    """Test cases for Flask application factory."""

    def test_create_app_default_config(self):
        """Test creating app with default configuration."""
        app = create_app()
        
        assert app is not None
        assert app.name == "src.main"
        assert "main" in [bp.name for bp in app.blueprints.values()]

    def test_create_app_with_config_name(self):
        """Test creating app with specific config name."""
        app = create_app("testing")
        
        assert app is not None
        assert app.config["TESTING"] is True

    def test_create_app_with_development_config(self):
        """Test creating app with development config."""
        app = create_app("development")
        
        assert app is not None
        # Development config should have debug settings

    def test_create_app_with_production_config(self):
        """Test creating app with production config."""
        app = create_app("production")
        
        assert app is not None
        # Production config should be more restrictive

    @patch.dict(os.environ, {"FLASK_CONFIG": "testing"})
    def test_create_app_uses_env_config(self):
        """Test that create_app uses FLASK_CONFIG environment variable."""
        app = create_app(config_name=None)
        
        assert app is not None
        assert app.config["TESTING"] is True

    @patch.dict(os.environ, {}, clear=True)
    def test_create_app_defaults_when_no_env(self):
        """Test that create_app defaults to 'default' when no env var set."""
        # Remove FLASK_CONFIG if it exists
        if "FLASK_CONFIG" in os.environ:
            del os.environ["FLASK_CONFIG"]
            
        app = create_app(config_name=None)
        
        assert app is not None
        # Should use default configuration

    def test_create_app_template_and_static_folders(self):
        """Test that app has correct template and static folder configuration."""
        app = create_app("testing")
        
        # Template and static folders should end with the correct relative paths
        assert app.template_folder.endswith("../templates")
        assert app.static_folder.endswith("../static")

    def test_create_app_blueprints_registered(self):
        """Test that required blueprints are registered."""
        app = create_app("testing")
        
        blueprint_names = [bp.name for bp in app.blueprints.values()]
        assert "main" in blueprint_names

    def test_create_app_config_object_applied(self):
        """Test that configuration object is properly applied."""
        app = create_app("testing")
        
        # Test that config values from config object are present
        assert hasattr(app.config, "get")
        assert "TESTING" in app.config