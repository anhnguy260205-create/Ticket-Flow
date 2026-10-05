from model.user import User
from model.password_reset import PasswordReset
from utils.mailer import send_reset_code_email


def mask_username(username):
    if len(username) <= 2:
        return username[0] + "*" * (len(username) - 1)
    return username[0] + "*" * (len(username) - 2) + username[-1]


class CreateUserController:
    def createUser(self, username, email, password_hash, role):
        return User.register_user(username, email, password_hash, role)


class LoginUserController:
    def loginUser(self, email, password):
        return User.login_user(email, password)


class GetUserInformationController:
    def getUserInformation(self):
        return User.get_user_infor()


class GetStaffCustomerController:
    def getStaffCustomer(self):
        return User.get_staffs_customers()


class GetUserInforByEmailController:
    def getUserInforByEmail(self, email):
        return User.get_user_by_email(email)


class RequestPasswordResetController:
    def requestReset(self, email):
        user = User.get_user_by_email(email)
        if not user:
            return None
        code = PasswordReset.create_reset_code(email)
        send_reset_code_email(email, code)
        return mask_username(user.username)


class VerifyResetCodeController:
    def verifyResetCode(self, email, code):
        return PasswordReset.verify_reset_code(email, code)


class ResetPasswordController:
    def resetPassword(self, email, code, new_password_hash):
        record = PasswordReset.verify_reset_code(email, code)
        if not record:
            return False
        success = User.reset_password(email, new_password_hash)
        if success:
            PasswordReset.mark_used(record)
        return success
