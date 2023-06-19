from sqlalchemy import Column, String, Float, BigInteger
from src.models.base_model import Base

class City(Base):
    __tablename__ = "city"

    id = Column(BigInteger, primary_key=True, index=True)
    name = Column(String(100))
    state = Column(String(100))
    country = Column(String(100))
    latitude = Column(Float)
    longitude = Column(Float)