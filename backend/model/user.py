from db import db


class User(db.Model):
    __tablename__ = 'users'

    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), nullable=False, unique=True)
    email = db.Column(db.String(255), nullable=False, unique=True)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.Enum('admin', 'user'), nullable=False, default='user')
    created_at = db.Column(db.DateTime, nullable=False,
                           default=db.func.current_timestamp())

    @staticmethod
    def get_user_by_id(user_id):
        return User.query.get(user_id)

    @staticmethod
    def get_user_by_username(username):
        return User.query.filter_by(username=username).first()

    @staticmethod
    def get_user_by_email(email) -> bool:
        return User.query.filter_by(email=email).first() is not None

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

    @staticmethod
    def login_user(username, password_hash):
        user = User.get_user_by_username(username)
        if user and user.password_hash == password_hash:
            return user
        return None

    def dict(self):
        return {
            'user_id': self.user_id,
            'username': self.username,
            'email': self.email,
            'role': self.role,
            'created_at': self.created_at.isoformat()
        }
