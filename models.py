from sqlalchemy import Column, Integer, String, Float,  JSON, TIMESTAMP
from database import Base

class Pass(Base):
    __tablename__ = 'passes'
    id = Column(Integer, primary_key=True, index=True)
    beauty_title = Column(String)
    title = Column(String)
    other_titles = Column(String)
    connect = Column(String)
    add_time = Column(String)
    latitude = Column(Float)
    longitude = Column(Float)
    height = Column(Integer)
    winter = Column(String)
    summer = Column(String)
    autumn = Column(String)
    spring = Column(String)
    user_fam = Column(String)
    user_name = Column(String)
    user_otc = Column(String)
    user_email = Column(String)
    user_phone = Column(String)

class PerevalAdded(Base):
    __tablename__ = "pereval_added"

    id = Column(Integer, primary_key=True, index=True)
    date_added = Column(TIMESTAMP)
    raw_data = Column(JSON)
    images = Column(JSON)
    status = Column(String, default="new")