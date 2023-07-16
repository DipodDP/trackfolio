# db models
from datetime import datetime

from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTableUUID
from sqlalchemy import (JSON, TIMESTAMP, Boolean, Column, ForeignKey, Integer,
                        String, Table)

from src.database import Base


# class Role(Base):
#     __tablename__ = "role"
#     id = Column(Integer, primary_key=True)
#     name = Column(String, nullable=False)
#     permissions = Column(String, nullable=False)


class User(SQLAlchemyBaseUserTableUUID, Base):
    __tablename__ = "user"
    username = Column(String, nullable=False)
    registered_at = Column(TIMESTAMP, default=datetime.utcnow)
