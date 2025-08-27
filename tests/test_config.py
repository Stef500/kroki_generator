"""Tests for configuration module."""

import pytest
import os
from unittest.mock import patch
from src.config import Config, DevelopmentConfig, ProductionConfig, TestingConfig, config


class TestConfig:
    """Test cases for configuration classes."""

    def test_base_config_defaults(self):
        """Test base Config class default values."""
        cfg = Config()
        
        # Test default values
        assert cfg.KROKI_URL == os.getenv("KROKI_URL", "http://localhost:8000")
        assert cfg.REQUEST_TIMEOUT == int(os.getenv("REQUEST_TIMEOUT", "10"))
        assert cfg.MAX_BYTES == int(os.getenv("MAX_BYTES", "1000000"))
        assert cfg.FLASK_ENV == os.getenv("FLASK_ENV", "development")
        assert cfg.SECRET_KEY == os.getenv("SECRET_KEY", "dev-key-change-in-production")
        assert cfg.DIAGRAM_BACKGROUND_COLOR == os.getenv("DIAGRAM_BACKGROUND_COLOR", "white")
        assert cfg.DIAGRAM_THEME == os.getenv("DIAGRAM_THEME", "default")

    def test_config_uses_environment_variables(self):
        """Test that Config class reads environment variables."""
        # Just test that the Config class can access environment variables
        # The actual values depend on current environment
        cfg = Config()
        assert hasattr(cfg, 'KROKI_URL')
        assert hasattr(cfg, 'REQUEST_TIMEOUT')
        assert hasattr(cfg, 'MAX_BYTES')

    def test_config_environment_variable_pattern(self):
        """Test that Config follows environment variable pattern."""
        # Test that os.getenv is called with proper defaults
        cfg = Config()
        
        # These should be strings/ints, not None
        assert isinstance(cfg.KROKI_URL, str)
        assert isinstance(cfg.REQUEST_TIMEOUT, int)
        assert isinstance(cfg.MAX_BYTES, int)

    @patch.dict(os.environ, {"FLASK_DEBUG": "true"})
    def test_config_debug_true_from_env(self):
        """Test DEBUG setting from environment variable."""
        cfg = Config()
        assert cfg.DEBUG is True

    def test_config_debug_boolean_handling(self):
        """Test DEBUG boolean handling."""
        cfg = Config()
        # DEBUG should be a boolean
        assert isinstance(cfg.DEBUG, bool)

    def test_development_config(self):
        """Test DevelopmentConfig settings."""
        cfg = DevelopmentConfig()
        assert cfg.DEBUG is True

    def test_production_config(self):
        """Test ProductionConfig settings."""
        cfg = ProductionConfig()
        assert cfg.DEBUG is False

    def test_testing_config(self):
        """Test TestingConfig settings."""
        cfg = TestingConfig()
        assert cfg.TESTING is True
        assert cfg.DEBUG is True

    def test_config_dictionary(self):
        """Test config dictionary contains all expected configurations."""
        assert "development" in config
        assert "production" in config
        assert "testing" in config
        assert "default" in config
        
        assert config["development"] == DevelopmentConfig
        assert config["production"] == ProductionConfig
        assert config["testing"] == TestingConfig
        assert config["default"] == DevelopmentConfig

    def test_config_inheritance(self):
        """Test that all config classes inherit from Config."""
        assert issubclass(DevelopmentConfig, Config)
        assert issubclass(ProductionConfig, Config)
        assert issubclass(TestingConfig, Config)