from akira.models import db
from datetime import datetime, timezone

class Decision(db.model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    time = db.Column(db.DateTime, default=datetime.now(timezone.utc), nullable=False)
    annotator_id = db.Column(db.Integer, db.ForeignKey('annotator.id'))
    annotator = db.relationship('Annotator', foreign_keys=[annotator_id], uselist=False)
    participant_id = db.Column(db.Integer, db.ForeignKey('participant.id'))
    participant = db.relationship('Participant', foreign_keys=[participant_id], uselist=False)
    assignment_id = db.Column(db.Integer, db.ForeignKey('assignment.id'))
    assignment = db.Column('Assignment', foreign_keys=[assignment_id], uselist=False)
    placement = db.Column(db.Integer, default=-1, nullable=False)

    def __init__(self, annotator, participant, assignment, placement):
        self.annotator = annotator
        self.participant = participant
        self.assignment = assignment
        self.placement = placement