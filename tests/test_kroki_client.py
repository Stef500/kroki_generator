"""Tests for Kroki client."""

import pytest
import requests
from src.kroki_client import KrokiClient, KrokiError


class TestKrokiClient:
    """Test cases for KrokiClient."""

    def setup_method(self):
        """Set up test client."""
        self.client = KrokiClient(
            base_url="http://test-kroki:8000", timeout=5, max_bytes=1000
        )

    def test_init(self):
        """Test client initialization."""
        client = KrokiClient("http://example.com", 10)
        assert client.base_url == "http://example.com"
        assert client.timeout == 10

    def test_validate_inputs_valid(self):
        """Test input validation with valid data."""
        # Should not raise
        self.client._validate_inputs("mermaid", "png", "graph TD\\nA --> B")

    def test_validate_inputs_invalid_type(self):
        """Test input validation with invalid diagram type."""
        with pytest.raises(KrokiError, match="Invalid diagram type"):
            self.client._validate_inputs("invalid", "png", "source")

    def test_validate_inputs_invalid_format(self):
        """Test input validation with invalid output format."""
        with pytest.raises(KrokiError, match="Invalid output format"):
            self.client._validate_inputs("mermaid", "pdf", "source")

    def test_validate_inputs_empty_source(self):
        """Test input validation with empty source."""
        with pytest.raises(KrokiError, match="Diagram source cannot be empty"):
            self.client._validate_inputs("mermaid", "png", "")

    def test_generate_diagram_success_png(self, requests_mock):
        """Test successful PNG diagram generation."""
        mock_image_data = b"fake-png-data"
        requests_mock.post(
            "http://test-kroki:8000/mermaid/png", content=mock_image_data
        )

        result_data, content_type = self.client.generate_diagram(
            "mermaid", "png", "graph TD\\nA --> B"
        )

        assert result_data == mock_image_data
        assert content_type == "image/png"
        assert requests_mock.last_request.headers["Content-Type"] == "text/plain"
        assert requests_mock.last_request.headers["Accept"] == "image/png"

    def test_generate_diagram_timeout(self, requests_mock):
        """Test timeout handling."""
        requests_mock.post(
            "http://test-kroki:8000/mermaid/png", exc=requests.exceptions.Timeout
        )

        with pytest.raises(KrokiError, match="Request timeout"):
            self.client.generate_diagram("mermaid", "png", "graph TD\\nA --> B")

    def test_generate_diagram_http_400(self, requests_mock):
        """Test HTTP 400 error handling."""
        requests_mock.post(
            "http://test-kroki:8000/mermaid/png", status_code=400, text="Invalid syntax"
        )

        with pytest.raises(KrokiError, match="Invalid diagram syntax"):
            self.client.generate_diagram("mermaid", "png", "invalid syntax")
