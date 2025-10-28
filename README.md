# 🎯 Activity Impact Tracker

A full-stack Python and JavaScript application to track and manage your activities and impact.

## 📋 Features

- **Track Activities**: Add, view, update, and delete activities with detailed information
- **🤖 AI-Powered Summaries**: Generate professional impact summaries using Azure AI Foundry
- **🤖 AI Performance Reviews**: Generate comprehensive performance review summaries from all your activities
- **Impact Framework**: Visual guide showing the relationship between "WHAT" you achieved and "HOW" you achieved it
- **Activity Categories**: Organize activities by type (Speaking, Blog Posts, Videos, etc.)
- **Tagging System**: Add custom tags to activities for better organization
- **Statistics Dashboard**: View real-time stats showing total activities and categories
- **Category Filtering**: Filter activities by category to focus on specific work types
- **Collapsible Sections**: Clean, minimalistic UI with collapsible filter, activities, and performance summary sections
- **Modern Glassmorphism Design**: Sleek, responsive interface with gradient backgrounds and glass-effect cards
- **Docker Support**: Run locally with virtual environment or deploy with Docker Compose

## 🏗️ Architecture

### Backend (Python Flask)
- **Framework**: Flask 3.0.3 with CORS support
- **Data Storage**: JSON file-based storage (activities_data.json)
- **API Endpoints**:
  - `GET /api/activities` - Get all activities (with optional category filter)
  - `POST /api/activities` - Create a new activity
  - `GET /api/activities/<id>` - Get a specific activity
  - `PUT /api/activities/<id>` - Update an activity
  - `DELETE /api/activities/<id>` - Delete an activity
  - `GET /api/categories` - Get all categories
  - `POST /api/categories` - Add a new category
  - `GET /api/stats` - Get activity statistics
  - `POST /api/generate-summary` - Generate AI-powered activity summary
  - `POST /api/generate-review-summary` - Generate performance review summary
  - `GET /api/ai-status` - Check if AI service is available

### Frontend (JavaScript)
- **Pure JavaScript**: No framework dependencies
- **Fetch API**: Modern HTTP requests to the Flask backend
- **Responsive Design**: Mobile-friendly CSS Grid and Flexbox layout
- **Real-time Updates**: Dynamic content updates without page refresh

## 🚀 Getting Started

### Prerequisites
- Python 3.9 or higher
- pip (Python package manager)
- **For Docker**: Docker installed
- **Optional**: Azure AI Foundry project with deployed model for AI-powered summaries
  - Create at: https://ai.azure.com/

### Installation

There are two ways to run this application: **locally with a virtual environment** or **using Docker**.

---

## Option 1: Running Locally with Virtual Environment (Recommended for Development)

### 1. Clone the repository:
```bash
git clone https://github.com/liamchampton/write-my-performance-review.git
cd write-my-performance-review
```

### 2. Create and activate a virtual environment:

**On macOS/Linux:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

**On Windows:**
```bash
python -m venv .venv
.venv\Scripts\activate
```

**Important:** Always activate the virtual environment before working on the project. You'll know it's activated when you see `(.venv)` in your terminal prompt.

### 3. Install dependencies inside the virtual environment:
```bash
pip install -r requirements.txt
```

### 4. Configure Azure AI Foundry (Optional, for AI summaries):
```bash
# Copy the example environment file
cp .env.example .env

# Edit .env with your Azure AI Foundry details:
# - AZURE_AI_FOUNDRY_ENDPOINT: Your endpoint URL from Azure AI Foundry
# - AZURE_AI_FOUNDRY_KEY: Your API key from project settings
# - AZURE_AI_FOUNDRY_MODEL: Model deployment name (e.g., gpt-5-chat)
```

To get your Azure AI Foundry credentials:
1. Go to https://ai.azure.com/ and sign in
2. Create or open your project
3. Deploy a model (e.g., gpt-5-chat) from the Model catalog
4. Go to Project settings → Copy the endpoint URL and generate an API key
5. Add these values to your `.env` file

### 5. Run the application:

