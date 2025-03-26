from akira.models import Base, transactional
from sqlalchemy import ForeignKey, Column, Integer, DateTime, String
from sqlalchemy.orm import relationship
from datetime import datetime, timezone

class Decision(Base):
    __tablename__ = 'decision'

    id = Column(Integer, primary_key=True, nullable=False)
    time = Column(DateTime, default=datetime.now(timezone.utc), nullable=False)
    placement = Column(Integer, default=-1, nullable=False)
    annotator_id = Column(String(32), ForeignKey('annotator.secret'))
    annotator = relationship('Annotator', foreign_keys=[annotator_id], uselist=False)
    item_id = Column(Integer, ForeignKey('item.id'))
    item = relationship('Item', foreign_keys=[item_id], uselist=False)
    assignment_id = Column(String(16), ForeignKey('assignment.id'))
    assignment = relationship('Assignment', foreign_keys=[assignment_id], uselist=False)

    def __init__(self, placement, item_id, annotator_id, assignment_id):
        self.placement = placement
        self.item_id = item_id
        self.annotator_id = annotator_id
        self.assignment_id = assignment_id

    @classmethod
    @transactional
    def vote(cls, session, annotator_id, decisions):
        '''
        decision_list = {
            "annotator_id": "secret",
            "decisions": [
                {
                    "item_id": 1,
                    "placement": 1,
                    "assignment_id": "id"
                },
                ...
            ]
        }
        '''
        new_decisions = [cls(decision['placement'], decision['item_id'], annotator_id, decision['assignment_id']) for decision in decisions]
        session.bulk_save_objects(new_decisions)
        session.commit()
        return new_decisions
    
    @classmethod
    @transactional
    def update_vote(cls, session):
        pass