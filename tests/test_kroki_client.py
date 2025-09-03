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

    def test_validate_inputs_new_diagram_types(self):
        """Test input validation with new diagram types."""
        # Test all new diagram types
        new_types = ["blockdiag", "excalidraw", "ditaa", "seqdiag", "actdiag", "bpmn"]
        for diagram_type in new_types:
            # Should not raise
            self.client._validate_inputs(diagram_type, "png", "sample source")

    def test_preprocess_blockdiag_family(self):
        """Test preprocessing for blockdiag family diagrams."""
        source = """blockdiag {
  A -> B -> C;
}"""

        for diagram_type in ["blockdiag", "seqdiag", "actdiag"]:
            result = self.client._preprocess_blockdiag_family(diagram_type, source)

            # Should add styling
            assert "default_node_color = lightblue;" in result
            assert "default_linecolor = black;" in result
            # Original content should be preserved (but may be restructured)
            assert "A -> B -> C;" in result
            assert "blockdiag {" in result

    def test_preprocess_ditaa(self):
        """Test preprocessing for ditaa diagrams."""
        source = "+--------+\n|  Test  |\n+--------+"
        result = self.client._preprocess_ditaa(source)

        # Ditaa doesn't need preprocessing, should return unchanged
        assert result == source

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

    def test_generate_diagram_http_500(self, requests_mock):
        """Test HTTP 500 error handling."""
        requests_mock.post(
            "http://test-kroki:8000/mermaid/png", status_code=500, text="Server error"
        )

        with pytest.raises(KrokiError, match="Kroki service error"):
            self.client.generate_diagram("mermaid", "png", "graph TD\nA --> B")

    def test_generate_diagram_connection_error(self, requests_mock):
        """Test connection error handling."""
        requests_mock.post(
            "http://test-kroki:8000/mermaid/png",
            exc=requests.exceptions.ConnectionError,
        )

        with pytest.raises(KrokiError, match="Connection error"):
            self.client.generate_diagram("mermaid", "png", "graph TD\nA --> B")

    def test_generate_diagram_success_svg(self, requests_mock):
        """Test successful SVG diagram generation."""
        mock_svg_data = b"<svg>fake svg</svg>"
        requests_mock.post("http://test-kroki:8000/graphviz/svg", content=mock_svg_data)

        result_data, content_type = self.client.generate_diagram(
            "graphviz", "svg", "digraph G { A -> B }"
        )

        assert result_data == mock_svg_data
        assert content_type == "image/svg+xml"
        assert requests_mock.last_request.headers["Accept"] == "image/svg+xml"

    def test_generate_with_large_payload(self, requests_mock):
        """Test large payload handling with temporary files."""
        # Create a client with very small max_bytes to trigger temp file path
        small_client = KrokiClient("http://test-kroki:8000", timeout=5, max_bytes=10)

        mock_image_data = b"fake-image-data"
        requests_mock.post(
            "http://test-kroki:8000/mermaid/png", content=mock_image_data
        )

        large_diagram = "graph TD\n" + "A --> B\n" * 100  # Large diagram source

        result_data, content_type = small_client.generate_diagram(
            "mermaid", "png", large_diagram
        )

        assert result_data == mock_image_data
        assert content_type == "image/png"

    def test_validation_constants(self):
        """Test validation with known supported types and formats."""
        # Test valid diagram types
        valid_types = ["mermaid", "plantuml", "graphviz"]
        for diagram_type in valid_types:
            # Should not raise exception
            self.client._validate_inputs(diagram_type, "png", "test")

        # Test valid output formats
        valid_formats = ["png", "svg"]
        for output_format in valid_formats:
            # Should not raise exception
            self.client._validate_inputs("mermaid", output_format, "test")

    def test_generate_new_diagram_types_blockdiag(self, requests_mock):
        """Test successful BlockDiag diagram generation."""
        mock_image_data = b"fake-blockdiag-png"
        requests_mock.post(
            "http://test-kroki:8000/blockdiag/png", content=mock_image_data
        )

        result_data, content_type = self.client.generate_diagram(
            "blockdiag", "png", "blockdiag {\n  A -> B -> C;\n}"
        )

        assert result_data == mock_image_data
        assert content_type == "image/png"
        assert requests_mock.last_request.headers["Content-Type"] == "text/plain"

    def test_generate_new_diagram_types_excalidraw(self, requests_mock):
        """Test successful Excalidraw diagram generation."""
        mock_image_data = b"fake-excalidraw-svg"
        requests_mock.post(
            "http://test-kroki:8000/excalidraw/svg", content=mock_image_data
        )

        excalidraw_source = '{"type": "excalidraw", "elements": []}'
        result_data, content_type = self.client.generate_diagram(
            "excalidraw", "svg", excalidraw_source
        )

        assert result_data == mock_image_data
        assert content_type == "image/svg+xml"

    def test_generate_new_diagram_types_ditaa(self, requests_mock):
        """Test successful Ditaa diagram generation."""
        mock_image_data = b"fake-ditaa-png"
        requests_mock.post("http://test-kroki:8000/ditaa/png", content=mock_image_data)

        ditaa_source = "+--------+\n|  Test  |\n+--------+"
        result_data, content_type = self.client.generate_diagram(
            "ditaa", "png", ditaa_source
        )

        assert result_data == mock_image_data
        assert content_type == "image/png"

    def test_generate_new_diagram_types_seqdiag(self, requests_mock):
        """Test successful SeqDiag diagram generation."""
        mock_image_data = b"fake-seqdiag-png"
        requests_mock.post(
            "http://test-kroki:8000/seqdiag/png", content=mock_image_data
        )

        seqdiag_source = "seqdiag {\n  A -> B -> C;\n}"
        result_data, content_type = self.client.generate_diagram(
            "seqdiag", "png", seqdiag_source
        )

        assert result_data == mock_image_data
        assert content_type == "image/png"
