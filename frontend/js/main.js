fetch("http://ticketflow-env.eba-gamu7nvf.ap-southeast-1.elasticbeanstalk.com/")
    .then(res => res.json())
    .then(data => {
        document.getElementById("status").textContent = "Backend status: " + data.status;
    })
    .catch(() => {
        document.getElementById("status").textContent = "Backend not reachable";
    });
