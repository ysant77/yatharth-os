from pydantic import BaseModel, HttpUrl


class ProfileLinks(BaseModel):
    linkedin: HttpUrl
    github: HttpUrl


class Profile(BaseModel):
    name: str
    headline: str
    location: str
    email: str
    links: ProfileLinks
    summary: str
