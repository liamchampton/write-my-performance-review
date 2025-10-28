"""
Static file routes for Activity Impact Tracker
"""
from __future__ import annotations

import os
from flask import Blueprint, send_from_directory

static_bp = Blueprint('static_files', __name__)


@static_bp.route('/')
def index():
    """Serve the main index.html page."""
    return send_from_directory('static', 'index.html')


@static_bp.route('/<path:path>')
def serve_static(path):
    """Serve static files (CSS, JS, etc.)."""
    return send_from_directory('static', path)
