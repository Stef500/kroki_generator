# Multi-stage build for production Flask app
FROM python:3.12-slim AS builder

# Install build dependencies and uv
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/* \
    && curl -LsSf https://astral.sh/uv/install.sh | sh

# Add uv to PATH (uv installs to ~/.local/bin by default)
ENV PATH="/root/.local/bin:$PATH"

# Set work directory
WORKDIR /app

# Copy requirements
COPY pyproject.toml uv.lock ./

# Install dependencies with uv (much faster than pip)
# Use --system to install directly into system Python, not venv
RUN uv sync --no-dev --frozen --system

# Production stage
FROM python:3.12-slim AS production

# Create non-root user
RUN groupadd -r appuser && useradd -r -g appuser appuser

# Install runtime dependencies only
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Set work directory
WORKDIR /app

# Copy installed packages from builder
COPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Copy application code
COPY src/ ./src/
COPY templates/ ./templates/
COPY static/ ./static/
COPY wsgi.py ./
COPY .env.template ./

# Create .env from template if not exists
RUN cp .env.template .env

# Create required directories and set permissions
RUN mkdir -p /app/logs && \
    chown -R appuser:appuser /app

# Switch to non-root user
USER appuser

# Expose port
EXPOSE 8080

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8080/health || exit 1

# Run with gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "--workers", "2", "--worker-class", "sync", "--timeout", "30", "--keep-alive", "5", "--log-level", "info", "--access-logfile", "-", "--error-logfile", "-", "wsgi:app"]