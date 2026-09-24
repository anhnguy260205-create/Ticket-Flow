from model.ticket import Ticket


class CreateTicketController:
    def createTicket(self, title, user_id, description, priority, category, sla_due_at):
        return Ticket.create_ticket(title, user_id, description, priority, category, sla_due_at)


class UpdateTicketController:
    def updateTicket(self, ticket_id, user_id, title=None, description=None, status=None, priority=None, category=None, assigned_role=None, sla_due_at=None):
        return Ticket.update_ticket(ticket_id, user_id, title, description, status, priority, category, assigned_role, sla_due_at)


class GetAllTicketsController:
    def getAllTickets(self):
        return Ticket.get_all_tickets()


class GetTicketByAssignedRoleController:
    def getTicketsByAssignedRole(self, assigned_role):
        return Ticket.get_tickets_by_assigned_role(assigned_role)


class GetTicketByUserIDController:
    def getTicketsByUserID(self, user_id):
        return Ticket.get_tickets_by_user_id(user_id)


class AdminUpdateTicketController:
    def adminUpdateTicket(self, ticket_id, status=None, priority=None, category=None, assigned_role=None):
        return Ticket.admin_update_ticket(ticket_id, status, priority, category, assigned_role)
