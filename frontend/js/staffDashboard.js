const STATUS_COLORS = {
    "Open": { bg: "#EAEEFB", text: "#3454D1" },
    "In Progress": { bg: "#FBEEDD", text: "#8A4B07" },
    "Resolved": { bg: "#E4F4EA", text: "#1B7A43" },
    "Closed": { bg: "#ECECE8", text: "#4B4E57" }
};

const PRIORITY_COLORS = {
    "Urgent": { bg: "#FBEAEA", text: "#B23131" },
    "High": { bg: "#FBEEDD", text: "#8A4B07" },
    "Medium": { bg: "#EAEEFB", text: "#3454D1" },
    "Low": { bg: "#ECECE8", text: "#4B4E57" }
};

let tickets = [
    {
        id: "TF-2042",
        subject: "Can't reset password after email change",
        description: "Customer updated their email in account settings and the reset link now bounces with an invalid-token error.",
        customer: "Morgan Ito",
        category: "Account",
        priority: "Urgent",
        status: "In Progress",
        date: "Sep 19"
    },
    {
        id: "TF-2045",
        subject: "Two-factor codes arriving late",
        description: "SMS codes are taking 3-4 minutes to arrive, well past the 5 minute expiry window during peak hours.",
        customer: "Riley Chen",
        category: "Account",
        priority: "Medium",
        status: "In Progress",
        date: "Sep 20"
    },
    {
        id: "TF-2050",
        subject: "Team member removed but still billed",
        description: "A seat was removed from the workspace on Sep 15 but still appears on the latest invoice.",
        customer: "Priya Shah",
        category: "Billing",
        priority: "High",
        status: "Open",
        date: "Sep 21"
    },
    {
        id: "TF-2036",
        subject: "CSV export missing custom fields",
        description: "Exported ticket reports leave out the two custom fields the team added last quarter.",
        customer: "Noah Park",
        category: "Technical",
        priority: "Low",
        status: "Resolved",
        date: "Sep 11"
    },
    {
        id: "TF-2028",
        subject: "Slack notifications duplicated",
        description: "Every status change posts to Slack twice since the integration was reconnected last week.",
        customer: "Taylor Brooks",
        category: "Technical",
        priority: "Medium",
        status: "Resolved",
        date: "Sep 9"
    }
];

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

renderStats();
renderTickets();
