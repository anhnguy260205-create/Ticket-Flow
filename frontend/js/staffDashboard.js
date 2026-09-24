const STATUS_COLORS = {
    "Open": { bg: "#EAEEFB", text: "#3454D1" },
    "In Progress": { bg: "#FBEEDD", text: "#8A4B07" },
    "Resolved": { bg: "#E4F4EA", text: "#1B7A43" },
    "Closed": { bg: "#ECECE8", text: "#4B4E57" }
};

const PRIORITY_COLORS = {
    "Critical": { bg: "#FBEAEA", text: "#B23131" },
    "High": { bg: "#FBEEDD", text: "#8A4B07" },
    "Medium": { bg: "#EAEEFB", text: "#3454D1" },
    "Low": { bg: "#ECECE8", text: "#4B4E57" }
};

// backend enum values (model/ticket.py) <-> display labels used above
const STATUS_TO_DISPLAY = { open: "Open", in_progress: "In Progress", resolved: "Resolved", closed: "Closed" };
const STATUS_TO_BACKEND = { "Open": "open", "In Progress": "in_progress", "Resolved": "resolved", "Closed": "closed" };
const PRIORITY_TO_DISPLAY = { low: "Low", medium: "Medium", high: "High", critical: "Critical" };

let tickets = [];

function loadTickets() {
    const storedUser = JSON.parse(localStorage.getItem('ticketflow_user'));
    if (!storedUser) return;

    fetch(`http://localhost:5000/tickets/get-tickets-by-assigned-role?assigned_role=${encodeURIComponent(storedUser.username)}`)
        .then(response => response.json())
        .then(data => {
            tickets = (data.tickets || []).map((t) => ({
                ticketId: t.ticket_id,
                id: `TF-${t.ticket_id}`,
                subject: t.title,
                description: t.description,
                customer: t.customer || `User #${t.user_id}`,
                category: t.category,
                priority: PRIORITY_TO_DISPLAY[t.priority] || t.priority,
                status: STATUS_TO_DISPLAY[t.status] || t.status,
                date: t.created_at ? new Date(t.created_at).toLocaleDateString() : ""
            }));
            renderStats();
            renderTickets();
        })
        .catch(error => console.error('Error fetching tickets:', error));
}

function persistTicketUpdate(ticketId, body) {
    fetch(`http://localhost:5000/tickets/update-ticket/${ticketId}`, {
        method: "PATCH",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(body)
    })
        .then(response => response.json())
        .then(data => {
            if (data.error) console.error('Failed to update ticket:', data.error);
        })
        .catch(error => console.error('Error updating ticket:', error));
}

function renderStats() {
    document.getElementById("stat-total").textContent = tickets.length;
    document.getElementById("stat-in-progress").textContent =
        tickets.filter((t) => t.status === "In Progress").length;
    document.getElementById("stat-resolved").textContent =
        tickets.filter((t) => t.status === "Resolved").length;
}

function onStatusChange(ticketId, newStatus) {
    const ticket = tickets.find((t) => t.id === ticketId);
    ticket.status = newStatus;
    renderStats();
    renderTickets();
    persistTicketUpdate(ticket.ticketId, { status: STATUS_TO_BACKEND[newStatus] || newStatus });
}

function renderTickets() {
    const list = document.getElementById("ticket-list");
    list.innerHTML = "";

    tickets.forEach((t) => {
        const statusColor = STATUS_COLORS[t.status];
        const priorityColor = PRIORITY_COLORS[t.priority];

        const card = document.createElement("div");
        card.className = "ticket-card";

        const info = document.createElement("div");
        info.className = "ticket-info";

        const headerRow = document.createElement("div");
        headerRow.className = "ticket-header-row";
        headerRow.innerHTML = `
            <span class="ticket-id">${t.id}</span>
            <span class="ticket-subject">${t.subject}</span>
        `;

        const desc = document.createElement("p");
        desc.className = "ticket-desc";
        desc.textContent = t.description;

        const metaRow = document.createElement("div");
        metaRow.className = "ticket-meta-row";
        metaRow.innerHTML = `
            <span class="ticket-meta-text">${t.customer}</span>
            <span class="ticket-meta-dot">·</span>
            <span class="ticket-meta-text">${t.category}</span>
            <span class="pill" style="background:${priorityColor.bg};color:${priorityColor.text};">${t.priority}</span>
            <span class="ticket-meta-dot">·</span>
            <span class="ticket-meta-text">Opened ${t.date}</span>
        `;

        info.appendChild(headerRow);
        info.appendChild(desc);
        info.appendChild(metaRow);

        const select = document.createElement("select");
        select.className = "status-select";
        select.style.backgroundColor = statusColor.bg;
        select.style.color = statusColor.text;
        ["Open", "In Progress", "Resolved", "Closed"].forEach((status) => {
            const option = document.createElement("option");
            option.value = status;
            option.textContent = status;
            if (status === t.status) option.selected = true;
            select.appendChild(option);
        });
        select.addEventListener("change", (e) => onStatusChange(t.id, e.target.value));

        card.appendChild(info);
        card.appendChild(select);
        list.appendChild(card);
    });
}

loadTickets();
