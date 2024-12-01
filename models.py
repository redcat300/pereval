from sqlalchemy import Column, Integer, String, Float, ForeignKey, Table
from sqlalchemy.orm import relationship
from pereval.database import Base

pereval_images = Table(
    'pereval_images', Base.metadata,
    Column('pereval_id', Integer, ForeignKey('pereval_added.id')),
    Column('image_id', Integer, ForeignKey('images.id'))
)


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    fam = Column(String)
    name = Column(String)
    otc = Column(String)
    phone = Column(String)
    passes = relationship("PerevalAdded", back_populates="user")


class Coords(Base):
    __tablename__ = 'coords'
    id = Column(Integer, primary_key=True, index=True)
    latitude = Column(Float)
    longitude = Column(Float)
    height = Column(Integer)


class Level(Base):
    __tablename__ = 'level'
    id = Column(Integer, primary_key=True, index=True)
    winter = Column(String)
    summer = Column(String)
    autumn = Column(String)
    spring = Column(String)


class Image(Base):
    __tablename__ = 'images'
    id = Column(Integer, primary_key=True, index=True)
    url = Column(String)
    title = Column(String)
    perevals = relationship("PerevalAdded", secondary=pereval_images, back_populates="images")


class PerevalAdded(Base):
    __tablename__ = 'pereval_added'
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    beauty_title = Column(String)
    title = Column(String)
    other_titles = Column(String)
    connect = Column(String)
    add_time = Column(String)
    coord_id = Column(Integer, ForeignKey('coords.id'))
    level_id = Column(Integer, ForeignKey('level.id'))
    status = Column(String, default="new")

    user = relationship("User", back_populates="passes")
    coords = relationship("Coords")
    level = relationship("Level")
    images = relationship("Image", secondary="pereval_images", back_populates="perevals")
