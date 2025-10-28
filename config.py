"""
Configuration module for Activity Impact Tracker
"""
import os

# Data storage file
DATA_FILE = 'activities_data.json'

# Default categories for initial setup
DEFAULT_CATEGORIES = [
    "Speaking Engagement",
    "Blog Post",
    "Video Content",
    "Community Event",
    "Technical Workshop",
    "Documentation",
    "Open Source Contribution",
    "Customer Engagement",
    "Team Collaboration",
    "Mentoring"
]

# Azure AI Foundry configuration
AZURE_AI_ENDPOINT = os.environ.get("AZURE_AI_FOUNDRY_ENDPOINT")
AZURE_AI_KEY = os.environ.get("AZURE_AI_FOUNDRY_KEY")
AZURE_AI_MODEL = os.environ.get("AZURE_AI_FOUNDRY_MODEL", "gpt-5-chat")

# Server configuration
SERVER_HOST = '0.0.0.0'
SERVER_PORT = 8080
DEBUG = True
