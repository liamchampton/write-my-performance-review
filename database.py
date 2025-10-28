"""
Database module for Activity Impact Tracker - handles data persistence
"""
from __future__ import annotations

import json
from datetime import datetime
from typing import Any
from config import DATA_FILE, DEFAULT_CATEGORIES


def load_data() -> dict[str, Any]:
    """
    Load activity data from JSON file.
    Creates file with default categories if it doesn't exist.
    
    Returns:
        dict: Data containing activities and categories
    """
    try:
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        # Initialize with default structure
        initial_data = {
            'activities': [],
            'categories': DEFAULT_CATEGORIES
        }
        save_data(initial_data)
        return initial_data


def save_data(data: dict[str, Any]) -> None:
    """
    Save activity data to JSON file.
    
    Args:
        data: Dictionary containing activities and categories to save
    """
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=2)


def get_next_activity_id(data: dict[str, Any]) -> int:
    """
    Generate the next available activity ID.
    
    Args:
        data: Current data dictionary
        
    Returns:
        int: Next available ID
    """
    if not data['activities']:
        return 1
    return max(activity['id'] for activity in data['activities']) + 1


def find_activity_by_id(data: dict[str, Any], activity_id: int) -> dict[str, Any] | None:
    """
    Find an activity by its ID.
    
    Args:
        data: Current data dictionary
        activity_id: ID to search for
        
    Returns:
        dict or None: Activity data if found, None otherwise
    """
    return next((activity for activity in data['activities'] if activity['id'] == activity_id), None)
