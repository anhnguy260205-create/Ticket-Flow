from db import db


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), nullable=False, unique=True)
    email = db.Column(db.String(255), nullable=False, unique=True)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.Enum('admin', 'user'), nullable=False, default='user')
    created_at = db.Column(db.DateTime, nullable=False,
                           default=db.func.current_timestamp())

    @staticmethod
    def get_user_by_id(user_id):
        pass

    @staticmethod
    def get_user_by_username(username):
        pass

    @staticmethod
    def register_user(username, email, password_hash, role='user'):
        pass

    @staticmethod
    def login_user(username, password_hash):
        pass
