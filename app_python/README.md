## DevOps Info Service

### Overview

A simple web application built with **Flask** that provides comprehensive system introspection, runtime information, and health status. This project serves as a foundation for learning DevOps practices including CI/CD, containerization, and monitoring.

### Prerequisites

- **Python** 3.10+
- **pip** (Python package manager)

### Installation

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Running the Application

The application runs on `0.0.0.0:5000` by default.

Custom Configuration
You can change the host and port using environment variables.

```bash
$env:PORT=8080; python app.py
```

### API Endpoints

1. System Information
- URL: GET /
- Description: Returns detailed JSON about the service, system, runtime, and current request.
- Example Response:

```json
{
  "service": { "name": "devops-info-service", "version": "1.0.0" },
  "system": { "platform": "Windows", "python_version": "3.12.0" },
  "runtime": { "uptime_human": "0 hour, 5 minutes" }
}

2. Health Check
- URL: GET /health
- Description: Lightweight endpoint for liveness/readiness probes.
- Example Response:

```json
{
  "status": "healthy",
  "timestamp": "2026-01-28T16:20:00+00:00",
  "uptime_seconds": 300
}

### Configuration

| Variable | Description                     | Default |
| -------- | ------------------------------- | ------- |
| HOST     | Interface to bind the server to | 0.0.0.0 |
| PORT     | Port number to listen on        | 5000    |