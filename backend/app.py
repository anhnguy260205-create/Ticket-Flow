import os

from flask import Flask
from flask_cors import CORS

from db import db
from model import ticket, user

app = Flask(__name__)
CORS(app)

db_user = os.environ["DB_USER"]
db_password = os.environ["DB_PASSWORD"]
db_host = os.environ["DB_HOST"]
db_name = os.environ["DB_NAME"]
app.config["SQLALCHEMY_DATABASE_URI"] = (
    f"mysql+pymysql://{db_user}:{db_password}@{db_host}/{db_name}"
)

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
