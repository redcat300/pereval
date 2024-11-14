from typing import List, Optional
from pydantic import BaseModel, Field, validator
from datetime import datetime

class Coords(BaseModel):
    latitude: float
    longitude: float
    height: int

    class Config:
        from_attributes = True


class Level(BaseModel):
    winter: Optional[str] = None
    summer: Optional[str] = None
    autumn: Optional[str] = None
    spring: Optional[str] = None

    class Config:
        from_attributes = True


class User(BaseModel):
    fam: str
    name: str
    otc: str
    email: str
    phone: str

    class Config:
        from_attributes = True

class Image(BaseModel):
    id: Optional[int] = None
    url: str
    title: str

    class Config:
        from_attributes = True

class PerevalCreate(BaseModel):
    beauty_title: str
    title: str
    other_titles: Optional[str] = None
    connect: Optional[str] = None
    add_time: datetime
    coords: Coords
    level: Level
    user: User
    images: List[Image] = []
    status: str = "new"

    class Config:
        from_attributes = True


class PerevalResponse(BaseModel):
    id: int
    beauty_title: str
    title: str
    other_titles: Optional[str] = None
    connect: Optional[str] = None
    add_time: datetime
    coords: Coords
    level: Level
    user: User
    images: List[Image]
    status: str

@validator("status")
def validate_status(cls, v):
    allowed_statuses = {"new", "pending", "accepted", "rejected"}
    if v not in allowed_statuses:
        raise ValueError("Invalid status value. Must be one of: new, pending, accepted, rejected")
    return v

class Config:
    from_attributes = True