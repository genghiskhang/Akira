from akira.models import Base, transactional
from sqlalchemy import Column, Integer, Text, Boolean

class Item(Base):
    __tablename__ = 'item'

    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(Text, nullable=False)
    location = Column(Text, nullable=False)
    active = Column(Boolean, default=True, nullable=False)
    prioritized = Column(Boolean, default=False, nullable=False)

    def __init__(self, name, location):
        self.name = name
        self.location = location

    @classmethod
    @transactional
    def num_items(cls, session):
        return session.query(cls).count()
    
    @classmethod
    @transactional
    def bulk_create(cls, session, items_list):
        items = [cls(**item) for item in items_list]
        session.bulk_save_objects(items)
        session.commit()
        return items