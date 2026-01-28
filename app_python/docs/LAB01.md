# Lab 01 - DevOps Info Service: Python Implementation
## Framework Selection
For this project, I selected **Flask**.

### Comparison

| Feature | Flask | FastAPI | Django |
|---------|-------|---------|--------|
| **Type** | Microframework | Microframework | Full-stack Framework |
| **Architecture** | Synchronous (WSGI) | Asynchronous (ASGI) | Monolithic (mostly) |
| **Learning Curve** | Low (Easy to start) | Medium (Type hints, async) | High (Complex ORM, structure) |
| **Performance** | Good | Excellent | Good |
| **Use Case** | Simple services, prototyping | High-load APIs, ML models | Complex enterprise apps |

### Justification
I chose **Flask** because it is lightweight and provides exactly what is needed for a simple system information service without unnecessary overhead. It allows for quick prototyping and has a simple, intuitive syntax for defining routes. While FastAPI offers automatic documentation, Flask is robust enough for this assignment and is an industry standard for many microservices.
## Best Practices Applied
I implemented several Python and DevOps best practices in the application:

1.  **Configuration via Environment Variables**
    Instead of hardcoding settings, I use `os.getenv` to load `HOST` and `PORT`. This adheres to the **12-Factor App** methodology, allowing the app to be configured differently in Dev, Test, and Prod environments without changing code.
    ```python
    HOST = os.getenv('HOST', '0.0.0.0')
    PORT = int(os.getenv('PORT', 5000))
    ```

2.  **Proper Logging**
    I used the standard `logging` library instead of `print()` statements. This allows for better log management (levels like INFO, ERROR) and is essential for monitoring in production environments.
    ```python
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - ...')
    ```

3.  **Clean Code & Documentation**
    - Code is organized into logical blocks.
    - Logic for uptime calculation is separated into a dedicated function `get_uptime()`.
    - Docstrings are added to functions to explain their purpose.
    - Variable names are descriptive (`uptime_seconds`, `platform_version`).

4.  **Error Handling**
    Specific handlers for `404 Not Found` and `500 Internal Server Error` (implicit in Flask, can be extended) ensure that the client receives valid JSON responses even when things go wrong, rather than raw HTML stack traces.

5.  **Dependency Management**
    All dependencies are pinned in `requirements.txt` to ensure reproducibility across different environments.
    ```text
    Flask==3.1.0
    python-dotenv==1.0.1
    ```
## API Documentation
## 3. API Documentation

### Main Endpoint (`GET /`)
Returns comprehensive information about the running service and the host system.

**Response Example:**
```json
{
  "service": {
    "name": "devops-info-service",
    "version": "1.0.0",
    "framework": "Flask"
  },
  "system": {
    "hostname": "DESKTOP-XYZ",
    "platform": "Windows",
    "python_version": "3.12.4"
  },
  "runtime": {
    "uptime_human": "0 hour, 15 minutes",
    "timezone": "UTC"
  }
}
```
### Health Check (GET /health)
A lightweight endpoint for container orchestrators (like Kubernetes) to verify the app is alive.
**Response Example:**
```json
{
  "status": "healthy",
  "timestamp": "2026-01-28T16:30:00+00:00",
  "uptime_seconds": 900
}
```
## Testing Evidence
**Screenshots:** Place in `docs/screenshots/`.

To verify that the service works as expected, I performed manual testing using both the web browser and command-line tools.

**Verification Steps:**
1.  **Main Endpoint Check:** Opened `http://127.0.0.1:5000/` in the browser to validate the complete JSON structure, ensuring all required sections (`service`, `system`, `runtime`, `request`, and `endpoints`) are present and correct.
2.  **Health Check:** Access `http://127.0.0.1:5000/health` to confirm that the endpoint returns the correct `status`, current `timestamp`, and `uptime_seconds`.
3.  **Formatted Output:** Used `curl` with `jq` to see formatted output in the terminal.

## Challenges & Solutions
Working on Windows with PowerShell presented some specific challenges compared to a standard Linux environment.

**Command Differences (touch, source)**

**Challenge:** Commands like touch to create files or source to activate the virtual environment are not natively available in PowerShell.

**Solution:** I learned to use PowerShell equivalents: `New-Item` (or `ni`) for creating files and `.\venv\Scripts\activate` for activating the environment.

**Curl & JSON Formatting**

**Challenge:** The `curl` command in PowerShell is often an alias for `Invoke-WebRequest`, which parses HTML differently than the Linux `curl` tool. Also, `jq` is not installed by default on Windows.

**Solution:** I used the browser to verify the JSON output structure and formatting, which provides a clear view of the data without needing extra CLI tools.
## GitHub Community
Starring repositories is a way to show appreciation to maintainers and helps projects gain visibility/trust in the community. Following other developers allows me to stay updated on their work, discover new tools, and observe coding practices from experienced engineers, which is crucial for professional growth.