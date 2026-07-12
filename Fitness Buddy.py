"""
AI Fitness Buddy — Flask Application Entry Point
=================================================
Runs with:  python app.py
Production: gunicorn -w 4 -b 0.0.0.0:5000 app:app
"""

import os
import logging
from flask import Flask, render_template
from flask_cors import CORS
from dotenv import load_dotenv

# Load .env FIRST before anything else reads os.getenv()
load_dotenv()

# ─── Logging ────────────────────────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s — %(message)s",
)
logger = logging.getLogger(__name__)

# ─── App Factory ────────────────────────────────────────────────────────────
def create_app() -> Flask:
    app = Flask(__name__, template_folder="templates", static_folder="static")

    # Security
    app.secret_key = os.getenv("FLASK_SECRET_KEY", "fitbuddy-dev-secret-2025-change-me!")
    app.config["SESSION_COOKIE_HTTPONLY"] = True
    app.config["SESSION_COOKIE_SAMESITE"] = "Lax"

    # CORS (needed if frontend is served separately)
    CORS(app, supports_credentials=True)

    # ── Register Blueprints ──────────────────────────────────────────────
    from routes.chat import chat_bp
    from routes.fitness import fitness_bp
    from routes.calculator import calculator_bp
    from routes.profile import profile_bp

    app.register_blueprint(chat_bp)
    app.register_blueprint(fitness_bp)
    app.register_blueprint(calculator_bp)
    app.register_blueprint(profile_bp)

    # ── Page Routes ─────────────────────────────────────────────────────
    @app.route("/")
    def index():
        return render_template("index.html")

    @app.route("/chat")
    def chat():
        return render_template("chat.html")

    @app.route("/dashboard")
    def dashboard():
        return render_template("dashboard.html")

    @app.route("/calculator")
    def calculator():
        return render_template("calculator.html")

    @app.route("/planner")
    def planner():
        return render_template("planner.html")

    @app.route("/profiles")
    def profiles():
        return render_template("profiles.html")

    # ── Health check ─────────────────────────────────────────────────────
    @app.route("/health")
    def health():
        return {"status": "ok", "app": os.getenv("APP_NAME", "AI Fitness Buddy")}

    # ── Error handlers ───────────────────────────────────────────────────
    @app.errorhandler(404)
    def not_found(e):
        return render_template("404.html"), 404

    @app.errorhandler(500)
    def server_error(e):
        logger.error("Internal server error: %s", e)
        return {"error": "Internal server error."}, 500

    logger.info("AI Fitness Buddy application created and ready.")
    return app


# ─── Entry point ────────────────────────────────────────────────────────────
app = create_app()

if __name__ == "__main__":
    debug = os.getenv("FLASK_DEBUG", "True").lower() == "true"
    port = int(os.getenv("PORT", 5000))
    logger.info("Starting server on http://0.0.0.0:%d  debug=%s", port, debug)
    app.run(host="0.0.0.0", port=port, debug=debug)

