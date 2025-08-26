from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from database import Base

# ------------------------------
# Task model
# ------------------------------
class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)  # Primary key
    title = Column(String, nullable=False)             # Task title
    description = Column(String, default="")          # Task description
    status = Column(String, nullable=False)           # Task status
    created_at = Column(DateTime, default=datetime.utcnow)  # Creation timestamp
