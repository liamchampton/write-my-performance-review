"""
AI Service module for Activity Impact Tracker - handles Azure AI Foundry integration
"""
from __future__ import annotations

from azure.ai.inference import ChatCompletionsClient
from azure.core.credentials import AzureKeyCredential
from azure.core.exceptions import HttpResponseError
from config import AZURE_AI_ENDPOINT, AZURE_AI_KEY, AZURE_AI_MODEL


# Global AI client instance
ai_client = None


def initialize_ai() -> ChatCompletionsClient | None:
    """
    Initialize Azure AI Foundry client for generating activity summaries.
    
    Returns:
        ChatCompletionsClient or None: Initialized client or None if credentials missing
    """
    global ai_client
    
    if not AZURE_AI_ENDPOINT or not AZURE_AI_KEY:
        print("Warning: Azure AI Foundry credentials not configured")
        return None
    
    try:
        ai_client = ChatCompletionsClient(
            endpoint=AZURE_AI_ENDPOINT,
            credential=AzureKeyCredential(AZURE_AI_KEY)
        )
        print("Azure AI Foundry client initialized successfully")
        return ai_client
    except Exception as e:
        print(f"Error initializing Azure AI Foundry client: {e}")
        return None


def generate_activity_summary(title: str, description: str, category: str) -> str | None:
    """
    Generate an AI summary for an activity using Azure AI Foundry.
    
    Args:
        title: Activity title
        description: Activity description
        category: Activity category
        
    Returns:
        str or None: Generated summary or None if generation fails
    """
    if not ai_client:
        return None
    
    try:
        prompt = f"""You are an expert at summarizing professional activities for me, a Microsoft Senior Cloud Advocate.
Create a concise, professional summary (2-3 sentences) of this activity:

Title: {title}
Category: {category}
Description: {description}

Focus on the key impact, audience reached, and technical topics covered. It is especially important to highlight what results I have delivered for my goals, keeping security, quality, and AI in mind, as well as how my behaviors and actions have led me, my team, and Microsoft to excel, grow, and build trust."""

        response = ai_client.complete(
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful assistant that creates concise professional summaries."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            model=AZURE_AI_MODEL,
            temperature=0.7,
            max_tokens=150
        )
        
        return response.choices[0].message.content.strip()
    
    except HttpResponseError as e:
        print(f"Azure AI API error: {e}")
        return None
    except Exception as e:
        print(f"Error generating summary: {e}")
        return None


def generate_review_summary(activities: list) -> str | None:
    """
    Generate a comprehensive performance review summary from multiple activities.
    
    Args:
        activities: List of activity dictionaries with ai_summary field
        
    Returns:
        str or None: Generated review summary or None if generation fails
    """
    if not ai_client:
        return None
    
    try:
        # Build a comprehensive list of all activity summaries
        summaries_text = []
        for idx, activity in enumerate(activities, 1):
            summary = activity.get('ai_summary', '')
            title = activity.get('title', 'Untitled')
            category = activity.get('category', 'General')
            date = activity.get('date', '')
            
            if summary:
                summaries_text.append(f"{idx}. [{category}] {title} ({date})\n   {summary}")
        
        combined_summaries = "\n\n".join(summaries_text)
        
        prompt = f"""You are an expert at writing performance reviews for Microsoft Cloud Advocates.

Based on the following {len(activities)} activities and their impact summaries, create a comprehensive performance review summary that:
- Highlights key accomplishments and overall impact
- Mentions quantifiable metrics (audience size, views, engagement)
- Groups related activities by theme or category
- Emphasizes technical depth and community engagement
- Is suitable for inclusion in a formal performance review
- Uses professional language and active voice

Activities:

{combined_summaries}

Write a compelling performance review summary (3-5 paragraphs) that showcases the breadth and impact of these activities:"""

        response = ai_client.complete(
            messages=[
                {
                    "role": "system",
                    "content": "You are an expert at writing compelling, metrics-driven performance reviews for technology professionals."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            model=AZURE_AI_MODEL,
            temperature=0.7,
            max_tokens=800
        )
        
        return response.choices[0].message.content.strip()
    
    except HttpResponseError as e:
        print(f"Azure AI API error: {e}")
        return None
    except Exception as e:
        print(f"Error generating review summary: {e}")
        return None


def get_ai_status() -> dict[str, bool | str]:
    """
    Get the current status of the AI service.
    
    Returns:
        dict: Status information including availability and model name
    """
    return {
        'enabled': ai_client is not None,
        'available': ai_client is not None,
        'model': AZURE_AI_MODEL if ai_client else None
    }
