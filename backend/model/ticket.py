from db import db


class Ticket(db.Model):
    __tablename__ = 'tickets'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
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

    @staticmethod
    def get_task():
        pass

    @staticmethod
    def get_ticket_by_id(ticket_id):
        pass

    @staticmethod
    def get_tickets_by_status(status):
        pass

    @staticmethod
    def get_tickets_by_priority(priority):
        pass

    @staticmethod
    def get_tickets_by_category(category):
        pass

    @staticmethod
    def get_tickets_by_assigned_role(assigned_role):
        pass

    @staticmethod
    def get_tickets_by_sla_due_date(sla_due_at):
        pass

    @staticmethod
    def get_tickets_by_created_at(created_at):
        pass

    @staticmethod
    def create_ticket(title, description, status, priority, category, assigned_role, sla_due_at):
        pass

    @staticmethod
    def update_ticket(ticket_id, title=None, description=None, status=None, priority=None, category=None, assigned_role=None, sla_due_at=None):
        pass

    @staticmethod
    def delete_ticket(ticket_id):
        pass

    @staticmethod
    def get_tickets_by_user_id(user_id):
        pass
