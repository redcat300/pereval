from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

class Coords(BaseModel):
    latitude: float
    longitude: float
    height: int

class Level(BaseModel):
    winter: Optional[str]
    summer: Optional[str]
    autumn: Optional[str]
    spring: Optional[str]

class User(BaseModel):
    fam: str
    name: str
    otc: str
    email: str
    phone: str

class Image(BaseModel):
    id: int
    title: str

class RawData(BaseModel):
    beauty_title: str
    title: str
    other_titles: str
    connect: str
    add_time: str
    coords: Coords
    level: Level
    user: User
    images: List[Image]

class PerevalCreate(BaseModel):
    date_added: datetime = Field(default_factory=datetime.now)
    raw_data: RawData
    images: List[Image]