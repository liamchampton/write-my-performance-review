#!/bin/bash
# Helper script to load environment variables and start the Flask application

# Check if .env file exists
if [ ! -f .env ]; then
    echo "⚠️  .env file not found"
    echo "📝 Creating .env from .env.example..."
    cp .env.example .env
    echo ""
    echo "✅ Created .env file"
    echo "📝 Please edit .env with your Azure AI Foundry credentials:"
    echo "   - AZURE_AI_FOUNDRY_ENDPOINT"
    echo "   - AZURE_AI_FOUNDRY_KEY"
    echo "   - AZURE_AI_FOUNDRY_MODEL (optional)"
    echo ""
    read -p "Press Enter after editing .env to continue, or Ctrl+C to exit..."
fi

# Load environment variables from .env
echo "📂 Loading environment variables from .env..."
export $(cat .env | grep -v '^#' | xargs)

# Check if required variables are set
if [ -z "$AZURE_AI_FOUNDRY_ENDPOINT" ] || [ -z "$AZURE_AI_FOUNDRY_KEY" ]; then
    echo "⚠️  Warning: Azure AI Foundry not configured"
    echo "   AI summary generation will be disabled"
    echo "   To enable it, set AZURE_AI_FOUNDRY_ENDPOINT and AZURE_AI_FOUNDRY_KEY in .env"
    echo ""
fi

# Start Flask application
echo "🚀 Starting Flask application..."
python app.py
