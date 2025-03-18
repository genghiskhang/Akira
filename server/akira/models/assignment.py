from akira.models import db
from datetime import datetime, timezone

class Assignment(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    time = db.Column(db.DateTime, default=datetime.now(timezone.utc), nullable=False)
    annotator_id = db.Column(db.Integer, db.ForeignKey('annotator.id'))
    annotator = db.relationship('Annotator', foreign_keys=[annotator_id], uselist=False)
    participant_id = db.Column(db.Integer, db.ForeignKey('participant.id'))
    participant = db.relationship('Participant', foreign_keys=[participant_id], uselist=False)

    def __init__(self, annotator, participant):
        self.annotator = annotator
        self.participant = participant