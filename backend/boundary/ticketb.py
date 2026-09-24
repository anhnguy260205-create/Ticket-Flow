from flask import Blueprint, request

from backend.controller.ticketc import CreateTicketController, UpdateTicketController, GetAllTicketsController, GetTicketByStatusController, GetTicketByPriorityController, GetTicketByCategoryController, GetTicketByAssignedRoleController, GetTicketBySlaDueDateController

ticket_bp = Blueprint("tickets", __name__)

@ticket_bp.route("/create-tickets", methods=["POST"])
def create_ticket():
    data = request.get_json(silent=True) or {}
    title = data.get("title")
    description = data.get("description")
    priority = data.get("priority")
    category = data.get("category")
    assigned_role = data.get("assigned_role")
    sla_due_date = data.get("sla_due_date")

    if not title or not description or not priority or not category or not assigned_role or not sla_due_date:
        return {"error": "All fields are required"}, 400

    ticket = CreateTicketController().createTicket(title, description, priority, category, assigned_role, sla_due_date)

    if ticket is None:
        return {"error": "Failed to create ticket"}, 500

    return {"message": "Ticket created successfully", "ticket": ticket.dict()}, 201