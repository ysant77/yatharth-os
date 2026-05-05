import json
from pathlib import Path
from typing import Any

from yatharth_os.core.config import DATA_DIR


class DataLoadError(RuntimeError):
    """Raised when static portfolio data cannot be loaded."""


def load_json(filename: str, data_dir: Path = DATA_DIR) -> Any:
    """Load a JSON file from the configured data directory."""
    path = data_dir / filename
    try:
        with path.open("r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError as exc:
        raise DataLoadError(f"Data file not found: {path}") from exc
    except json.JSONDecodeError as exc:
        raise DataLoadError(f"Invalid JSON in data file: {path}") from exc


def load_profile() -> dict[str, Any]:
    return load_json("profile.json")


def load_projects() -> list[dict[str, Any]]:
    return load_json("projects.json")


def load_experience() -> list[dict[str, Any]]:
    return load_json("experience.json")


def load_skills() -> dict[str, list[str]]:
    return load_json("skills.json")
