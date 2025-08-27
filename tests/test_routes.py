"""Tests for Flask routes."""

import pytest
import json
from unittest.mock import patch, MagicMock
from src.main import create_app
from src.kroki_client import KrokiError


@pytest.fixture
def app():
    """Create test Flask app."""
    app = create_app("testing")
    app.config.update(
        {
            "TESTING": True,
            "KROKI_URL": "http://test-kroki:8000",
            "REQUEST_TIMEOUT": 5,
            "MAX_BYTES": 1000000,
        }
    )
    return app


@pytest.fixture
def client(app):
    """Create test client."""
    return app.test_client()


class TestRoutes:
    """Test cases for Flask routes."""

    def test_index_route(self, client):
        """Test main page route."""
        response = client.get("/")
        assert response.status_code == 200
        assert b"Kroki Generator" in response.data
        assert b"diagram_type" in response.data

    def test_health_route(self, client):
        """Test health check route."""
        response = client.get("/health")
        assert response.status_code == 200

        data = json.loads(response.data)
        assert data["status"] == "healthy"
        assert data["service"] == "kroki-flask-generator"
        assert data["version"] == "0.1.0"

    @patch("src.routes.KrokiClient")
    def test_generate_diagram_json_success(self, mock_kroki_class, client):
        """Test successful diagram generation with JSON."""
        # Setup mock
        mock_client = MagicMock()
        mock_kroki_class.return_value = mock_client
        mock_client.generate_diagram.return_value = (b"fake-image-data", "image/png")

        # Test request
        response = client.post(
            "/api/generate",
            json={
                "diagram_type": "mermaid",
                "output_format": "png",
                "diagram_source": "graph TD\nA --> B",
            },
            content_type="application/json",
        )

        assert response.status_code == 200
        assert response.data == b"fake-image-data"
        assert response.content_type == "image/png"
        assert "filename=diagram.png" in response.headers.get("Content-Disposition", "")

        # Verify client was called correctly
        mock_client.generate_diagram.assert_called_once_with(
            diagram_type="mermaid",
            output_format="png",
            diagram_source="graph TD\nA --> B",
        )

    @patch("src.routes.KrokiClient")
    def test_generate_diagram_text_success(self, mock_kroki_class, client):
        """Test successful diagram generation with text/plain."""
        # Setup mock
        mock_client = MagicMock()
        mock_kroki_class.return_value = mock_client
        mock_client.generate_diagram.return_value = (b"fake-svg-data", "image/svg+xml")

        # Test request
        response = client.post(
            "/api/generate?diagram_type=plantuml&output_format=svg",
            data="@startuml\nA -> B\n@enduml",
            content_type="text/plain",
        )

        assert response.status_code == 200
        assert response.data == b"fake-svg-data"
        assert "image/svg+xml" in response.content_type

        mock_client.generate_diagram.assert_called_once_with(
            diagram_type="plantuml",
            output_format="svg",
            diagram_source="@startuml\nA -> B\n@enduml",
        )

    def test_generate_diagram_invalid_content_type(self, client):
        """Test invalid content type handling."""
        response = client.post(
            "/api/generate", data="some data", content_type="text/html"
        )

        assert response.status_code == 400
        data = json.loads(response.data)
        assert "Content-Type must be" in data["error"]

    def test_generate_diagram_invalid_json(self, client):
        """Test invalid JSON handling."""
        response = client.post(
            "/api/generate", data="invalid json", content_type="application/json"
        )

        assert response.status_code == 400
        data = json.loads(response.data)
        assert "Invalid JSON data" in data["error"]

    def test_generate_diagram_missing_fields(self, client):
        """Test missing required fields."""
        response = client.post(
            "/api/generate",
            json={"diagram_type": "mermaid"},
            content_type="application/json",
        )

        assert response.status_code == 400
        data = json.loads(response.data)
        assert "Missing required fields" in data["error"]
        assert "output_format" in data["error"]
        assert "diagram_source" in data["error"]

    @patch("src.routes.KrokiClient")
    def test_generate_diagram_kroki_error(self, mock_kroki_class, client):
        """Test KrokiError handling."""
        # Setup mock to raise KrokiError
        mock_client = MagicMock()
        mock_kroki_class.return_value = mock_client
        mock_client.generate_diagram.side_effect = KrokiError("Invalid diagram syntax")

        response = client.post(
            "/api/generate",
            json={
                "diagram_type": "mermaid",
                "output_format": "png",
                "diagram_source": "invalid syntax",
            },
            content_type="application/json",
        )

        assert response.status_code == 400
        data = json.loads(response.data)
        assert data["error"] == "Invalid diagram syntax"

    @patch("src.routes.KrokiClient")
    def test_generate_diagram_unexpected_error(self, mock_kroki_class, client):
        """Test unexpected error handling."""
        # Setup mock to raise unexpected exception
        mock_client = MagicMock()
        mock_kroki_class.return_value = mock_client
        mock_client.generate_diagram.side_effect = ValueError("Unexpected error")

        response = client.post(
            "/api/generate",
            json={
                "diagram_type": "mermaid",
                "output_format": "png",
                "diagram_source": "graph TD\nA --> B",
            },
            content_type="application/json",
        )

        assert response.status_code == 500
        data = json.loads(response.data)
        assert data["error"] == "Internal server error"
