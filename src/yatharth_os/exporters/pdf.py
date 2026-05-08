"""
PDF export utilities for Yatharth OS.

This module converts the JSON-backed portfolio data into a clean, readable PDF.
Both the FastAPI endpoint and CLI command should call this module so export logic
stays centralized and easy to test.

The implementation intentionally uses ReportLab because it is stable, lightweight,
and suitable for backend-side PDF generation without needing browser rendering.
"""

from __future__ import annotations

from io import BytesIO
from typing import Any

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

from yatharth_os.core.loader import (
    load_experience,
    load_profile,
    load_projects,
    load_skills,
)


def _safe_text(value: Any, fallback: str = "") -> str:
    """Convert any value into a safe printable string."""

    if value is None:
        return fallback
    return str(value)


def _section_title(title: str, styles: dict[str, ParagraphStyle]) -> Paragraph:
    """Create a consistently formatted section title."""

    return Paragraph(title, styles["SectionTitle"])


def _bullet_items(
    items: list[str], styles: dict[str, ParagraphStyle]
) -> list[Paragraph]:
    """Convert a list of strings into ReportLab bullet paragraphs."""

    return [Paragraph(f"• {_safe_text(item)}", styles["Body"]) for item in items]


def build_profile_pdf_bytes() -> bytes:
    """Build a PDF representation of the Yatharth OS profile.

    Returns:
        PDF content as bytes. This can be written to disk by the CLI or returned
        directly from a FastAPI response.
    """

    profile = load_profile()
    skills = load_skills()
    projects = load_projects()
    experience = load_experience()

    buffer = BytesIO()

    document = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=0.65 * inch,
        leftMargin=0.65 * inch,
        topMargin=0.55 * inch,
        bottomMargin=0.55 * inch,
        title="Yatharth Mahesh Sant Profile",
        author="Yatharth Mahesh Sant",
    )

    base_styles = getSampleStyleSheet()

    styles = {
        "Title": ParagraphStyle(
            "Title",
            parent=base_styles["Title"],
            fontSize=22,
            leading=28,
            spaceAfter=6,
            textColor=colors.HexColor("#111827"),
        ),
        "Subtitle": ParagraphStyle(
            "Subtitle",
            parent=base_styles["Normal"],
            fontSize=10,
            leading=14,
            textColor=colors.HexColor("#374151"),
            spaceAfter=10,
        ),
        "SectionTitle": ParagraphStyle(
            "SectionTitle",
            parent=base_styles["Heading2"],
            fontSize=13,
            leading=16,
            spaceBefore=10,
            spaceAfter=6,
            textColor=colors.HexColor("#0F766E"),
        ),
        "Body": ParagraphStyle(
            "Body",
            parent=base_styles["Normal"],
            fontSize=9,
            leading=12,
            textColor=colors.HexColor("#111827"),
            spaceAfter=3,
        ),
        "Small": ParagraphStyle(
            "Small",
            parent=base_styles["Normal"],
            fontSize=8,
            leading=10,
            textColor=colors.HexColor("#4B5563"),
        ),
    }

    story = []

    name = _safe_text(profile.get("name"), "Yatharth Mahesh Sant")
    title = _safe_text(profile.get("title"), "Applied AI Engineer")
    location = _safe_text(profile.get("location"), "Singapore")
    email = _safe_text(profile.get("email"), "ysant77@gmail.com")
    summary = _safe_text(profile.get("summary"))

    story.append(Paragraph(name, styles["Title"]))
    story.append(Paragraph(f"{title} | {location} | {email}", styles["Subtitle"]))

    if summary:
        story.append(_section_title("Professional Summary", styles))
        story.append(Paragraph(summary, styles["Body"]))

    story.append(_section_title("Core Skills", styles))
    skill_rows = [["Category", "Skills"]]
    for category, values in skills.items():
        skill_rows.append(
            [
                Paragraph(_safe_text(category), styles["Body"]),
                Paragraph(
                    ", ".join(_safe_text(item) for item in values), styles["Body"]
                ),
            ]
        )

    skill_table = Table(skill_rows, colWidths=[1.65 * inch, 5.0 * inch])
    skill_table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#E0F2FE")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.HexColor("#0F172A")),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("GRID", (0, 0), (-1, -1), 0.25, colors.HexColor("#CBD5E1")),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 6),
                ("RIGHTPADDING", (0, 0), (-1, -1), 6),
                ("TOPPADDING", (0, 0), (-1, -1), 5),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
            ]
        )
    )
    story.append(skill_table)

    story.append(_section_title("Professional Experience", styles))
    for item in experience:
        role = _safe_text(item.get("role"), "Role")
        organization = _safe_text(
            item.get("organization", item.get("company")), "Organization"
        )
        location = _safe_text(item.get("location"))
        start = _safe_text(item.get("start"))
        end = _safe_text(item.get("end"))
        duration = f"{start} - {end}".strip(" -")

        header_parts = [f"<b>{role}</b>", organization]
        if duration:
            header_parts.append(duration)
        if location:
            header_parts.append(location)

        story.append(Paragraph(" | ".join(header_parts), styles["Body"]))

        highlights = item.get("highlights", [])
        if isinstance(highlights, list):
            story.extend(_bullet_items([_safe_text(h) for h in highlights], styles))

        story.append(Spacer(1, 4))

    story.append(_section_title("Applied AI Projects", styles))
    for project in projects:
        project_name = _safe_text(project.get("name"), "Project")
        description = _safe_text(project.get("description"))
        tags = ", ".join(_safe_text(tag) for tag in project.get("tags", []))
        url = _safe_text(project.get("url"))

        story.append(Paragraph(f"<b>{project_name}</b>", styles["Body"]))
        if description:
            story.append(Paragraph(description, styles["Body"]))
        if tags:
            story.append(Paragraph(f"Tags: {tags}", styles["Small"]))
        if url:
            story.append(Paragraph(url, styles["Small"]))
        story.append(Spacer(1, 4))

    document.build(story)

    pdf_bytes = buffer.getvalue()
    buffer.close()

    return pdf_bytes