**Option A: Use the start script:**
```bash
./start.sh
```
This script automatically loads environment variables from `.env` and starts the application.

**Option B: Manual start:**

**On macOS/Linux:**
```bash
# Ensure virtual environment is activated
source .venv/bin/activate

# Load environment variables
export $(cat .env | xargs)

# Start the application
python app.py
```

**On Windows:**
```bash
# Ensure virtual environment is activated
.venv\Scripts\activate

# Load environment variables (PowerShell)
Get-Content .env | ForEach-Object {
    if ($_ -match '^([^=]+)=(.*)$') {
        [Environment]::SetEnvironmentVariable($matches[1], $matches[2], 'Process')
    }
}

# Or using Command Prompt
for /f "tokens=*" %i in (.env) do set %i

# Start the application
python app.py
```

The server will start on `http://localhost:8080`

### 6. Open your browser and navigate to:
```
http://localhost:8080
```

### Deactivating the Virtual Environment:
When you're done working, deactivate the virtual environment:
```bash
deactivate
```

---

## Option 2: Running with Docker Compose (Recommended)

Docker Compose provides an isolated, containerized environment without needing to install Python locally.

### 1. Clone the repository:
```bash
git clone https://github.com/liamchampton/write-my-performance-review.git
cd write-my-performance-review
```

### 2. Configure environment variables:
```bash
# Copy the example environment file
cp .env.example .env

# Edit .env with your Azure AI Foundry credentials
# (Required for AI summaries, optional otherwise)
```

### 3. Build and start the container:
```bash
docker-compose up -d
```

This command will:
- Build the Docker image from the Dockerfile
- Start the container in detached mode (background)
- Mount your `activities_data.json` for data persistence
- Expose the application on port 8080

### 4. Access the application:
Open your browser and navigate to:
```
http://localhost:8080
```

### Docker Compose Commands:

**View logs:**
```bash
docker-compose logs -f
```

**Stop the container:**
```bash
docker-compose down
```

**Rebuild after code changes:**
```bash
docker-compose up -d --build
```

**View running containers:**
```bash
docker-compose ps
```

**Restart the container:**
```bash
docker-compose restart
```

### Data Persistence with Docker:
Your activity data is stored in `activities_data.json` and is mounted as a volume, so your data persists even when containers are stopped or removed.

For more Docker configuration options, see [DOCKER.md](DOCKER.md).

---

**Start tracking your activities!** 🎉

## 📱 How to Use

### Adding an Activity

1. Fill out the "Add New Activity" form:
   - **Title**: Brief description of the activity
   - **Description**: Detailed information about what you did
   - **Date**: When the activity occurred
   - **🤖 AI Summary**: Click "Generate AI Summary" to automatically create a professional summary (requires Azure AI Foundry configuration)
   - **Tags**: Add comma-separated tags (e.g., "Azure, AI, Community")

2. Click "Add Activity" to save

### Viewing Activities

- Each card shows the title, date, category, description, and tags
- The dashboard at the top shows total activities and counts per circle

### Filtering Activities

- Use the filter dropdowns to view activities by specific circle or category
- Click "Clear Filters" to reset and see all activities

### Deleting Activities

- Click the "Delete" button on any activity card
- Confirm the deletion when prompted

## 🤖 AI-Powered Summary Generation

This application integrates with **Azure AI Foundry** to generate professional impact summaries automatically using cloud-hosted AI models.

### How It Works

1. Fill in your activity description and impact details
2. Click the "🤖 Generate AI Summary" button
3. The AI model (hosted in Azure) analyzes your input
4. A concise, professional 2-3 sentence summary is generated
5. The summary highlights key accomplishments and measurable impact

### Setting Up Azure AI Foundry

To enable AI-powered summaries:

1. **Create an Azure AI Foundry project**:
   - Visit: https://ai.azure.com/
   - Sign in with your Microsoft account
   - Create a new project or use an existing one

2. **Deploy a model**:
   - Go to the Model catalog
   - Deploy a model (recommended: `gpt-5-chat` for balance of speed and quality)
   - Note the deployment name

