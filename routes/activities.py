"""
Activity routes for Activity Impact Tracker
"""
from __future__ import annotations

from datetime import datetime
from flask import Blueprint, request, jsonify
from database import load_data, save_data, get_next_activity_id, find_activity_by_id

activities_bp = Blueprint('activities', __name__)


@activities_bp.route('/api/activities', methods=['GET'])
def get_activities():
    """Get all activities, optionally filtered by category."""
    data = load_data()
    activities = data['activities']
    
    # Filter by category if provided
    category = request.args.get('category')
    if category:
        activities = [a for a in activities if a.get('category') == category]
    
    # Sort by date (newest first)
    activities.sort(key=lambda x: x.get('date', ''), reverse=True)
    
    return jsonify({'activities': activities, 'total': len(activities)})


@activities_bp.route('/api/activities', methods=['POST'])
def create_activity():
    """Create a new activity."""
    activity_data = request.json
    data = load_data()
    
    # Create new activity with generated ID
    new_activity = {
        'id': get_next_activity_id(data),
        'title': activity_data['title'],
        'description': activity_data['description'],
        'category': activity_data['category'],
        'impact_description': activity_data.get('impact_description', ''),
        'ai_summary': activity_data.get('ai_summary', ''),
        'date': activity_data.get('date', datetime.now().isoformat()),
        'tags': activity_data.get('tags', [])
    }
    
    data['activities'].append(new_activity)
    save_data(data)
    
    return jsonify(new_activity), 201


@activities_bp.route('/api/activities/<int:activity_id>', methods=['GET'])
def get_activity(activity_id):
    """Get a specific activity by ID."""
    data = load_data()
    activity = find_activity_by_id(data, activity_id)
    
    if activity:
        return jsonify(activity)
    return jsonify({'error': 'Activity not found'}), 404


@activities_bp.route('/api/activities/<int:activity_id>', methods=['PUT'])
def update_activity(activity_id):
    """Update an existing activity."""
    data = load_data()
    activity = find_activity_by_id(data, activity_id)
    
    if not activity:
        return jsonify({'error': 'Activity not found'}), 404
    
    update_data = request.json
    
    # Update allowed fields
    activity['title'] = update_data.get('title', activity['title'])
    activity['description'] = update_data.get('description', activity['description'])
    activity['category'] = update_data.get('category', activity['category'])
    activity['impact_description'] = update_data.get('impact_description', activity.get('impact_description', ''))
    activity['ai_summary'] = update_data.get('ai_summary', activity.get('ai_summary', ''))
    activity['tags'] = update_data.get('tags', activity.get('tags', []))
    
    save_data(data)
    
    return jsonify(activity)


@activities_bp.route('/api/activities/<int:activity_id>', methods=['DELETE'])
def delete_activity(activity_id):
    """Delete an activity."""
    data = load_data()
    activity = find_activity_by_id(data, activity_id)
    
    if not activity:
        return jsonify({'error': 'Activity not found'}), 404
    
    data['activities'].remove(activity)
    save_data(data)
    
    return jsonify({'message': 'Activity deleted successfully'})
