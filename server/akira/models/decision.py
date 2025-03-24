from akira.models import Base
from sqlalchemy import ForeignKey, Column, Integer, DateTime, String
from sqlalchemy.orm import relationship
from datetime import datetime, timezone

class Decision(Base):
    __tablename__ = 'decision'

    id = Column(Integer, primary_key=True, nullable=False)
    time = Column(DateTime, default=datetime.now(timezone.utc), nullable=False)
    placement = Column(Integer, default=-1, nullable=False)
    annotator_id = Column(Integer, ForeignKey('annotator.id'))
    annotator = relationship('Annotator', foreign_keys=[annotator_id], uselist=False)
    item_id = Column(Integer, ForeignKey('item.id'))
    item = relationship('Item', foreign_keys=[item_id], uselist=False)
    assignment_id = Column(String, ForeignKey('assignment.id'))
    assignment = relationship('Assignment', foreign_keys=[assignment_id], uselist=False)

    def __init__(self, placement):
        self.placement = placement