3. **Get your credentials**:
   - Go to Project settings
   - Copy your endpoint URL (format: `https://<resource>.services.ai.azure.com/models`)
   - Generate and copy an API key

4. **Configure environment variables**:
   ```bash
   # Copy the example file
   cp .env.example .env
   
   # Edit .env and add your values:
   AZURE_AI_FOUNDRY_ENDPOINT=https://your-resource.services.ai.azure.com/models
   AZURE_AI_FOUNDRY_KEY=your-api-key-here
   AZURE_AI_FOUNDRY_MODEL=gpt-4o-mini
   ```

5. **Load environment variables and start the application**:
   ```bash
   export $(cat .env | xargs)
   python app.py
   ```

The application will automatically connect to Azure AI Foundry when environment variables are configured. If not configured, the app works normally but without AI summary generation.

### Privacy & Security

- All data is sent securely to Azure AI Foundry via HTTPS
- Your API key should be kept secret (never commit .env to git)
- Azure AI Foundry follows Microsoft's security and compliance standards

## 📂 Project Structure

```
write-my-performance-review/
├── app.py                      # Main Flask application entry point
├── config.py                   # Configuration and environment variables
├── database.py                 # Data persistence layer (JSON file operations)
├── ai_service.py              # Azure AI Foundry integration
├── requirements.txt            # Python dependencies
├── README.md                   # Project documentation
├── SECURITY.md                 # Security guidelines and best practices
├── DOCKER.md                   # Docker deployment guide
├── AZURE_SETUP.md              # Azure AI Foundry setup instructions
├── .env.example                # Environment template
├── .gitignore                  # Git ignore rules
├── pre-commit-check.sh         # Security validation script
├── start.sh                    # Quick start script
├── Dockerfile                  # Docker container configuration
├── docker-compose.yml          # Docker Compose configuration
├── .github/
│   └── instructions/
│       └── python.instructions.md  # Python coding standards
├── routes/                     # API route modules (Flask blueprints)
│   ├── __init__.py
│   ├── activities.py          # Activity CRUD operations
│   ├── categories.py          # Category management
│   ├── stats.py               # Statistics endpoints
│   ├── ai.py                  # AI summary generation
│   └── static_files.py        # Static file serving
├── static/                     # Frontend assets
│   ├── index.html             # Main HTML page
│   ├── styles.css             # Glassmorphism design styles
│   └── app.js                 # Frontend JavaScript logic

```

### Module Descriptions

**Core Application:**
- `app.py` (38 lines) - Minimal entry point, registers blueprints
- `config.py` - Centralized configuration, loads from environment
- `database.py` - Data operations (load, save, find, ID generation)
- `ai_service.py` - Azure AI client initialization and summary generation

**API Routes (Blueprints):**
- `routes/activities.py` - Full CRUD for activities (GET, POST, PUT, DELETE)
- `routes/categories.py` - Category listing and creation
- `routes/stats.py` - Activity statistics and analytics
- `routes/ai.py` - AI summary generation endpoints
- `routes/static_files.py` - Serves frontend files

**Frontend:**
- `static/index.html` - Single-page application
- `static/styles.css` - Modern glassmorphism design with gradient background
- `static/app.js` - Handles API calls, collapsible sections, AI summaries

**Testing:**
- `tests/test_activities.py` - Comprehensive activity route tests with 29 test cases
- `tests/conftest.py` - Shared fixtures for test database and client

**Documentation:**
- `README.md` - Complete usage guide
- `SECURITY.md` - Security checklist and emergency procedures
- `DOCKER.md` - Containerization guide
- `AZURE_SETUP.md` - Azure AI Foundry configuration
- `MIGRATION.md` - Refactoring documentation

