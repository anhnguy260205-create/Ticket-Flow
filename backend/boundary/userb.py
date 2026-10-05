from flask import Blueprint, request
from werkzeug.security import generate_password_hash

from controller.userc import (
    CreateUserController, GetStaffCustomerController, LoginUserController, GetUserInformationController,
    RequestPasswordResetController, VerifyResetCodeController, ResetPasswordController
)

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


@user_bp.route("/get_all_users", methods=['GET'])
def get_all_user():
    all_users = GetUserInformationController().getUserInformation()
    return {"message": "Get information successfully", "users": [u.dict() for u in all_users]}, 200


@user_bp.route("/get_staffs_customers", methods=['GET'])
def get_staffs_customers():
    all_users = GetStaffCustomerController().getStaffCustomer()
    return {"message": "Get information successfully", "users": [u.dict() for u in all_users]}, 200


@user_bp.route("/request_reset", methods=["POST"])
def request_reset():
    data = request.get_json(silent=True) or {}
    email = data.get("email")
    if not email:
        return {"error": "Email is required"}, 400

    masked_username = RequestPasswordResetController().requestReset(email)
    if masked_username is None:
        return {"error": "No account found with that email"}, 404

    return {"message": "Code sent", "masked_username": masked_username}, 200


@user_bp.route("/verify_reset_code", methods=["POST"])
def verify_reset_code():
    data = request.get_json(silent=True) or {}
    email = data.get("email")
    code = data.get("code")
    if not email or not code:
        return {"error": "Email and code are required"}, 400

    record = VerifyResetCodeController().verifyResetCode(email, code)
    if record is None:
        return {"error": "Invalid or expired code"}, 401

    return {"message": "Code verified"}, 200


@user_bp.route("/reset_password", methods=["POST"])
def reset_password():
    data = request.get_json(silent=True) or {}
    email = data.get("email")
    code = data.get("code")
    new_password = data.get("new_password")

    if not email or not code or not new_password:
        return {"error": "Email, code, and new password are required"}, 400

    new_password_hash = generate_password_hash(new_password)
    success = ResetPasswordController().resetPassword(email, code, new_password_hash)

    if not success:
        return {"error": "Invalid or expired code"}, 401

    return {"message": "Password reset successfully"}, 200
