from sqlalchemy import Column, String, Float, BigInteger
from src.domain.model_base import Base

class City(Base):
    __tablename__ = "city"

    id = Column(BigInteger, primary_key=True, index=True)
    name = Column(String)
    state = Column(String)
    country = Column(String)
    latitude = Column(Float)
    longitude = Column(Float)