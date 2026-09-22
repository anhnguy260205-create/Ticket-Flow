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

const STAFF_LIST = ["Jordan Lee", "Priya Nair", "Sam Ortiz", "Dana Cole"];

let tickets = [
    { id: "TF-2041", subject: "Invoice #4821 charged twice", customer: "Alex Rivera", category: "Billing", priority: "High", status: "Resolved", assignee: "Priya Nair", date: "Sep 12" },
    { id: "TF-2042", subject: "Can't reset password after email change", customer: "Morgan Ito", category: "Account", priority: "Urgent", status: "In Progress", assignee: "Jordan Lee", date: "Sep 19" },
    { id: "TF-2043", subject: "Dashboard export button not responding", customer: "Casey Kim", category: "Technical", priority: "Medium", status: "Open", assignee: null, date: "Sep 21" },
    { id: "TF-2044", subject: "Seats not syncing with billing plan", customer: "Dana Whitfield", category: "Billing", priority: "High", status: "Open", assignee: "Sam Ortiz", date: "Sep 21" },
    { id: "TF-2045", subject: "Two-factor codes arriving late", customer: "Riley Chen", category: "Account", priority: "Medium", status: "In Progress", assignee: "Jordan Lee", date: "Sep 20" },
    { id: "TF-2046", subject: "Request: dark mode for reports page", customer: "Taylor Brooks", category: "Feature request", priority: "Low", status: "Open", assignee: null, date: "Sep 15" },
    { id: "TF-2047", subject: "Webhook retries failing silently", customer: "Noah Park", category: "Technical", priority: "Urgent", status: "In Progress", assignee: "Dana Cole", date: "Sep 22" },
    { id: "TF-2048", subject: "Refund not reflected in statement", customer: "Casey Kim", category: "Billing", priority: "Medium", status: "Open", assignee: null, date: "Sep 22" }
];

let openAllocateId = null;

function renderStats() {
    document.getElementById("stat-open").textContent =
        tickets.filter((t) => t.status === "Open").length;
    document.getElementById("stat-in-progress").textContent =
        tickets.filter((t) => t.status === "In Progress").length;
    document.getElementById("stat-resolved").textContent =
        tickets.filter((t) => t.status === "Resolved").length;
    document.getElementById("stat-unassigned").textContent =
        tickets.filter((t) => !t.assignee).length;
}

function onStatusChange(ticketId, newStatus) {
    tickets.find((t) => t.id === ticketId).status = newStatus;
    renderStats();
    renderTable();
}

function toggleAllocate(ticketId) {
    openAllocateId = openAllocateId === ticketId ? null : ticketId;
    renderTable();
}

function assign(ticketId, name) {
    tickets.find((t) => t.id === ticketId).assignee = name;
    openAllocateId = null;
    renderStats();
    renderTable();
}

function renderTable() {
    const tbody = document.getElementById("ticket-table-body");
    tbody.innerHTML = "";

    tickets.forEach((t) => {
        const statusColor = STATUS_COLORS[t.status];
        const priorityColor = PRIORITY_COLORS[t.priority];

        const row = document.createElement("tr");

        const subjectCell = document.createElement("td");
        subjectCell.innerHTML = `
            <span class="ticket-subject">${t.subject}</span><br>
            <span class="ticket-id">${t.id}</span>
        `;

        const customerCell = document.createElement("td");
        customerCell.style.color = "#4B4E57";
        customerCell.textContent = t.customer;

        const categoryCell = document.createElement("td");
        categoryCell.style.color = "#4B4E57";
        categoryCell.textContent = t.category;

        const priorityCell = document.createElement("td");
        priorityCell.innerHTML = `<span class="pill" style="background:${priorityColor.bg};color:${priorityColor.text};">${t.priority}</span>`;

        const statusCell = document.createElement("td");
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
        statusCell.appendChild(select);

        const assignCell = document.createElement("td");
        const wrap = document.createElement("div");
        wrap.className = "allocate-wrap";

        const allocateBtn = document.createElement("button");
        allocateBtn.className = "allocate-btn";
        allocateBtn.innerHTML = `
            ${t.assignee || "Allocate"}
            <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="#8A8D97" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round">
                <path d="M6 9l6 6 6-6"></path>
            </svg>
        `;
        allocateBtn.addEventListener("click", () => toggleAllocate(t.id));
        wrap.appendChild(allocateBtn);

        if (openAllocateId === t.id) {
            const menu = document.createElement("div");
            menu.className = "allocate-menu";
            STAFF_LIST.forEach((name) => {
                const option = document.createElement("button");
                option.className = "allocate-option";
                option.textContent = name;
                option.addEventListener("click", () => assign(t.id, name));
                menu.appendChild(option);
            });
            wrap.appendChild(menu);
        }
        assignCell.appendChild(wrap);

        const dateCell = document.createElement("td");
        dateCell.style.color = "#4B4E57";
        dateCell.textContent = t.date;

        row.appendChild(subjectCell);
        row.appendChild(customerCell);
        row.appendChild(categoryCell);
        row.appendChild(priorityCell);
        row.appendChild(statusCell);
        row.appendChild(assignCell);
        row.appendChild(dateCell);
        tbody.appendChild(row);
    });
}

renderStats();
renderTable();
