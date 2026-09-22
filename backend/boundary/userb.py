from flask import Blueprint, request
from werkzeug.security import generate_password_hash

from controller.userc import CreateUserController, LoginUserController, FilterUserByRoleController

user_bp = Blueprint("users", __name__)


@user_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json(silent=True) or {}
    username = data.get("username")
    email = data.get("email")
    password = data.get("password")
    role = data.get("role", "user")

    if not username or not email or not password:
        return {"error": "username, email, and password are required"}, 400
    # Hash the password before storing it
    password_hash = generate_password_hash(password)
    user = CreateUserController().createUser(username, email, password_hash, role)

    if user is None:
        return {"error": "Username or email already exists"}, 409

    return {"message": "User registered successfully", "user": user.dict()}, 201


@user_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json(silent=True) or {}
    email = data.get("email")
    password = data.get("password")
    if not email or not password:
        return {"error": "Email and password are required"}, 400

    user = LoginUserController().loginUser(email, password)

    if user is None:
        return {"error": "Invalid email or password"}, 401

    return {"message": "Login successful", "user": user.dict()}, 200


@user_bp.route("/logout", methods=["POST"])
def Logout():
    # In a real application, you would handle session management or token invalidation here.
    return {"message": "Logout successful"}, 200
