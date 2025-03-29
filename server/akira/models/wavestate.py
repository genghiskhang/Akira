from akira.models import Base, transactional
from sqlalchemy import Column, Integer
from akira.constants import NEXT, PREV

class WaveState(Base):
    __tablename__ = 'wave_state'

    id = Column(Integer, primary_key=True, nullable=False)
    current_wave = Column(Integer, default=-1, nullable=False)

    def __init__(self, current_wave=-1):
        self.current_wave = current_wave

    @classmethod
    @transactional
    def get_current_wave(cls, session):
        return session.query(cls).one_or_none()
    
    @classmethod
    @transactional
    def start(cls, session):
        wave = session.query(cls).one_or_none()
        if not wave:
            new_wave = cls(current_wave=0)
            session.add(new_wave)
            session.commit()
            return new_wave
        else:
            wave.current_wave = 0
            session.commit()
            return wave
    
    @classmethod
    @transactional
    def change_wave(cls, session, dir):
        from akira.models import Assignment
        cur_wave = session.query(cls).one_or_none()
        if dir == NEXT and cur_wave.current_wave == Assignment.max_wave(session):
            raise Exception('Maximum wave reached, can not increment...')
        if dir == PREV and cur_wave.current_wave == 0:
            raise Exception('Minimum wave reached, can not decrement...')
        cur_wave.current_wave += dir
        session.commit()
        return cur_wave.current_wave