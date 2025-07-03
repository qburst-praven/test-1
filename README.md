# Test-1 Web Application

A simple Flask web application for Backstage demo that provides API endpoints with dynamic data and user greetings.

## Features

- REST API endpoints with JSON responses
- Real-time date and time data
- Personalized greeting using environment variable
- Health check endpoint
- Dockerized for easy deployment

## API Endpoints

- `GET /` - Application info and available endpoints
- `GET /api/details` - Get detailed information including time, date, and user greeting
- `GET /health` - Health check endpoint

## Running Locally

```bash
# Install dependencies
pip install -r requirements.txt

# Set the USER environment variable (optional)
export USER="YourName"

# Run the application
python app.py
```

The application will start on `http://localhost:8080`

## Testing the API

```bash
# Get application details
curl http://localhost:8080/api/details

# Health check
curl http://localhost:8080/health

# Application info
curl http://localhost:8080/
```

## Running with Docker

### Build the Docker image
```bash
docker build -t test-1 .
```

### Run the container
```bash
# Run with default user and port binding
docker run -p 8080:8080 test-1

# Run with custom user
docker run -p 8080:8080 -e USER="CustomUser" test-1

# Run with custom port
docker run -p 3000:8080 -e USER="CustomUser" test-1
```

## Environment Variables

- `USER`: The name to display in the greeting (defaults to "BackstageUser")
- `PORT`: The port to run the application on (defaults to 8080)

## Example API Response

```json
{
  "message": "Hello BackstageUser",
  "timestamp": "2024-01-15 14:30:25",
  "date": "2024-01-15",
  "time": "14:30:25",
  "day": "Monday",
  "app": "Test-1 Application",
  "status": "running"
}
```

## Docker Image Details

- Base image: `python:3.11-slim`
- Dependencies: Flask 3.0.0
- Non-root user for security
- Exposes port 8080 