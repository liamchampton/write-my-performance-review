"""
Statistics routes for Activity Impact Tracker
"""
from __future__ import annotations

from flask import Blueprint, jsonify
from database import load_data

stats_bp = Blueprint('stats', __name__)


@stats_bp.route('/api/stats', methods=['GET'])
def get_stats():
    """Get activity statistics."""
    data = load_data()
    activities = data['activities']
    
    # Calculate category distribution
    category_counts = {}
    for activity in activities:
        category = activity.get('category', 'Uncategorized')
        category_counts[category] = category_counts.get(category, 0) + 1
    
    return jsonify({
        'total_activities': len(activities),
        'categories_used': len(category_counts),
        'category_distribution': category_counts
    })
