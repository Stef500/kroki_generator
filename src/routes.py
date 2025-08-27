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
    """Health check endpoint."""
    return jsonify(
        {"status": "healthy", "service": "kroki-flask-generator", "version": "0.1.0"}
    )


@main_bp.route("/api/generate", methods=["POST"])
def generate_diagram():
    """Generate diagram via Kroki API."""
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
        image_data, content_type = kroki_client.generate_diagram(
            diagram_type=data["diagram_type"],
            output_format=data["output_format"],
            diagram_source=data["diagram_source"],
        )

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
        return jsonify({"error": "Internal server error"}), 500
