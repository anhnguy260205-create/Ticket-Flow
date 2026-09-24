from db import db
from werkzeug.security import check_password_hash


class User(db.Model):
    __tablename__ = 'users'

    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), nullable=False, unique=True)
    email = db.Column(db.String(255), nullable=False, unique=True)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.Enum('admin', 'user', 'staff'),
                     nullable=False, default='user')
    employee_code = db.Column(db.String(255), nullable=True)
    first_time_login = db.Column(db.Boolean, nullable=False, default=True)
    created_at = db.Column(db.DateTime, nullable=False,
                           default=db.func.current_timestamp())

    @staticmethod
    def get_user_by_id(user_id):
        return User.query.get(user_id)

    @staticmethod
    def get_user_by_username(username):
        return User.query.filter_by(username=username).first()

    @staticmethod
    def get_user_by_email(email):
        return User.query.filter_by(email=email).first()

    @staticmethod
    def filter_user_by_role(role):
        return User.query.filter_by(role=role).all()

    @staticmethod
    def register_user(username, email, password_hash, role):
        if User.get_user_by_username(username) or User.get_user_by_email(email):
            return None  # User already exists
        new_user = User(username=username, email=email,
                        password_hash=password_hash, role=role)
        db.session.add(new_user)
        db.session.commit()
        return new_user

    @staticmethod
    def login_user(email, password):
        user = User.get_user_by_email(email)
        if user and check_password_hash(user.password_hash, password):
            return user
        return None

    @staticmethod
    def get_user_infor():
        return User.query.all()

    @staticmethod
    def get_staffs_customers():
        return User.query.filter(User.role.in_(["staff", "user"])).all()

    def dict(self):
        return {
            'user_id': self.user_id,
            'username': self.username,
            'email': self.email,
            'role': self.role,
            'employee_code': self.employee_code,
            'created_at': self.created_at.isoformat()
        }

    @staticmethod
    def check_employee_code_exists(employee_code):
        return User.query.filter_by(employee_code=employee_code).first() is not None
