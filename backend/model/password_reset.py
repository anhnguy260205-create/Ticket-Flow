
import hashlib
# generate a secure random code for password reset
import secrets
from datetime import datetime, timedelta

from db import db

CODE_TTL_MINUTES = 10  # Code is valid for 10 minutes


class PasswordReset(db.Model):
    __tablename__ = 'password_resets'
    reset_id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), nullable=False)
    code_hash = db.Column(db.String(255), nullable=False)
    expiration_time = db.Column(db.DateTime, nullable=False)
    used = db.Column(db.Boolean, nullable=False, default=False)
    created_at = db.Column(db.DateTime, nullable=False,
                           default=db.func.current_timestamp())

    # Static method to generate a secure random code
    @staticmethod
    def _hash(code):
        return hashlib.sha256(code.encode()).hexdigest()

    @staticmethod
    def create_reset_code(email):
        # invalidate any previous unused codes so only the newest one works
        PasswordReset.query.filter_by(email=email, used=False).update({"used": True})

        code = f"{secrets.randbelow(1000000):06d}"  # plaintext 6-digit code
        record = PasswordReset(
            email=email,
            code_hash=PasswordReset._hash(code),
            expiration_time=datetime.utcnow() + timedelta(minutes=CODE_TTL_MINUTES),
            used=False
        )
        db.session.add(record)
        db.session.commit()
        return code  # plaintext, only returned here so it can be emailed

    @staticmethod
    def verify_reset_code(email, code):
        record = PasswordReset.query.filter_by(
            email=email, code_hash=PasswordReset._hash(code), used=False).first()
        if not record:
            return None
        if record.expiration_time < datetime.utcnow():
            return None
        return record  # return the record itself so mark_used() can flip it

    @staticmethod
    def mark_used(record):
        record.used = True
        db.session.commit()
