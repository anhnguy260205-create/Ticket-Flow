from flask import Blueprint, request

from backend.controller.ticketc import CreateTicketController, UpdateTicketController, GetAllTicketsController, GetTicketByStatusController, GetTicketByPriorityController, GetTicketByCategoryController, GetTicketByAssignedRoleController, GetTicketBySlaDueDateController

ticket_bp = Blueprint("tickets", __name__)
