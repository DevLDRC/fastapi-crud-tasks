from fastapi_crud_tasks.database import Base
from sqlalchemy import Column, Integer, String

class Item(Base):
   __tablename__ = "items"

   id = Column(Integer, primary_key=True, index=True)
   name = Column(String, index=True, nullable=False)
   description = Column(String, nullable=True)

class User(Base):
   __tablename__ = "users"

   id = Column(Integer, primary_key=True, index=True)
   name = Column(String, index=True, nullable=False)
   email = Column(String, index=True, nullable=False, unique=True)
   password = Column(String, nullable=False)