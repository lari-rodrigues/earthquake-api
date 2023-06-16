from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import MetaData

class Base:
    pass

Base = declarative_base(cls=Base, metadata=MetaData())
