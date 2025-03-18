from akira.models import db
from datetime import datetime, timezone

class Annotator(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(128), nullable=False)
    description = db.Column(db.Text, nullable=False)
    active = db.Column(db.Boolean, default=True, nullable=False)
    secret = db.Column(db.String(32), unique=True, nullable=False)
    updated = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    assignment_id = db.Column(db.Integer, db.ForeignKey('assignment.id'))
    assignment = db.relationship('Assignment', foreign_keys=[assignment_id], uselist=False)

    def __init__(self, name, email, description):
        self.name = name
        self.email = email
        self.description = description