"""
Base ORM metadata definitions.

All SQLAlchemy ORM models should inherit from `Base`.
"""

from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    """Base declarative model for SQLAlchemy ORM."""

    pass
