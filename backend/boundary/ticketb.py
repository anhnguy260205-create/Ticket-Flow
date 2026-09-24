from flask import Blueprint, request

from controller.ticketc import CreateTicketController, UpdateTicketController, GetAllTicketsController, GetTicketByStatusController, GetTicketByPriorityController, GetTicketByCategoryController, GetTicketByAssignedRoleController, GetTicketBySlaDueDateController, GetTicketByUserIDController, AdminUpdateTicketController
from model.user import User

ticket_bp = Blueprint("tickets", __name__)


@ticket_bp.route("/create-tickets", methods=["POST"])
def create_ticket():
    data = request.get_json(silent=True) or {}
    user_id = data.get("user_id")
    title = data.get("title")
    description = data.get("description")
    priority = data.get("priority")
    category = data.get("category")
    sla_due_at = data.get("sla_due_at")

    if not user_id or not title or not description or not priority or not category or not sla_due_at:
        return {"error": "All fields are required"}, 400

    ticket = CreateTicketController().createTicket(
        title, user_id, description, priority, category, sla_due_at)

    if ticket is None:
        return {"error": "Failed to create ticket"}, 500

    return {"message": "Ticket created successfully", "ticket": ticket.to_dict()}, 201


@ticket_bp.route("/get-tickets", methods=["GET"])
def get_tickets():
    # get user_id from the url
    user_id = request.args.get("user_id")
    tickets = GetTicketByUserIDController().getTicketsByUserID(user_id)
    return {"tickets": [ticket.to_dict() for ticket in tickets]}, 200


@ticket_bp.route("/get-all-tickets", methods=["GET"])
def get_all_tickets():
    all_tickets = GetAllTicketsController().getAllTickets()
    result = []
    for t in all_tickets:
        d = t.to_dict()
        owner = User.get_user_by_id(t.user_id)
        d["customer"] = owner.username if owner else None
        result.append(d)
    return {"tickets": result}, 200


@ticket_bp.route("/get-tickets-by-assigned-role", methods=["GET"])
def get_tickets_by_assigned_role():
    assigned_role = request.args.get("assigned_role")
    tickets = GetTicketByAssignedRoleController().getTicketsByAssignedRole(assigned_role)
    result = []
    for t in tickets:
        d = t.to_dict()
        owner = User.get_user_by_id(t.user_id)
        d["customer"] = owner.username if owner else None
        result.append(d)
    return {"tickets": result}, 200


@ticket_bp.route("/update-ticket/<int:ticket_id>", methods=["PATCH"])
def update_ticket_status(ticket_id):
    data = request.get_json(silent=True) or {}
    status = data.get("status")
    priority = data.get("priority")
    category = data.get("category")
    assigned_role = data.get("assigned_role")

    ticket = AdminUpdateTicketController().adminUpdateTicket(
        ticket_id, status, priority, category, assigned_role)

    if ticket is None:
        return {"error": "Ticket not found"}, 404

    return {"message": "Ticket updated successfully", "ticket": ticket.to_dict()}, 200
