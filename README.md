# Yatharth OS

[![CI](https://github.com/ysant77/yatharth-os/actions/workflows/ci.yml/badge.svg)](https://github.com/ysant77/yatharth-os/actions/workflows/ci.yml)
[![Docker Build](https://github.com/ysant77/yatharth-os/actions/workflows/docker.yml/badge.svg)](https://github.com/ysant77/yatharth-os/actions/workflows/docker.yml)

**Yatharth OS** is a CLI-first, API-backed engineering portfolio for **Yatharth Mahesh Sant**.

The goal is simple: build a real production-style Python project that can power a personal portfolio, expose structured profile data through FastAPI, and provide a developer-friendly terminal interface using Rich and Typer.

This repository is also a learning playground for professional engineering workflows: Poetry, Git/GitHub, pull requests, CI, Docker, testing, linting, and eventually deployment.

---

## Why this project exists

Most portfolio sites are static and shallow. This project treats a portfolio as an actual software system.

Instead of hardcoding everything in a frontend, the profile data lives in structured JSON files and is served through a backend API and CLI.

This gives us a clean foundation for:

- a real backend for an existing portfolio website
- a terminal-style developer portfolio
- structured project and experience data
- automated tests and CI checks
- future export features such as JSON, Markdown, or PDF
- future frontend integration using React, Next.js, or any other UI layer

---

## Core idea

```text
Frontend portfolio  <- calls -> FastAPI backend
CLI portfolio       <- calls -> same profile/data layer
Static JSON data    <- powers -> profile, projects, skills, experience
```

---

## Current features

- FastAPI backend
- Rich/Typer-based CLI foundation
- Static JSON-backed profile data
- Poetry-based Python project management
- Unit tests with Pytest
- API tests with FastAPI TestClient
- Coverage reporting with pytest-cov
- Formatting with Black
- Linting with Ruff
- GitHub Actions CI workflow
- Dockerfile for containerized API runtime

---

## Planned features

- Richer CLI interaction inspired by developer tools like Git, Docker, and modern AI coding CLIs
- Project search and filtering
- Resume/profile export as Markdown, JSON, and PDF
- Frontend integration with the current portfolio site
- Docker Compose setup
- Jenkins pipeline for enterprise CI practice
- Deployment pipeline

Example future commands:

```bash
yatharth whoami
yatharth skills
yatharth projects
yatharth projects --tag rag
yatharth experience
yatharth export resume --format json
yatharth serve
```

---

## Repository structure

```text
yatharth-os/
├── pyproject.toml
├── README.md
├── Dockerfile
├── data/
│   ├── profile.json
│   ├── projects.json
│   ├── experience.json
│   └── skills.json
├── src/
│   └── yatharth_os/
│       ├── __init__.py
│       ├── main.py
│       ├── api/
│       │   ├── app.py
│       │   └── routes.py
│       ├── cli/
│       │   └── app.py
│       ├── core/
│       │   ├── config.py
│       │   └── loader.py
│       └── schemas/
│           └── profile.py
├── tests/
│   ├── test_loader.py
│   ├── test_api.py
│   └── test_cli.py
└── .github/
    └── workflows/
        └── ci.yml
```

---

## Tech stack

| Area | Tool |
|---|---|
| Backend API | FastAPI |
| CLI | Typer + Rich |
| Data storage | JSON files |
| Project management | Poetry |
| Testing | Pytest |
| Coverage | pytest-cov |
| API testing | FastAPI TestClient |
| Formatting | Black |
| Linting | Ruff |
| CI | GitHub Actions |
| Containerization | Docker |

---

## Local development setup

This project uses **Poetry** for dependency management.

### 1. Install Poetry

Recommended installation:

```bash
pipx install poetry
```

Alternative installation:

```bash
pip install poetry
```

Verify installation:

```bash
poetry --version
```

---

### 2. Install project dependencies

For normal application usage:

```bash
poetry install
```

For local development, testing, linting, formatting, and coverage:

```bash
poetry install --with dev
```

This is important because development tools such as `pytest`, `pytest-cov`, `black`, and `ruff` are stored in the `dev` dependency group.

---

### 3. Activate the Poetry environment

You can run commands directly using `poetry run`:

```bash
poetry run pytest
```

Or activate the environment:

```bash
poetry shell
```

If `poetry shell` is unavailable in your Poetry version, use:

```bash
poetry env activate
```

---

## Common setup issue

### Pytest does not recognize `--cov`

If you see:

```text
pytest: error: unrecognized arguments: --cov=yatharth_os --cov-report=term-missing
```

it means `pytest-cov` is not installed in your active Poetry environment.

Fix it with:

```bash
poetry install --with dev
```

Then verify that coverage options are available:

```bash
poetry run pytest --help
```

You should see options such as:

```text
--cov
--cov-report
```

---

## Running checks locally

Run tests:

```bash
poetry run pytest
```

Run linting:

```bash
poetry run ruff check src tests
```

Check formatting:

```bash
poetry run black --check src tests
```

Auto-format code:

```bash
poetry run black src tests
```

Recommended full local check before pushing:

```bash
poetry run black src tests
poetry run ruff check src tests
poetry run pytest
```

---

## Running the API

```bash
poetry run uvicorn yatharth_os.api.app:app --reload
```

Open:

```text
http://localhost:8000/docs
```

Useful endpoints:

```text
GET /health
GET /profile
GET /projects
GET /projects?tag=rag
GET /experience
GET /skills
```

---

## CLI Usage

Yatharth OS includes a Rich/Typer-powered CLI that reads from the same structured
JSON data layer as the FastAPI backend.

Run commands through Poetry:

```bash
poetry run yatharth whoami
poetry run yatharth skills
poetry run yatharth projects
poetry run yatharth projects --tag rag
poetry run yatharth experience
poetry run yatharth version
```

### Available commands

| Command | Purpose |
|---|---|
| `yatharth whoami` | Display a concise profile card |
| `yatharth skills` | Show skills grouped by category |
| `yatharth projects` | Show all portfolio projects |
| `yatharth projects --tag <tag>` | Filter projects by tag |
| `yatharth experience` | Show professional experience |
| `yatharth version` | Show CLI version |
| `yatharth` | Show CLI help |

---

## Running with Docker

Build the image:

```bash
docker build -t yatharth-os .
```

Run the API:

```bash
docker run --rm -p 8000:8000 yatharth-os
```

Open:

```text
http://localhost:8000/docs
```

---

## Development workflow

This project should be developed using small feature branches and pull requests.

Recommended flow:

```bash
git checkout main
git pull origin main
git checkout -b feature/<short-feature-name>
# make changes
git add .
git commit -m "feat(scope): describe the change"
git push origin feature/<short-feature-name>
```

Then open a pull request into `main`.

---

## Commit message style

Use small, meaningful commits.

Recommended pattern:

```text
<type>(scope): <short message>
```

Examples:

```text
chore: bootstrap poetry project
feat(profile): add static profile loader
feat(api): expose profile endpoint
test(api): cover health and profile endpoints
ci: add GitHub Actions workflow
docs: clarify Poetry development setup
```

Common types:

| Type | Meaning |
|---|---|
| feat | New feature |
| fix | Bug fix |
| test | Tests added or updated |
| docs | Documentation only |
| refactor | Code change without behavior change |
| chore | Maintenance/setup work |
| ci | CI/CD workflow changes |
| style | Formatting-only change |

---

## Running with Docker

Yatharth OS can be packaged and run as a Docker container for reproducible local development and deployment workflows.

### Build the Docker image

```bash
docker build -t yatharth-os .
```

### Run the API container

```bash
docker run --rm -p 8000:8000 yatharth-os
```

The API will now be available at:

```text
http://localhost:8000/docs
```

---

## Running with Docker Compose

For local orchestration and easier container management:

```bash
docker compose up --build
```

Stop the service:

```bash
docker compose down
```

---

## Useful Docker validation commands

### Verify the health endpoint

```bash
curl http://localhost:8000/health
```

### Fetch profile data

```bash
curl http://localhost:8000/profile
```

### Fetch projects

```bash
curl http://localhost:8000/projects
```

---

## Why Docker is included

The Docker setup exists to ensure:

* reproducible backend environments
* dependency consistency across machines
* deployment-ready packaging
* CI/CD compatibility
* easier future cloud deployment

This also helps practise production-style backend engineering workflows commonly used in modern AI and platform engineering teams.

## Exporting Profile as PDF

Yatharth OS can export the JSON-backed portfolio data as a clean PDF profile.

The export feature is available through both the CLI and the FastAPI backend.

### CLI export

Generate a PDF in the current directory:

```bash
poetry run yatharth export-pdf
```

Generate a PDF at a custom path:

```bash
poetry run yatharth export-pdf --output exports/yatharth-profile.pdf
```

### API export

Run the API:

```bash
poetry run uvicorn yatharth_os.api.app:app --reload
```

Download the PDF from:

```text
http://localhost:8000/export/profile.pdf
```

You can also test it with curl:

```bash
curl -L -o yatharth-profile.pdf http://localhost:8000/export/profile.pdf
```

### Why this exists

The export feature turns the portfolio data layer into a reusable professional artifact.

Instead of manually maintaining separate resume, website, and CLI content, the project can generate a formatted profile directly from structured JSON data.

This keeps the system closer to a single source of truth.

## Authentication

Yatharth OS includes a simple JWT-based authentication flow for protected future features such as contact requests.

The current auth system supports:

- user registration
- user login
- JWT access tokens
- protected `/auth/me` route
- CLI token storage

### API auth flow

Start the API:

```bash
poetry run uvicorn yatharth_os.api.app:app --reload
```

Register:

```bash
curl -X POST http://localhost:8000/auth/register \
  -H "Content-Type: application/json" \
  -d "{\"email\":\"test@example.com\",\"full_name\":\"Test User\",\"password\":\"StrongPass123!\"}"
```

Login:

```bash
curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d "{\"email\":\"test@example.com\",\"password\":\"StrongPass123!\"}"
```

Use the returned access token:

```bash
curl http://localhost:8000/auth/me \
  -H "Authorization: Bearer <ACCESS_TOKEN>"
```

### CLI auth flow

Make sure the API is running first:

```bash
poetry run uvicorn yatharth_os.api.app:app --reload
```

Then use:

```bash
poetry run yatharth auth register
poetry run yatharth auth login
poetry run yatharth auth me
```

The CLI stores the access token locally at:

```text
~/.yatharth_os/token.json
```

### Token expiry

Access tokens expire after 30 minutes by default.

You can override this through an environment variable:

```bash
YATHARTH_OS_ACCESS_TOKEN_EXPIRE_MINUTES=60
```

### Production note

The default JWT secret is only for local development.

For deployment, set:

```bash
YATHARTH_OS_JWT_SECRET_KEY=<strong-random-secret>
```
## Request Logging and Request IDs

Yatharth OS uses structured JSON logging and request ID middleware for production-style debugging.

Every HTTP response includes an `X-Request-ID` header.

If the client provides an `X-Request-ID`, the application preserves it. Otherwise, the API generates one automatically.

### Example

Run the API:

```bash
poetry run uvicorn yatharth_os.api.app:app --reload
```

Call the health endpoint:

```bash
curl -i http://localhost:8000/health
```

You should see a response header similar to:

```text
X-Request-ID: 7d3fd0de-f9a4-43a3-b4a0-42be5b1d72f9
```

You can also provide your own request ID:

```bash
curl -i http://localhost:8000/health \
  -H "X-Request-ID: local-debug-123"
```

### Why this matters

Request IDs make it easier to trace a single request across:

- API logs
- authentication
- contact request creation
- background jobs
- email acknowledgement
- future observability systems

Structured JSON logs make application events easier to parse and ship to logging platforms.

## Contact Requests

Yatharth OS supports protected contact requests through the API and CLI.

This feature demonstrates a production-style POST workflow:

```text
POST -> validate -> authenticate -> persist -> trace -> respond
```

### API flow

Start the API:

```bash
poetry run uvicorn yatharth_os.api.app:app --reload
```

Register or login to get a JWT token.

Submit a contact request:

```bash
curl -X POST http://localhost:8000/contact-requests \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <ACCESS_TOKEN>" \
  -d "{
    \"name\": \"Jane Doe\",
    \"email\": \"jane@example.com\",
    \"company\": \"Example AI Labs\",
    \"purpose\": \"collaboration\",
    \"message\": \"I would like to discuss an applied AI collaboration.\",
    \"calendly_requested\": true
  }"
```

Check request status:

```bash
curl http://localhost:8000/contact-requests/<REQUEST_ID> \
  -H "Authorization: Bearer <ACCESS_TOKEN>"
```

### CLI flow

Make sure the API is running and you are logged in:

```bash
poetry run yatharth auth login
```

Submit a request:

```bash
poetry run yatharth contact submit
```

Check status:

```bash
poetry run yatharth contact status <REQUEST_ID>
```

### Validation

Contact request payloads are validated through Pydantic schemas.

Invalid requests return a structured validation error containing:

- error type
- message
- request ID
- validation details

### Request tracing

Every response includes:

```text
X-Request-ID
X-Correlation-ID
```

These IDs are designed for future observability workflows such as log aggregation, dashboards, and tracing.
