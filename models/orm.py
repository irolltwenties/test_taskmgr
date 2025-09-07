from datetime import datetime
from uuid import uuid4

from sqlalchemy import Column, String, Uuid, DateTime
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class TaskORM(Base):
    __tablename__ = "tasks"
    id = Column(Uuid, primary_key=True, index=True, default=uuid4)
    name = Column(String, nullable=False)
    text = Column(String, nullable=False)
    status = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)
    deleted_at = Column(DateTime, default=None, nullable=True)
