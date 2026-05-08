"""
FastAPI routes for Yatharth OS.

The API exposes structured profile data from JSON files and provides export
functionality for generating a PDF profile.
"""

from __future__ import annotations

from fastapi import APIRouter
from fastapi.responses import Response

from yatharth_os.core.loader import (
    load_experience,
    load_profile,
    load_projects,
    load_skills,
)
from yatharth_os.exporters.pdf import build_profile_pdf_bytes

router = APIRouter()


@router.get("/health")
def health() -> dict[str, str]:
    """Health check endpoint used by local testing, CI, and Docker validation."""

    return {"status": "ok"}


@router.get("/profile")
def get_profile() -> dict:
    """Return structured profile information."""

    return load_profile()


@router.get("/skills")
def get_skills() -> dict:
    """Return skills grouped by category."""

    return load_skills()


@router.get("/projects")
def get_projects(tag: str | None = None) -> list[dict]:
    """Return projects, optionally filtered by tag."""

    projects = load_projects()

    if tag is None:
        return projects

    normalized_tag = tag.strip().lower()

    return [
        project
        for project in projects
        if normalized_tag in [item.lower() for item in project.get("tags", [])]
    ]


@router.get("/experience")
def get_experience() -> list[dict]:
    """Return professional experience entries."""

    return load_experience()


@router.get("/export/profile.pdf")
def export_profile_pdf() -> Response:
    """Export the portfolio profile as a PDF file."""

    pdf_bytes = build_profile_pdf_bytes()

    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={"Content-Disposition": 'attachment; filename="yatharth-profile.pdf"'},
    )
