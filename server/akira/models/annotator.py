from akira.models import Base, transactional
from akira import utils
from sqlalchemy import Column, Integer, String, Boolean, DateTime
from datetime import datetime, timezone

class Annotator(Base):
    __tablename__ = 'annotator'

    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String(128), nullable=False)
    email = Column(String(128), nullable=False)
    secret = Column(String(32), unique=True, nullable=False)
    updated = Column(DateTime, default=datetime.now(timezone.utc))
    active = Column(Boolean, default=True, nullable=False)

    def __init__(self, name, email):
        self.name = name
        self.email = email
        self.secret = utils.generate_secret(32)

    @classmethod
    @transactional
    def create(cls, session, name, email):
        annotator = cls(name=name, email=email)
        session.add(annotator)
        session.commit()
        return annotator
    
    @classmethod
    @transactional
    def bulk_create(cls, session, annotator_list):
        '''
        annotator_list = [
            {
                'name':'example',
                'email':'example@example.com'
            },
            ...
        ]
        '''
        annotators = [cls(**item) for item in annotator_list]
        session.bulk_save_objects(annotators)
        session.commit()
        return annotators
    
    @classmethod
    @transactional
    def by_secret(cls, session, _secret):
        annotator = session.query(Annotator).filter_by(secret=_secret).first()
        return annotator