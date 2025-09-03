"""WSGI entry point for production deployment."""

from src.main import create_app

app = create_app("production")

if __name__ == "__main__":
    app.run()
