# Yatharth OS

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
Frontend portfolio  ← calls → FastAPI backend
CLI portfolio       ← calls → same profile/data layer
Static JSON data    ← powers → profile, projects, skills, experience
```

---

## Current features

- FastAPI backend
- Rich/Typer-based CLI
- Static JSON-backed profile data
- Poetry-based Python project management
- Unit tests with Pytest
- API tests with FastAPI TestClient
- GitHub Actions CI workflow
- Dockerfile for containerized API runtime

---

## Planned features

- Project search and filtering
- Resume/profile export as Markdown, JSON, and PDF
- Frontend integration with the current portfolio site
- Docker Compose setup
- Jenkins pipeline for enterprise CI practice
- Deployment pipeline
- Better CLI interaction inspired by developer tools like Git, Docker, and modern AI coding CLIs

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
| API testing | FastAPI TestClient |
| Formatting | Black |
| Linting | Ruff |
| CI | GitHub Actions |
| Containerization | Docker |

---

## Getting started

### 1. Clone the repository

```bash
git clone https://github.com/<your-username>/yatharth-os.git
cd yatharth-os
```

### 2. Install Poetry

```bash
pipx install poetry
```

Check installation:

```bash
poetry --version
```

### 3. Install dependencies

```bash
poetry install
```

### 4. Run tests

```bash
poetry run pytest
```

### 5. Run linting

```bash
poetry run ruff check src tests
```

### 6. Check formatting

```bash
poetry run black --check src tests
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
GET /experience
GET /skills
```

---

## Running the CLI

```bash
poetry run yatharth whoami
poetry run yatharth projects
poetry run yatharth projects --tag rag
poetry run yatharth skills
```

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
git checkout -b feature/project-bootstrap
# make changes
git add .
git commit -m "chore: bootstrap poetry project"
git push origin feature/project-bootstrap
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
docs: add setup instructions
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

---

## Learning goals

This repository is intentionally designed to help practise:

- modern Python project structure
- `pyproject.toml` and Poetry workflows
- clean Git commits
- feature branches and pull requests
- merge and rebase workflows
- API development with FastAPI
- CLI development with Rich and Typer
- unit and integration testing
- GitHub Actions CI
- Docker-based reproducibility

---

## Roadmap

| Phase | Goal | Status |
|---|---|---|
| Phase 0 | Bootstrap project with Poetry, FastAPI, CLI, tests | In progress |
| Phase 1 | Add richer profile/project data | Planned |
| Phase 2 | Improve CLI commands and UX | Planned |
| Phase 3 | Add CI checks and branch protection | Planned |
| Phase 4 | Add Docker Compose and deployment workflow | Planned |
| Phase 5 | Integrate with portfolio frontend | Planned |
| Phase 6 | Add export features | Planned |

---

## Philosophy

This project is not just a portfolio backend.

It is a statement of engineering maturity: clean structure, reproducible workflows, strong documentation, automated checks, and thoughtful user experience across API, CLI, and eventually UI.
