from akira.models import Base
from sqlalchemy import Column, Integer, String, Boolean, DateTime
from datetime import datetime, timezone

class Annotator(Base):
    __tablename__ = 'annotator'

    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String(128), nullable=False)
    email = Column(String(128), nullable=False)
    secret = Column(String(32), nullable=False)
    updated = Column(DateTime, default=datetime.now(timezone.utc))
    active = Column(Boolean, default=True, nullable=False)

    def __init__(self, name, email):
        self.name = name
        self.email = email