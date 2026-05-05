from fastapi import APIRouter

from yatharth_os.core.loader import (
    load_experience,
    load_profile,
    load_projects,
    load_skills,
)
from yatharth_os.schemas.profile import Profile

router = APIRouter()


@router.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "ok"}


@router.get("/profile", response_model=Profile)
def get_profile() -> dict:
    return load_profile()


@router.get("/projects")
def get_projects() -> list[dict]:
    return load_projects()


@router.get("/experience")
def get_experience() -> list[dict]:
    return load_experience()


@router.get("/skills")
def get_skills() -> dict[str, list[str]]:
    return load_skills()
