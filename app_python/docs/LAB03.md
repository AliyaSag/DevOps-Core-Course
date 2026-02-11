
# Lab 03 — Continuous Integration (CI/CD)

## 1. Overview

**Testing Framework:** pytest 8.1.1

**Why pytest?**
- Simple, Pythonic syntax with minimal boilerplate
- Powerful fixtures for Flask test client
- Detailed assertion error messages
- Industry standard for Python testing

**What endpoints are tested:**
- `GET /` — 6 tests (status, JSON structure, fields, data types, request info, User-Agents)
- `GET /health` — 5 tests (status, JSON, status="healthy", timestamp, uptime)
- `get_uptime()` — 2 tests (return structure, human-readable format)
- Error cases — 4 tests (404, 405, invalid methods, malformed URL)
- Configuration — 2 tests (environment variables, defaults)
- Data consistency — 2 tests (uptime across endpoints, UTC timezone)

**Total tests: 21**  
**Coverage: 93%**

**CI Workflow Trigger Configuration:**
```yaml
on:
  push:
    branches: [ main, master, develop, lab03 ]
    paths:
      - 'app_python/**'
      - '.github/workflows/**'
  pull_request:
    branches: [ main, master, develop ]
    paths:
      - 'app_python/**'
```

**Versioning Strategy:** Calendar Versioning (CalVer) — YYYY.MM.DD

**Why CalVer?**
I chose Calendar Versioning because my app has a stable API with no breaking changes. CalVer provides automatic version numbers from the build date without manual decisions about major/minor/patch. Users immediately know how recent the image is.

## 2. Workflow Evidence

### ✅ Successful GitHub Actions Run
Link: https://github.com/AliyaSag/DevOps-Core-Course/actions

### ✅ Tests Passing Locally
```text
PS C:\Users\neia_\Desktop\DevOps\DevOps-Core-Course\app_python> pytest tests/ --cov=app --cov-report=term
========================================================================== test session starts ==========================================================================
platform win32 -- Python 3.14.2, pytest-8.1.1, pluggy-1.6.0
collected 21 items                                                                                                                                                       

tests\test_app.py .....................                                                                                                                            [100%]

---------- coverage: platform win32, python 3.14.2-final-0 -----------
Name     Stmts   Miss  Cover
----------------------------
app.py      28      2    93%
----------------------------
TOTAL       28      2    93%

========================================================================== 21 passed in 0.33s ===========================================================================
```

### ✅ Docker Image on Docker Hub
Link: https://hub.docker.com/r/aliyasag/devops-info-service/tags
**Tags created:**
- `2026.02.11` — exact version
- `2026.02` — monthly track
- `latest` — most recent build
- `[commit-sha]` — for debugging

### ✅ Status Badge Working in README
https://github.com/AliyaSag/DevOps-Core-Course/actions/workflows/python-ci.yml/badge.svg?branch=lab03

## 3. Best Practices Implemented

**Practice 1: Dependency Caching**
Caches pip packages at `~/.cache/pip`. Cache key uses hash of requirements files. Reduces install time from 45s to 12s (73% faster).

**Practice 2: Job Dependencies (needs)**
Docker push only runs if tests and security scan pass. Prevents wasting resources on failed builds.

**Practice 3: Conditional Execution**
Docker images only pushed from lab03 branch. Prevents half-finished features from being published.

**Practice 4: Path-based Triggers**
CI doesn't run when only documentation changes. Saves ~80% unnecessary workflow runs.

**Caching Speed Improvement:**

| Run | Install Time | Total Workflow |
| :--- | :--- | :--- |
| First run (no cache) | 45s | 98s |
| Second run (cache hit) | 12s | 37s |
| **Improvement** | **73% faster** | **62% faster** |

**Snyk Security Results:**
- ✅ No vulnerabilities found
- Severity threshold: `high`
- Action: `continue-on-error: true` (warn only)
- Tested: Flask 3.1.0, python-dotenv 1.0.1

## 4. Key Decisions

**Versioning Strategy: CalVer**
I chose Calendar Versioning because my API is stable with no breaking changes. SemVer would require manual decisions about major/minor/patch versions. With CalVer, CI automatically generates versions from build date.

**Docker Tags:** `latest`, `YYYY.MM.DD`, `YYYY.MM`, `commit-sha`
Four tags give users choice: production can pin to monthly tags, development can use latest, debugging can use commit SHAs.

**Workflow Triggers: push + PR + path filters**
Push to main/lab03 runs full pipeline. PRs run tests only. Path filters prevent CI on documentation changes.

**Test Coverage: 93%**
Tested: all endpoints, JSON fields, status codes, edge cases. Not tested: `if __name__ == '__main__'` (low value), logging config (system concern). Threshold: 70%.

## 5. Challenges

- **HEAD method test** — Flask returns 200 for HEAD to GET endpoints. Removed HEAD from invalid methods test.
- **Python version** — Used Python 3.11 for compatibility.
- **Snyk token** — Generated token, added to GitHub Secrets.
- **Cache key** — Fixed hashFiles path to `'app_python/requirements*.txt'`.
- **Docker context** — Fixed with `context: ./app_python`.
```