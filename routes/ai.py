"""
AI routes for Activity Impact Tracker
"""
from __future__ import annotations

from flask import Blueprint, request, jsonify
from ai_service import generate_activity_summary, generate_review_summary, get_ai_status

ai_bp = Blueprint('ai', __name__)


@ai_bp.route('/api/generate-summary', methods=['POST'])
def generate_summary():
    """Generate an AI summary for an activity."""
    data = request.json
    
    summary = generate_activity_summary(
        title=data.get('title', ''),
        description=data.get('description', ''),
        category=data.get('category', '')
    )
    
    if summary:
        return jsonify({'summary': summary})
    else:
        return jsonify({'error': 'Could not generate summary. AI service may not be available.'}), 500


@ai_bp.route('/api/generate-review-summary', methods=['POST'])
def generate_performance_review_summary():
    """Generate a performance review summary from all activities."""
    data = request.json
    activities = data.get('activities', [])
    
    if not activities:
        return jsonify({'error': 'No activities provided'}), 400
    
    summary = generate_review_summary(activities)
    
    if summary:
        return jsonify({'summary': summary})
    else:
        return jsonify({'error': 'Could not generate review summary. AI service may not be available.'}), 500


@ai_bp.route('/api/ai-status', methods=['GET'])
def ai_status():
    """Get the status of the AI service."""
    return jsonify(get_ai_status())
