"""Route definitions for the Flask application."""

from flask import Blueprint, render_template, jsonify, request, Response
from src.kroki_client import KrokiClient, KrokiError
import logging

main_bp = Blueprint("main", __name__)
logger = logging.getLogger(__name__)


@main_bp.route("/")
def index():
    """Main page with diagram generation form."""
    return render_template("index.html")


@main_bp.route("/health")
def health():
    """Advanced health check endpoint with Kroki connectivity."""
    from flask import current_app
    import requests
    from datetime import datetime

    health_status = {
        "service": "kroki-flask-generator",
        "version": "0.1.0",
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "status": "healthy",
        "checks": {},
    }

    # Check basic service health
    health_status["checks"]["service"] = {
        "status": "healthy",
        "message": "Flask service running",
    }

    # Check Kroki connectivity
    try:
        kroki_url = current_app.config.get("KROKI_URL", "http://localhost:8000")
        timeout = min(
            current_app.config.get("REQUEST_TIMEOUT", 10), 5
        )  # Max 5s for health check

        response = requests.get(f"{kroki_url}/health", timeout=timeout)
        if response.status_code == 200:
            health_status["checks"]["kroki"] = {
                "status": "healthy",
                "message": f"Kroki service accessible at {kroki_url}",
                "response_time_ms": int(response.elapsed.total_seconds() * 1000),
            }
        else:
            health_status["checks"]["kroki"] = {
                "status": "degraded",
                "message": f"Kroki service returned status {response.status_code}",
            }
            health_status["status"] = "degraded"

    except requests.exceptions.Timeout:
        health_status["checks"]["kroki"] = {
            "status": "unhealthy",
            "message": "Kroki service timeout",
        }
        health_status["status"] = "degraded"

    except requests.exceptions.ConnectionError:
        health_status["checks"]["kroki"] = {
            "status": "unhealthy",
            "message": "Cannot connect to Kroki service",
        }
        health_status["status"] = "degraded"

    except Exception as e:
        health_status["checks"]["kroki"] = {
            "status": "unhealthy",
            "message": f"Kroki health check failed: {str(e)}",
        }
        health_status["status"] = "degraded"

    # Return appropriate HTTP status
    status_code = 200 if health_status["status"] == "healthy" else 503
    return jsonify(health_status), status_code


@main_bp.route("/api/generate", methods=["POST"])
def generate_diagram():
    """Generate diagram via Kroki API."""
    logger.info(f"Received request: Content-Type={request.content_type}")
    try:
        # Parse request data
        if request.content_type == "application/json":
            try:
                data = request.get_json(force=True)
                if not data:
                    return jsonify({"error": "Invalid JSON data"}), 400
            except Exception:
                return jsonify({"error": "Invalid JSON data"}), 400
        elif request.content_type == "text/plain":
            # Support text/plain with query parameters
            data = {
                "diagram_source": request.get_data(as_text=True),
                "diagram_type": request.args.get("diagram_type"),
                "output_format": request.args.get("output_format"),
            }
        else:
            return (
                jsonify(
                    {"error": "Content-Type must be application/json or text/plain"}
                ),
                400,
            )

        # Log received data
        logger.info(f"Parsed data keys: {list(data.keys()) if data else 'None'}")
        
        # Validate required fields
        required_fields = ["diagram_type", "output_format", "diagram_source"]
        missing_fields = [field for field in required_fields if not data.get(field)]
        if missing_fields:
            return (
                jsonify(
                    {"error": f"Missing required fields: {', '.join(missing_fields)}"}
                ),
                400,
            )

        # Generate diagram
        kroki_client = KrokiClient()
        
        # Set theme if provided
        if "diagram_theme" in data:
            # Temporarily set theme in current_app config for this request
            from flask import current_app
            original_theme = current_app.config.get("DIAGRAM_THEME")
            current_app.config["DIAGRAM_THEME"] = data["diagram_theme"]
        
        try:
            image_data, content_type = kroki_client.generate_diagram(
                diagram_type=data["diagram_type"],
                output_format=data["output_format"],
                diagram_source=data["diagram_source"],
            )
        finally:
            # Restore original theme
            if "diagram_theme" in data and original_theme is not None:
                current_app.config["DIAGRAM_THEME"] = original_theme

        # Return binary response
        filename = f"diagram.{data['output_format']}"
        response = Response(
            image_data,
            mimetype=content_type,
            headers={
                "Content-Disposition": f"inline; filename={filename}",
                "Cache-Control": "no-cache, no-store, must-revalidate",
            },
        )

        logger.info(
            f"Generated {data['diagram_type']} diagram in {data['output_format']} format"
        )
        return response

    except KrokiError as e:
        logger.warning(f"Kroki error: {str(e)}")
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        logger.error(f"Unexpected error in generate_diagram: {str(e)}")
        logger.error(f"Error type: {type(e)}")
        import traceback
        logger.error(f"Traceback: {traceback.format_exc()}")
        return jsonify({"error": f"Internal server error: {str(e)}"}), 500
