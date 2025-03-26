from akira import utils
from akira.models import Base, transactional
from sqlalchemy import ForeignKey, Column, Integer, String, func
from sqlalchemy.orm import relationship

class Assignment(Base):
    __tablename__ = 'assignment'

    id = Column(Integer, primary_key=True, nullable=False)
    wave = Column(Integer, default=-1, nullable=False)
    annotator_id = Column(Integer, ForeignKey('annotator.id'))
    annotator = relationship('Annotator', foreign_keys=[annotator_id], uselist=False)
    item_id = Column(Integer, ForeignKey('item.id'))
    item = relationship('Item', foreign_keys=[item_id], uselist=False)

    def __init__(self, wave, annotator_id, item_id):
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

    @classmethod
    @transactional
    def dump(cls, session):
        assignments = session.query(cls).all()
        return assignments
    
    @classmethod
    @transactional
    def by_secret(cls, session, secret):
        from akira.models import WaveState, Annotator
        wave_state = WaveState.get_current_wave(session)
        a_id = Annotator.to_id(session, secret)
        if wave_state is None:
            raise Exception('Wave has not been initialized')
        return session.query(cls).filter(cls.annotator_id == a_id, cls.wave == wave_state.current_wave).all()
    
    @classmethod
    @transactional
    def max_wave(cls, session):
        return session.query(func.max(cls.wave)).scalar()