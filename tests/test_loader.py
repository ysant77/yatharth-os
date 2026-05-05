from yatharth_os.core.loader import load_profile, load_projects, load_skills


def test_load_profile_returns_name() -> None:
    profile = load_profile()
    assert profile["name"] == "Yatharth Mahesh Sant"


def test_load_projects_returns_non_empty_list() -> None:
    projects = load_projects()
    assert len(projects) >= 1
    assert "name" in projects[0]


def test_load_skills_contains_backend_group() -> None:
    skills = load_skills()
    assert "backend" in skills
