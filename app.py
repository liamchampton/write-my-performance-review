"""
Activity Impact Tracker - A tool for Microsoft Cloud Advocates to track
and visualize their activities and impact across different engagement areas.

Main application entry point.
"""
from __future__ import annotations

from flask import Flask
from flask_cors import CORS

from config import SERVER_HOST, SERVER_PORT, DEBUG
from ai_service import initialize_ai

# Import route blueprints
from routes.static_files import static_bp
from routes.activities import activities_bp
from routes.categories import categories_bp
from routes.stats import stats_bp
from routes.ai import ai_bp

# Initialize Flask application
app = Flask(__name__)
CORS(app)

# Register blueprints
app.register_blueprint(static_bp)
app.register_blueprint(activities_bp)
app.register_blueprint(categories_bp)
app.register_blueprint(stats_bp)
app.register_blueprint(ai_bp)

if __name__ == '__main__':
    # Initialize AI client on startup
    initialize_ai()
    
    # Start the Flask server
    app.run(host=SERVER_HOST, port=SERVER_PORT, debug=DEBUG)
