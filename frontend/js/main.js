fetch("http://localhost:5000/")
    .then(res => res.json())
    .then(data => {
        document.getElementById("status").textContent = "Backend status: " + data.status;
    })
    .catch(() => {
        document.getElementById("status").textContent = "Backend not reachable";
    });
