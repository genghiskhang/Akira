from akira.models import db
from sqlalchemy.orm.exc import NoResultFound

view_table = db.Table('view',
    db.Column('participant_id', db.Integer, db.ForeignKey('participant.id')),
    db.Column('annotator_id', db.Integer, db.ForeignKey('annotator.id'))
)

class Participant(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.Text, nullable=False)
    location = db.Column(db.Text, nullable=False)
    description = db.Column(db.Text, nullable=False)
    active = db.Column(db.Boolean, default=True, nullable=False)
    viewed = db.relationship('Annotator', secondary=view_table)
    prioritized = db.Column(db.Boolean, default=False, nullable=False)

    def __init__(self, name, location, description):
        self.name = name
        self.location = location
        self.description = description

    @classmethod
    def by_id(cls, pid):
        if id is None:
            return None
        try:
            item = cls.query.get(pid)
        except NoResultFound:
            item = None
        return item