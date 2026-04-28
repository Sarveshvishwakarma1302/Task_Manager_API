from models import db


class Task(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    # basic info
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)

    # status
    status = db.Column(db.String(20), default="pending")

    # priority (NEW - FIXED)
    priority = db.Column(
        db.String(20),
        default="low",
        nullable=False
    )

    # creator admin
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))