**Deployment:**
- `Dockerfile` - Container image definition
- `docker-compose.yml` - Multi-container orchestration
- `start.sh` - Development quick-start script
- `pre-commit-check.sh` - Pre-push security validation
```

## 🎨 Customization

### Adding New Categories

Categories can be added through the API or by editing the initial data in `app.py`:

```python
"categories": [
    "Your Custom Category",
    # ... other categories
]
```

### Changing Port

To run on a different port, modify the last line in `app.py`:

```python
app.run(debug=True, host='0.0.0.0', port=8080)  # Change 8080 to your port
```

## 🔒 Data Storage

- All data is stored in `activities_data.json` in the project root
- The file is automatically created on first run
- Data persists between application restarts
- **Backup recommendation**: Regularly backup this file to prevent data loss

## 🛠️ API Examples

### Create an Activity (cURL)

```bash
curl -X POST http://localhost:8080/api/activities \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Presented at Microsoft Build",
    "description": "Delivered a session on Azure AI",
    "category": "Speaking Engagement",
    "impact_circle": "Your key individual accomplishments that contribute to team, business or customer results",
    "impact_description": "500+ attendees, 95% positive feedback",
    "tags": ["Azure", "AI", "Speaking"]
  }'
```

### Get Statistics

```bash
curl http://localhost:8080/api/stats
```

### Generate AI Summary (cURL)

```bash
curl -X POST http://localhost:8080/api/generate-summary \
  -H "Content-Type: application/json" \
  -d '{
    "description": "Delivered a technical workshop on Azure AI services",
    "impact_description": "Trained 50 developers, 90% satisfaction rate",
    "category": "Technical Workshop",
    "impact_circle": "Your contributions to the success of others"
  }'
```

## 🐛 Troubleshooting

### Port Already in Use
If port 8080 is already in use, either:
- Stop the process using port 8080
- Change the port in `config.py`

### CORS Errors
The application uses `flask-cors` to handle cross-origin requests. Make sure it's installed:
```bash
pip install flask-cors
```

### Missing Dependencies
If you encounter import errors, ensure all dependencies are installed:
```bash
pip install -r requirements.txt
```

### AI Summary Not Working
If the "Generate AI Summary" button is disabled:
- Azure AI Foundry environment variables are not configured
- Check your `.env` file has correct values for:
  - `AZURE_AI_FOUNDRY_ENDPOINT`
  - `AZURE_AI_FOUNDRY_KEY`
  - `AZURE_AI_FOUNDRY_MODEL`
- Ensure environment variables are loaded: `export $(cat .env | xargs)`
- Verify your Azure AI Foundry project has a deployed model
- The app will work fine without AI - it's an optional enhancement
- Check console logs for specific error messages

## 📝 Best Practices from Microsoft Documentation

This application follows best practices from official Microsoft documentation:

- **Flask REST API Design**: Based on Microsoft's guidance for Python web applications
- **JSON Data Handling**: Follows Microsoft's recommendations for data serialization
- Frontend-Backend Separation**: Clean separation of concerns
- **Error Handling**: Comprehensive error handling on both client and server
- **Security**: Input validation and sanitization

## 🔐 Security

### Before Pushing to GitHub

1. **Verify `.env` is ignored**:
   ```bash
   git check-ignore .env
   # Should output: .env
   ```

2. **What's Safe to Commit**:
   - ✅ All code files (`*.py`, `*.js`, `*.html`, `*.css`)
   - ✅ `.env.example` (template with NO real credentials)
   - ✅ `.gitignore` and other config files
   - ✅ Documentation (`*.md` files)
   - ✅ Docker files (use environment variable syntax)

3. **What's NEVER Committed** (in `.gitignore`):
   - ❌ `.env` file (contains your real Azure API keys)
   - ❌ `activities_data.json` (contains your personal activity data)
   - ❌ `.venv/` directory
   - ❌ `__pycache__/` and `*.pyc` files

### Security Best Practices

- **Never hard-code credentials** - Always use environment variables
- **Rotate API keys regularly** - Every 90 days minimum
- **Use Azure Key Vault** for production deployments
- **Review SECURITY.md** for complete security guidelines
- **Report security issues** privately, never in public issues

For detailed security guidelines, see [SECURITY.md](SECURITY.md).

## 🤝 Contributing

Feel free to enhance this application with additional features such as:
- Export to CSV/Excel
- Data visualization with charts
- User authentication
- Database integration (SQLite, PostgreSQL, etc.)
- Search functionality
- Activity editing
- Bulk operations

---
