from fastapi_crud_tasks.database import Base
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship


class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, index=True, nullable=False)
    name = Column(String, index=True, nullable=False)
    email = Column(String, index=True, nullable=False, unique=True)
    password = Column(String, nullable=False)

    itens = relationship("Item", back_populates="user")


class Item(Base):
    __tablename__ = "items"

    id = Column(String, primary_key=True, index=True, nullable=False)
    name = Column(String, index=True, nullable=False)
    description = Column(String, nullable=True)

    user_id = Column(ForeignKey("users.id"), nullable=False)
    user = relationship("User", back_populates="itens")
