// Client-side only: blocks the UI for anyone without a stored login,
// but does not protect any backend data (the backend doesn't check this).
(function () {
    const stored = localStorage.getItem('ticketflow_user') || sessionStorage.getItem('ticketflow_user');
    if (!stored) {
        window.location.href = '../Login.html';
    }
})();
