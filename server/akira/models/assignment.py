from akira.models import Base
from sqlalchemy import ForeignKey, Column, Integer
from sqlalchemy.orm import relationship
from datetime import datetime, timezone

class Assignment(Base):
    __tablename__ = 'assignment'

    id = Column(Integer, primary_key=True, nullable=False)
    wave = Column(Integer, default=-1, nullable=False)
    annotator_id = Column(Integer, ForeignKey('annotator.id'))
    annotator = relationship('Annotator', foreign_keys=[annotator_id], uselist=False)
    item_id = Column(Integer, ForeignKey('item.id'))
    item = relationship('Item', foreign_keys=[item_id], uselist=False)

    def __init__(self, wave):
        self.wave = wave