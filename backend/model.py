from db import db


class Ticket(db.Model):
    __tablename__ = 'tickets'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    status = db.Column(db.Enum('open', 'in_progress', 'resolved',
                       'closed'), nullable=False, default='open')
    priority = db.Column(db.Enum('low', 'medium', 'high',
                         'critical'), nullable=False, default='medium')
    category = db.Column(db.String(100))
    assigned_role = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, nullable=False,
                           default=db.func.current_timestamp())
    sla_due_at = db.Column(db.DateTime)
