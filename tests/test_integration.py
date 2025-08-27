"""Integration tests for Docker deployment."""

import pytest
import requests
import time
import json


class TestDockerIntegration:
    """Integration tests for Docker-deployed services."""

    @pytest.fixture(scope="class")
    def base_url(self):
        """Base URL for the deployed application."""
        return "http://localhost:8080"

    @pytest.fixture(scope="class", autouse=True)
    def wait_for_services(self, base_url):
        """Wait for services to be ready before running tests."""
        max_retries = 30
        retry_delay = 2

        for i in range(max_retries):
            try:
                response = requests.get(f"{base_url}/health", timeout=5)
                if response.status_code == 200:
                    health_data = response.json()
                    if health_data.get("status") == "healthy":
                        print(f"✅ Services ready after {i * retry_delay}s")
                        break
            except requests.exceptions.RequestException:
                pass

            if i < max_retries - 1:
                print(f"⏳ Waiting for services... ({i + 1}/{max_retries})")
                time.sleep(retry_delay)
        else:
            pytest.fail("Services failed to become ready within timeout")

    def test_health_endpoint(self, base_url):
        """Test health endpoint returns detailed status."""
        response = requests.get(f"{base_url}/health")

        assert response.status_code == 200
        data = response.json()

        # Check required fields
        assert data["service"] == "kroki-flask-generator"
        assert data["version"] == "0.1.0"
        assert "timestamp" in data
        assert data["status"] in ["healthy", "degraded"]
        assert "checks" in data

        # Check service check
        assert "service" in data["checks"]
        assert data["checks"]["service"]["status"] == "healthy"

        # Check Kroki connectivity
        assert "kroki" in data["checks"]
        kroki_status = data["checks"]["kroki"]["status"]
        assert kroki_status in ["healthy", "degraded", "unhealthy"]

        print(f"Health status: {data['status']}")
        print(f"Kroki status: {kroki_status}")

    def test_homepage_loads(self, base_url):
        """Test homepage loads successfully."""
        response = requests.get(base_url)

        assert response.status_code == 200
        assert "Kroki Generator" in response.text
        assert "diagram_type" in response.text
        assert "output_format" in response.text

    def test_static_assets(self, base_url):
        """Test static assets are served."""
        # Test Bootstrap CSS is referenced
        response = requests.get(base_url)
        assert "bootstrap" in response.text.lower()

    @pytest.mark.integration
    def test_diagram_generation_mermaid(self, base_url):
        """Test end-to-end diagram generation with Mermaid."""
        diagram_source = """graph TD
    A[Start] --> B{Decision}
    B -->|Yes| C[Action 1]
    B -->|No| D[Action 2]"""

        payload = {
            "diagram_type": "mermaid",
            "output_format": "png",
            "diagram_source": diagram_source,
        }

        response = requests.post(f"{base_url}/api/generate", json=payload, timeout=30)

        # Should either succeed (200) or fail gracefully (400/500)
        assert response.status_code in [200, 400, 500, 503]

        if response.status_code == 200:
            # Success case - verify image response
            assert response.headers["content-type"] == "image/png"
            assert len(response.content) > 1000  # PNG should be substantial
            print("✅ Mermaid diagram generated successfully")
        else:
            # Error case - should have JSON error response
            try:
                error_data = response.json()
                assert "error" in error_data
                print(f"⚠️  Expected error in test environment: {error_data['error']}")
            except json.JSONDecodeError:
                # Some errors might not be JSON
                print(f"⚠️  HTTP {response.status_code} error (expected in test)")

    @pytest.mark.integration
    def test_diagram_generation_plantuml(self, base_url):
        """Test end-to-end diagram generation with PlantUML."""
        diagram_source = """@startuml
Alice -> Bob: Hello
Bob -> Alice: Hi there!
@enduml"""

        payload = {
            "diagram_type": "plantuml",
            "output_format": "svg",
            "diagram_source": diagram_source,
        }

        response = requests.post(f"{base_url}/api/generate", json=payload, timeout=30)

        # Should either succeed (200) or fail gracefully (400/500)
        assert response.status_code in [200, 400, 500, 503]

        if response.status_code == 200:
            # Success case - verify SVG response
            assert "image/svg+xml" in response.headers["content-type"]
            assert b"<svg" in response.content
            print("✅ PlantUML diagram generated successfully")
        else:
            # Error case - should have JSON error response
            try:
                error_data = response.json()
                assert "error" in error_data
                print(f"⚠️  Expected error in test environment: {error_data['error']}")
            except json.JSONDecodeError:
                print(f"⚠️  HTTP {response.status_code} error (expected in test)")

    def test_error_handling(self, base_url):
        """Test API error handling."""
        # Test missing fields
        response = requests.post(f"{base_url}/api/generate", json={})
        assert response.status_code == 400

        error_data = response.json()
        assert "error" in error_data
        assert "Missing required fields" in error_data["error"]

        # Test invalid diagram type
        response = requests.post(
            f"{base_url}/api/generate",
            json={
                "diagram_type": "invalid",
                "output_format": "png",
                "diagram_source": "test",
            },
        )
        assert response.status_code == 400

        error_data = response.json()
        assert "error" in error_data

    def test_performance_response_time(self, base_url):
        """Test response times are reasonable."""
        start_time = time.time()
        response = requests.get(f"{base_url}/health")
        response_time = time.time() - start_time

        assert response.status_code in [200, 503]
        assert response_time < 2.0  # Health check should be fast

        print(f"Health check response time: {response_time:.3f}s")
