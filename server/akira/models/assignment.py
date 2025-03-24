from akira import utils
from akira.models import Base, transactional
from sqlalchemy import ForeignKey, Column, Integer, String
from sqlalchemy.orm import relationship

class Assignment(Base):
    __tablename__ = 'assignment'

    id = Column(String(16), primary_key=True, nullable=False)
    wave = Column(Integer, default=-1, nullable=False)
    annotator_id = Column(Integer, ForeignKey('annotator.id'))
    annotator = relationship('Annotator', foreign_keys=[annotator_id], uselist=False)
    item_id = Column(Integer, ForeignKey('item.id'))
    item = relationship('Item', foreign_keys=[item_id], uselist=False)

    def __init__(self, wave, annotator_id, item_id):
        self.id = utils.generate_secret(16)
        self.wave = wave
        self.annotator_id = annotator_id
        self.item_id = item_id

    @classmethod
    @transactional
    def bulk_create(cls, session, assignments):
        new_assignments = []
        for wave in range(len(assignments)):
            for annotator in range(len(assignments[wave])):
                for item in assignments[wave][annotator]:
                    new_assignments.append(cls(wave, annotator + 1, item + 1))
        session.bulk_save_objects(new_assignments)
        session.commit()
        return new_assignments