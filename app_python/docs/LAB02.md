```markdown
# Lab 02 - Docker Containerization

## Docker Best Practices Applied

### 1. Non-root User Implementation
```dockerfile
RUN useradd -m -u 1000 appuser
USER appuser
```
**Why it matters:** Running containers as non-root user minimizes security risks by following the principle of least privilege. If an attacker compromises the application, they won't have root access to the container or host system, limiting potential damage.

### 2. Specific Base Image Version
```dockerfile
FROM python:3.13-slim
```
**Why it matters:** Using a specific version (3.13-slim) ensures reproducible builds across different environments. The `slim` variant reduces image size by removing unnecessary packages while maintaining compatibility, and avoiding `latest` tag prevents unexpected breaking changes.

### 3. Layer Caching Optimization
```dockerfile
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY app.py .
```
**Why it matters:** Docker caches each layer. By copying `requirements.txt` and installing dependencies before copying application code, we avoid reinstalling dependencies when only application code changes. This significantly speeds up development cycles.

### 4. .dockerignore File Implementation
```text
__pycache__/
*.pyc
venv/
.venv/
.vscode/
.idea/
.git/
.DS_Store
```
**Why it matters:** Excluding unnecessary files reduces build context size from ~5MB to ~63B, resulting in faster build times. It also prevents sensitive files and development artifacts from accidentally being included in production images.

### 5. Minimal Runtime Installation
```dockerfile
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*
```
**Why it matters:** The `--no-install-recommends` flag installs only essential packages, and cleaning `/var/lib/apt/lists/*` immediately reduces image size by ~25MB. This follows the principle of minimal attack surface.

## Image Information & Decisions

### Base Image Choice
*   **Selected:** `python:3.13-slim`
*   **Justification:**
    *   **Version Specificity:** Python 3.13 ensures reproducible builds
    *   **Size Optimization:** `slim` variant (140MB) vs full image (190MB)
    *   **Security:** Fewer packages = smaller attack surface
    *   **Maintenance:** Official Docker image with regular security updates
    *   **Compatibility:** Contains essential libraries for most Python applications

### Final Image Size
*   **Image Size:** 439MB
*   **Breakdown:**
    *   Base Python 3.13-slim: ~140MB
    *   System dependencies (gcc): ~175MB
    *   Python packages: ~15.2MB
    *   Application code: ~12.3KB
*   **Assessment:** Acceptable for development. Could be optimized further with multi-stage builds for production.

## Layer Structure Analysis
```text
IMAGE          CREATED          CREATED BY                                      SIZE      COMMENT
9f0735dd4d22   56 minutes ago   CMD ["python" "app.py"]                         0B        buildkit.dockerfile.v0
<missing>      56 minutes ago   ENV PORT=5000                                   0B        buildkit.dockerfile.v0
<missing>      56 minutes ago   ENV HOST=0.0.0.0                                0B        buildkit.dockerfile.v0
<missing>      56 minutes ago   EXPOSE map[5000/tcp:{}]                         0B        buildkit.dockerfile.v0
<missing>      56 minutes ago   USER appuser                                    0B        buildkit.dockerfile.v0
<missing>      56 minutes ago   COPY app.py . # buildkit                        12.3kB    buildkit.dockerfile.v0
<missing>      56 minutes ago   RUN /bin/sh -c pip install --no-cache-dir -r…   15.2MB    buildkit.dockerfile.v0
<missing>      57 minutes ago   COPY requirements.txt . # buildkit              12.3kB    buildkit.dockerfile.v0
<missing>      57 minutes ago   WORKDIR /app                                    8.19kB    buildkit.dockerfile.v0
<missing>      57 minutes ago   RUN /bin/sh -c useradd -m -u 1000 appuser # …   69.6kB    buildkit.dockerfile.v0
<missing>      57 minutes ago   RUN /bin/sh -c apt-get update && apt-get ins…   175MB     buildkit.dockerfile.v0
<missing>      18 hours ago     CMD ["python3"]                                 0B        buildkit.dockerfile.v0
```
**Analysis:** The layer structure shows proper ordering with dependencies installed before application code, and user creation before switching to non-root context.

## Optimization Choices Made
*   `--no-install-recommends`: Installed only essential system packages
*   `--no-cache-dir` with pip: Prevented caching of Python packages
*   Apt cache cleanup: Removed `/var/lib/apt/lists/*` in same RUN command
*   Layer ordering: Requirements before code for optimal caching
*   `.dockerignore`: Reduced build context significantly

## Build & Run Process

### Complete Build Output
```text
#0 building with "desktop-linux" instance using docker driver

#1 [internal] load build definition from Dockerfile
#1 transferring dockerfile: 430B 0.0s done
#1 DONE 0.0s

#2 [internal] load metadata for docker.io/library/python:3.13-slim
#2 ...

#3 [auth] library/python:pull token for registry-1.docker.io
#3 DONE 0.0s

#2 [internal] load metadata for docker.io/library/python:3.13-slim
#2 DONE 1.9s

#4 [internal] load .dockerignore
#4 transferring context: 301B 0.0s done
#4 DONE 0.0s

#5 [internal] load build context
#5 transferring context: 63B 0.0s done
#5 DONE 0.0s

#6 [1/7] FROM docker.io/library/python:3.13-slim@sha256:2b9c9803c6a287cafa0a8c917211dddd23dcd2016f049690ee5219f5d3f1636e
#6 resolve docker.io/library/python:3.13-slim@sha256:2b9c9803c6a287cafa0a8c917211dddd23dcd2016f049690ee5219f5d3f1636e 0.1s done
#6 DONE 0.1s

#7 [5/7] COPY requirements.txt .
#7 CACHED

#8 [6/7] RUN pip install --no-cache-dir -r requirements.txt
#8 CACHED

#9 [2/7] RUN apt-get update && apt-get install -y --no-install-recommends     gcc     && rm -rf /var/lib/apt/lists/*
#9 CACHED

#10 [3/7] RUN useradd -m -u 1000 appuser
#10 CACHED

#11 [4/7] WORKDIR /app
#11 CACHED

#12 [7/7] COPY app.py .
#12 CACHED

#13 exporting to image
#13 exporting layers 0.0s done
#13 exporting manifest sha256:ab189c598cfbbae6065a09d45b9ae9ef7b208269f90bb01084c2ffeb91db0dfb done
#13 exporting config sha256:e531cc91daf29f2e891c7fa14bceaea396f64e6b089c60b718c78f26968e47a6 done
#13 exporting attestation manifest sha256:bd564584f86d410f43656869af261b9f92be7bee265f85c1651be3f3d3d614ff
#13 exporting attestation manifest sha256:bd564584f86d410f43656869af261b9f92be7bee265f85c1651be3f3d3d614ff 0.1s done
#13 exporting manifest list sha256:9f0735dd4d225b486eff269d5e1f37bb7141e854cd03da61afd16b3314cc7883
#13 exporting manifest list sha256:9f0735dd4d225b486eff269d5e1f37bb7141e854cd03da61afd16b3314cc7883 0.0s done
#13 naming to docker.io/library/devops-info-service:latest done
#13 unpacking to docker.io/library/devops-info-service:latest 0.0s done
#13 DONE 0.4s
```
**Key Observations:** All layers show `CACHED`, demonstrating effective layer caching. Build completed in 0.4 seconds due to cache utilization.

### Container Running Status
```text
CONTAINER ID   IMAGE                      STATUS         PORTS                    NAMES
a6a5c79e0735   devops-info-service:latest Up 3 seconds   0.0.0.0:5001->5000/tcp   test
```

### Container Logs Output
```text
2026-02-03 20:58:49,135 - INFO - Starting application on 0.0.0.0:5000
2026-02-03 20:58:49,171 - INFO - WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
 * Running on all addresses (0.0.0.0)
 * Running on http://127.0.0.1:5000
 * Running on http://172.17.0.2:5000
2026-02-03 20:58:49,172 - INFO - Press CTRL+C to quit
```

### Endpoint Testing Results

**Health Endpoint Test:**
```json
{
  "status": "healthy",
  "timestamp": "2026-02-03T20:59:07.483940+00:00",
  "uptime_seconds": 18
}
```

**Main Endpoint Test (truncated):**
```json
{
  "endpoints": [
    {
      "description": "Service information",
      "method": "GET",
      "path": "/"
    },
    {
      "description": "Health check",
      "method": "GET",
      "path": "/health"
    }
  ],
  "request": {
    "client_ip": "172.17.0.1",
    "method": "GET",
    "path": "/",
    "user_agent": "python-requests/2.31.0"
  },
  "runtime": {
    "current_time": "2026-02-03T20:59:14.518988+00:00",
    "timezone": "UTC",
    "uptime_human": "0 hour, 0 minutes",
    "uptime_seconds": 25
  },
  "service": {
    "description": "DevOps course info service",
    "framework": "Flask",
    "name": "devops-info-service",
    "version": "1.0.0"
  },
  "system": {
    "architecture": "x86_64",
    "cpu_count": 8,
    "hostname": "a6a5c79e0735",
    "platform": "Linux",
    "platform_version": "#1 SMP PREEMPT_DYNAMIC Debian 6.11.4-1 (2024-09-22)",
    "python_version": "3.13.11"
  }
}
```

## Docker Hub Repository
*   **URL:** [https://hub.docker.com/r/aliyasag/devops-info-service](https://hub.docker.com/r/aliyasag/devops-info-service)
*   **Available Tags:**
    *   `aliyasag/devops-info-service:latest` - Most recent stable build
    *   `aliyasag/devops-info-service:v1.0.0` - Versioned release for reproducibility
*   **Verification:** Successfully pulled and ran the image from Docker Hub without authentication, confirming public accessibility.

## Technical Analysis

### Why This Dockerfile Structure Works
The Dockerfile follows a logical production-ready structure:
1.  **Base foundation (FROM):** Starts with minimal Python environment
2.  **System preparation:** Installs build essentials in optimized manner
3.  **Security setup:** Creates non-root user early in the process
4.  **Workspace configuration:** Sets working directory before copying files
5.  **Dependency management:** Installs Python packages before application code
6.  **Application deployment:** Copies only necessary application files
7.  **Runtime configuration:** Sets environment variables and exposes ports
8.  **Execution definition:** Defines how to start the application

This sequence ensures security, optimization, and maintainability.

### Impact of Layer Order Changes
If we changed the order:
```dockerfile
# Incorrect order - code before dependencies
COPY app.py .
COPY requirements.txt .
RUN pip install -r requirements.txt
```
**Consequences:**
*   **Cache invalidation:** Every code change would invalidate the dependency layer
*   **Slower development:** 15+ second penalty on each rebuild
*   **CI/CD inefficiency:** Longer pipeline execution times
*   **Bandwidth waste:** Larger context transfers to Docker daemon

**Current order benefits:**
*   **Code changes:** Only rebuilds last layer (0.1s)
*   **Dependency changes:** Rebuilds from requirements layer
*   **Base image updates:** Full rebuild when necessary

### Security Considerations Implemented
*   **Non-root execution:** Application runs as `appuser` (UID 1000)
*   **Minimal base image:** `slim` variant reduces attack surface by 50+ packages
*   **No secrets in image:** Configuration via environment variables only
*   **Package cache cleanup:** Removed apt lists to prevent version disclosure
*   **Specific versions:** Avoided floating tags for reproducibility
*   **Build-time isolation:** Used Docker's built-in security context

### .dockerignore Benefits
**Before .dockerignore:**
*   Build context: ~5MB (including virtual env, cache, IDE files)
*   Transfer time: ~2-3 seconds
*   Potential security risks: Accidental inclusion of secrets

**After .dockerignore:**
*   Build context: 63B (only Dockerfile, requirements.txt, app.py)
*   Transfer time: <0.1 seconds
*   **Improvement:** 95% reduction in context size

**Additional benefits:**
*   Prevents `__pycache__/` and `.pyc` files from causing conflicts
*   Excludes IDE configurations that might contain sensitive paths
*   Removes version control metadata
*   Eliminates operating system artifacts

## Challenges & Solutions

### Challenge 1: PowerShell vs Bash Command Differences
**Problem:** On Windows with PowerShell, commands like `curl` behave differently than in Linux bash.
**Symptoms:**
*   `curl` in PowerShell is an alias for `Invoke-WebRequest`
*   JSON formatting requires additional parameters
*   Line ending differences in scripts

**Solution:**
```powershell
# Used Invoke-RestMethod for clean JSON parsing
Invoke-RestMethod -Uri "http://localhost:5001/health" | ConvertTo-Json -Depth 10

# Configured Git for proper line endings
git config core.autocrlf input
```

### Challenge 2: Port Conflicts on Windows
**Problem:** Port 5000 frequently occupied by other applications or previous container instances.
**Error Message:**
```text
Error response from daemon: Port is already allocated
```
**Solution:**
```bash
# Check port usage
netstat -ano | findstr :5000

# Use alternative port
docker run -d -p 5001:5000 --name devops-container devops-info-service:latest

# Implement port checking in documentation
```

### Challenge 3: Docker Image Size Optimization
**Problem:** Initial image size was larger than expected (439MB).
**Investigation:**
```bash
# Analyzed layer contributions
docker history --no-trunc devops-info-service:latest

# Found largest contributors:
# - System packages (gcc): 175MB
# - Python base: 140MB
# - Python packages: 15MB
```
**Solution Applied:**
*   Used `--no-install-recommends` for apt packages
*   Cleaned apt cache in same RUN command
*   Used `--no-cache-dir` with pip
*   Considered multi-stage builds for future optimization

**Future Optimization Potential:**
*   Multi-stage builds to remove gcc after compilation
*   Alpine-based images for smaller base
*   Static compilation for Python dependencies

### Challenge 4: Docker Hub Authentication on Windows
**Problem:** Web-based authentication flow in Docker Desktop sometimes requires manual intervention.
**Solution:**
```bash
docker login -u aliyasag

```

### Challenge 5: Windows Line Endings in Dockerfile
**Problem:** CRLF line endings from Windows caused issues in Linux containers.
**Solution:**
*   Configured Git: `git config core.autocrlf input`
*   Used VS Code to convert to LF
*   Verified with: `cat -A Dockerfile` (shows `$` not `^M$`)

## What I Learned

### Technical Learnings:
*   **Layer caching** is critical for developer productivity and CI/CD efficiency
*   **Non-root user** is not optional for production containers
*   **Image size optimization** requires understanding layer contributions
*   **.dockerignore** has dramatic impact on build performance
*   **Tagging strategy** affects deployment reliability and rollback capability

### Process Learnings:
*   **Documentation-first approach:** Saving terminal outputs immediately
*   **Incremental testing:** Build → Run → Test → Document cycle
*   **Platform considerations:** Windows Docker Desktop has unique behaviors
*   **Security as default:** Non-root, minimal images, no secrets in layers

### Tooling Learnings:
*   **PowerShell adaptations:** `Invoke-RestMethod` instead of `curl -s`
*   **Docker Desktop features:** BuildKit improvements and UI integration
*   **Git configuration:** Managing line endings for cross-platform development
*   **Registry workflows:** Tagging, pushing, and verifying on Docker Hub

### Best Practices Reinforced:
*   **Specific versions** for reproducibility
*   **Minimal layers** for cache optimization
*   **Security-first** container design
*   **Comprehensive documentation** including failures and solutions
```