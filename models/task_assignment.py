from models import db
from datetime import datetime

class TaskAssignment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task_id = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, nullable=False)

    assigned_at = db.Column(db.DateTime, default=datetime.utcnow)
    deadline = db.Column(db.DateTime)