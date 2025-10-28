"""
Category routes for Activity Impact Tracker
"""
from __future__ import annotations

from flask import Blueprint, request, jsonify
from database import load_data, save_data

categories_bp = Blueprint('categories', __name__)


@categories_bp.route('/api/categories', methods=['GET'])
def get_categories():
    """Get all available categories."""
    data = load_data()
    return jsonify({'categories': data.get('categories', [])})


@categories_bp.route('/api/categories', methods=['POST'])
def create_category():
    """Add a new category."""
    category_data = request.json
    data = load_data()
    
    new_category = category_data['name']
    
    if new_category not in data['categories']:
        data['categories'].append(new_category)
        save_data(data)
    
    return jsonify({'name': new_category}), 201
