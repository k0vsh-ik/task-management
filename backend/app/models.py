from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime
from app.database import Base
from app.constants import CENTRAL_EUROPE

class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String, default="")
    status = Column(String, nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(tz=CENTRAL_EUROPE))
