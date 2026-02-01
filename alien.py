from sqlalchemy import Column, Integer, String
from database import Base

class Alien(Base):
    __tablename__ = "aliens"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    power = Column(String, nullable=False)
