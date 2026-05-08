"""
Tests for PDF export generation.
"""

from yatharth_os.exporters.pdf import build_profile_pdf_bytes


def test_build_profile_pdf_bytes_returns_valid_pdf() -> None:
    """The PDF exporter should return valid PDF bytes."""

    pdf_bytes = build_profile_pdf_bytes()

    assert isinstance(pdf_bytes, bytes)
    assert pdf_bytes.startswith(b"%PDF")
    assert len(pdf_bytes) > 1000
