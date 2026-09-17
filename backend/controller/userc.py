from backend.model.user import User


class CreateUserController:
    def createUser(self, username, email, password_hash, role):
        return User.register_user(username, email, password_hash, role)


class LoginUserController:
    def loginUser(self, username, password_hash):
        return User.login_user(username, password_hash)


class FilterUserByRoleController:
    def filterUserByRole(self, role):
        return User.filter_user_by_role(role)
