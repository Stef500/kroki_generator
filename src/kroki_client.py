"""Kroki HTTP client for diagram generation."""

import tempfile
import requests
from typing import Tuple
from flask import current_app


class KrokiError(Exception):
    """Exception raised for Kroki-related errors."""
    pass


class KrokiClient:
    """HTTP client for Kroki service."""

    def __init__(
        self, base_url: str = None, timeout: int = None, max_bytes: int = None
    ):
        """Initialize Kroki client."""
        self.base_url = base_url or (
            current_app.config["KROKI_URL"] if current_app else "http://localhost:8000"
        )
        self.timeout = timeout or (
            current_app.config["REQUEST_TIMEOUT"] if current_app else 10
        )
        self.max_bytes = max_bytes or (
            current_app.config["MAX_BYTES"] if current_app else 1000000
        )

    def generate_diagram(
        self, diagram_type: str, output_format: str, diagram_source: str
    ) -> Tuple[bytes, str]:
        """
        Generate diagram using Kroki service.

        Args:
            diagram_type: Type of diagram (mermaid, plantuml, graphviz)
            output_format: Output format (png, svg)
            diagram_source: Source code of the diagram

        Returns:
            Tuple of (image_bytes, content_type)

        Raises:
            KrokiError: If generation fails
        """
        # Validate inputs
        self._validate_inputs(diagram_type, output_format, diagram_source)

        # Preprocess diagram source based on type and theme
        diagram_source = self._preprocess_diagram_source(diagram_type, diagram_source)

        # Prepare request
        url = f"{self.base_url}/{diagram_type}/{output_format}"
        headers = {
            "Content-Type": "text/plain",
            "Accept": (
                f"image/{output_format}" if output_format != "svg" else "image/svg+xml"
            ),
        }

        try:
            # Handle large payloads with temporary files
            if len(diagram_source.encode("utf-8")) > self.max_bytes:
                return self._generate_with_tempfile(
                    url, headers, diagram_source, output_format
                )
            else:
                return self._generate_direct(
                    url, headers, diagram_source, output_format
                )

        except requests.exceptions.Timeout:
            raise KrokiError("Request timeout - Kroki service is taking too long")
        except requests.exceptions.ConnectionError:
            raise KrokiError("Connection error - Cannot reach Kroki service")
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 400:
                raise KrokiError(f"Invalid diagram syntax: {e.response.text}")
            elif e.response.status_code >= 500:
                raise KrokiError("Kroki service error - Please try again later")
            else:
                raise KrokiError(
                    f"HTTP error {e.response.status_code}: {e.response.text}"
                )

    def _preprocess_diagram_source(self, diagram_type: str, diagram_source: str) -> str:
        """Preprocess diagram source to apply themes and styling."""
        if diagram_type == "mermaid":
            return self._preprocess_mermaid(diagram_source)
        elif diagram_type == "plantuml":
            return self._preprocess_plantuml(diagram_source)
        return diagram_source

    def _preprocess_mermaid(self, source: str) -> str:
        """Add theme configuration to Mermaid diagrams."""
        # Get theme from config or default to base (light theme)
        theme = current_app.config.get("DIAGRAM_THEME", "base") if current_app else "base"
        
        # Map our theme names to Mermaid theme names
        mermaid_themes = {
            "default": "base",
            "light": "base", 
            "dark": "dark",
            "neutral": "neutral",
            "forest": "forest"
        }
        
        mermaid_theme = mermaid_themes.get(theme, "base")
        
        # Check if the source already contains theme configuration
        if "%%{init:" in source or "theme:" in source:
            return source
            
        # Add theme configuration at the beginning
        theme_config = f"%%{{init: {{'theme': '{mermaid_theme}'}}}}%%\n"
        return theme_config + source

    def _preprocess_plantuml(self, source: str) -> str:
        """Add styling to PlantUML diagrams."""
        # For PlantUML, we can add skinparams for light background
        if not source.strip().startswith("@startuml"):
            return source
            
        # Insert skinparam after @startuml
        lines = source.split('\n')
        if len(lines) > 0 and lines[0].strip().startswith("@startuml"):
            # Add light theme skinparams
            skinparams = [
                "!theme plain",
                "skinparam backgroundColor white",
                "skinparam defaultFontColor black"
            ]
            # Insert after @startuml line
            lines = lines[:1] + skinparams + lines[1:]
            return '\n'.join(lines)
        return source

    def _validate_inputs(
        self, diagram_type: str, output_format: str, diagram_source: str
    ):
        """Validate input parameters."""
        valid_types = ["mermaid", "plantuml", "graphviz"]
        valid_formats = ["png", "svg"]

        if diagram_type not in valid_types:
            raise KrokiError(
                f"Invalid diagram type: {diagram_type}. Must be one of {valid_types}"
            )

        if output_format not in valid_formats:
            raise KrokiError(
                f"Invalid output format: {output_format}. Must be one of {valid_formats}"
            )

        if not diagram_source or not diagram_source.strip():
            raise KrokiError("Diagram source cannot be empty")

    def _generate_direct(
        self, url: str, headers: dict, diagram_source: str, output_format: str
    ) -> Tuple[bytes, str]:
        """Generate diagram with direct HTTP request."""
        response = requests.post(
            url,
            data=diagram_source.encode("utf-8"),
            headers=headers,
            timeout=self.timeout,
        )
        response.raise_for_status()

        content_type = (
            f"image/{output_format}" if output_format != "svg" else "image/svg+xml"
        )
        return response.content, content_type

    def _generate_with_tempfile(
        self, url: str, headers: dict, diagram_source: str, output_format: str
    ) -> Tuple[bytes, str]:
        """Generate diagram using temporary file for large payloads."""
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".txt", delete=False
        ) as tmp_file:
            tmp_file.write(diagram_source)
            tmp_file_path = tmp_file.name

        try:
            with open(tmp_file_path, "rb") as f:
                response = requests.post(
                    url, data=f, headers=headers, timeout=self.timeout
                )
            response.raise_for_status()

            content_type = (
                f"image/{output_format}" if output_format != "svg" else "image/svg+xml"
            )
            return response.content, content_type

        finally:
            # Cleanup temporary file
            import os

            try:
                os.unlink(tmp_file_path)
            except OSError:
                pass
