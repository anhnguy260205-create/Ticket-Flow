from flask import Flask
from flask_cors import CORS

from db import db, get_connection
from model import ticket, user

app = Flask(__name__)
CORS(app)

db.init_app(app)

with app.app_context():
    db.create_all()


@app.route("/")
def health():
    return {"status": "ok"}


@app.route("/tickets")
def list_tickets():
    tickets = ticket.Ticket.query.all()
    return {"tickets": [ticket.to_dict() for ticket in tickets]}


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
