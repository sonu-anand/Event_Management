from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from .database import Base

class Event(Base):
    __tablename__ = 'events'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    location = Column(String(250))
    start_time = Column(DateTime(timezone=True))
    end_time = Column(DateTime(timezone=True))
    max_capacity = Column(Integer)

class Register(Base):
    __tablename__ = 'register'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    email = Column(String(250), nullable=False)
    event_id = Column(Integer, ForeignKey('events.id'), nullable=False)

