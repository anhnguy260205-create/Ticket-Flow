from model.user import User


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


class ResetPasswordController:
    def resetPassword(self, email, new_password_hash):
        return User.reset_password(email, new_password_hash)
