from db import db


class Ticket(db.Model):
    __tablename__ = 'tickets'

    ticket_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey(
        'users.user_id'), nullable=False)
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
    def get_all_tickets():
        return Ticket.query.all()

    @staticmethod
    def get_ticket_by_id(ticket_id):
        return Ticket.query.get(ticket_id)

    @staticmethod
    def get_tickets_by_assigned_role(assigned_role):
        return Ticket.query.filter_by(assigned_role=assigned_role).all()

    @staticmethod
    def create_ticket(title, user_id, description, priority, category, sla_due_at):
        new_ticket = Ticket(title=title, user_id=user_id, description=description, status='open', priority=priority,
                            category=category, assigned_role='none', sla_due_at=sla_due_at)
        try:
            db.session.add(new_ticket)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e
            return None
        return new_ticket

    @staticmethod
    def update_ticket(ticket_id, user_id, title=None, description=None, status=None, priority=None, category=None, assigned_role=None, sla_due_at=None):
        ticket = Ticket.get_ticket_by_id(ticket_id)
        if not ticket:
            return None
        if ticket.user_id != user_id:
            return None
        if title is not None:
            ticket.title = title
        if description is not None:
            ticket.description = description
        if status is not None:
            ticket.status = status
        if priority is not None:
            ticket.priority = priority
        if category is not None:
            ticket.category = category
        if assigned_role is not None:
            ticket.assigned_role = assigned_role
        if sla_due_at is not None:
            ticket.sla_due_at = sla_due_at

        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e
        return ticket

    @staticmethod
    def admin_update_ticket(ticket_id, status=None, priority=None, category=None, assigned_role=None):
        ticket = Ticket.get_ticket_by_id(ticket_id)
        if not ticket:
            return None
        if status is not None:
            ticket.status = status
        if priority is not None:
            ticket.priority = priority
        if category is not None:
            ticket.category = category
        if assigned_role is not None:
            ticket.assigned_role = assigned_role

        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e
        return ticket

    @staticmethod
    def get_tickets_by_user_id(user_id):
        return Ticket.query.filter_by(user_id=user_id).all()

    def to_dict(self):
        return {
            'ticket_id': self.ticket_id,
            'user_id': self.user_id,
            'title': self.title,
            'description': self.description,
            'status': self.status,
            'priority': self.priority,
            'category': self.category,
            'assigned_role': self.assigned_role,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'sla_due_at': self.sla_due_at.isoformat() if self.sla_due_at else None
        }
