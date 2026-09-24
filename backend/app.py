import os
from unittest import result

from flask import Flask
from flask_cors import CORS
from werkzeug.security import generate_password_hash

from db import db
from model import ticket, user
from boundary.userb import user_bp
from controller.userc import CreateUserController, LoginUserController, FilterUserByRoleController

app = Flask(__name__)
CORS(app)
app.register_blueprint(user_bp, url_prefix="/users")

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


# seed admin account
NEW_USERNAME = "KIM"
NEW_EMAIL = "anhnguy.260205@gmail.com"
NEW_PASSWORD = "Limyuk.2005"
HASHED_PASSWORD = generate_password_hash(NEW_PASSWORD)
ROLE = 'admin'

with app.app_context():
    result = CreateUserController().createUser(
        NEW_USERNAME, NEW_EMAIL, HASHED_PASSWORD, ROLE)
    if result is None:
        print("User already exists — nothing created.")
    else:
        print(f"Created user: {result.username} ({result.email})")

# seed staff account
NEW_USERNAME_STAFF = "Jordan"
NEW_EMAIL_STAFF = "kimanh.work26@gmail.com"
NEW_PASSWORD_STAFF = "Limyuk.2005"
HASHED_PASSWORD_STAFF = generate_password_hash(NEW_PASSWORD_STAFF)
ROLE_STAFF = 'staff'
with app.app_context():
    result = CreateUserController().createUser(
        NEW_USERNAME_STAFF, NEW_EMAIL_STAFF, HASHED_PASSWORD_STAFF, ROLE_STAFF)
    if result is None:
        print("User already exists — nothing created.")
    else:
        print(f"Created user: {result.username} ({result.email})")

with app.app_context():
    result = CreateUserController().createUser(
        NEW_USERNAME_STAFF, NEW_EMAIL_STAFF, HASHED_PASSWORD_STAFF, ROLE_STAFF)
    if result is None:
        print("User already exists — nothing created.")
    else:
        print(f"Created user: {result.username} ({result.email})")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
