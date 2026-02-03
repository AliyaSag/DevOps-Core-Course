import os
import platform
import socket
import logging
import time
from datetime import datetime, timezone
from flask import Flask, jsonify, request

# Initialize Flask application instance
app = Flask(__name__)

# Application configuration from environment
HOST = os.getenv('HOST', '0.0.0.0')
PORT = int(os.getenv('PORT', 5000))

# Logging configuration
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

start_time = time.time() # record startup timestamp for uptime calculation

def get_uptime():
    """Returns uptime in seconds and hh:mm format."""
    uptime_seconds = int(time.time() - start_time)
    hours = uptime_seconds // 3600
    minutes = (uptime_seconds % 3600) // 60
    return {
        "uptime_seconds": uptime_seconds,
        "uptime_human": f"{hours} hour, {minutes} minutes"
    }

@app.route('/')
def index():
    """Main endpoint returning system info."""
    uptime = get_uptime()
    
    return jsonify({
        "service": {
            "name": "devops-info-service",
            "version": "1.0.0",
            "description": "DevOps course info service",
            "framework": "Flask"
        },
        "system": {
            "hostname": socket.gethostname(),
            "platform": platform.system(),
            "platform_version": platform.version(),
            "architecture": platform.machine(),
            "cpu_count": os.cpu_count(),
            "python_version": platform.python_version()
        },
        "runtime": {
            "uptime_seconds": uptime["uptime_seconds"],
            "uptime_human": uptime["uptime_human"],
            "current_time": datetime.now(timezone.utc).isoformat(),
            "timezone": "UTC"
        },
        "request": {
            "client_ip": request.remote_addr,
            "user_agent": request.headers.get('User-Agent'),
            "method": request.method,
            "path": request.path
        },
        "endpoints": [
            {"path": "/", "method": "GET", "description": "Service information"},
            {"path": "/health", "method": "GET", "description": "Health check"}
        ]
    })

@app.route('/health')
def health():
    """Health check endpoint for K8s probes."""
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "uptime_seconds": int(time.time() - start_time)
    })

if __name__ == '__main__':
    logger.info(f"Starting application on {HOST}:{PORT}")
    app.run(host=HOST, port=PORT)
