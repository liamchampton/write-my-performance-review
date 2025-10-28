# Docker Deployment Guide

This guide explains how to run the Connect Activity Tracker application using Docker.

## Prerequisites

- Docker installed on your system
- Docker Compose (usually comes with Docker Desktop)
- Your Azure AI Foundry credentials

## Quick Start

### Option 1: Using Docker Compose (Recommended)

1. **Ensure your `.env` file exists** with your Azure AI credentials:
   ```bash
   AZURE_AI_FOUNDRY_ENDPOINT=your-endpoint-url
   AZURE_AI_FOUNDRY_KEY=your-api-key
   AZURE_AI_FOUNDRY_MODEL=your-model-name
   ```

2. **Build and start the container**:
   ```bash
   docker-compose up -d
   ```

3. **Access the application**:
   Open your browser to `http://localhost:8080`

4. **View logs** (optional):
   ```bash
   docker-compose logs -f
   ```

5. **Stop the container**:
   ```bash
   docker-compose down
   ```

### Option 2: Using Docker CLI

1. **Build the image**:
   ```bash
   docker build -t connect-activity-tracker .
   ```

2. **Run the container**:
   ```bash
   docker run -d \
     --name connect-app \
     -p 8080:8080 \
     -e AZURE_AI_FOUNDRY_ENDPOINT="your-endpoint-url" \
     -e AZURE_AI_FOUNDRY_KEY="your-api-key" \
     -e AZURE_AI_FOUNDRY_MODEL="your-model-name" \
     -v $(pwd)/activities_data.json:/app/activities_data.json \
     connect-activity-tracker
   ```

3. **Access the application**:
   Open your browser to `http://localhost:8080`

4. **Stop the container**:
   ```bash
   docker stop connect-app
   docker rm connect-app
   ```

## Data Persistence

The Docker setup includes volume mappings to persist your activity data:

- `activities_data.json` is mounted from your host machine
- A `./data` directory can be used for additional persistent storage

Your data will remain even if you stop or remove the container.

## Environment Variables

The following environment variables are required:

| Variable | Description | Example |
|----------|-------------|---------|
| `AZURE_AI_FOUNDRY_ENDPOINT` | Your Azure AI endpoint URL | `https://your-resource.cognitiveservices.azure.com/...` |
| `AZURE_AI_FOUNDRY_KEY` | Your Azure AI API key | `your-api-key-here` |
| `AZURE_AI_FOUNDRY_MODEL` | Model deployment name | `gpt-5-chat` |

## Common Commands

### Rebuild after code changes:
```bash
docker-compose up -d --build
```

### View container logs:
```bash
docker-compose logs -f connect-app
```

### Access container shell:
```bash
docker exec -it connect-activity-tracker /bin/bash
```

### Remove everything (including volumes):
```bash
docker-compose down -v
```

## Troubleshooting

### Port already in use
If port 8080 is already in use, modify the `docker-compose.yml` file:
```yaml
ports:
  - "8081:8080"  # Change 8081 to any available port
```

### Environment variables not loading
Ensure your `.env` file is in the same directory as `docker-compose.yml` and contains valid values.

### Data not persisting
Check that the volume mappings in `docker-compose.yml` point to the correct paths on your host machine.
