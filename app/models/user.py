from datetime import datetime, timezone

from flask_login import UserMixin

from app import db


class User(UserMixin, db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(
        db.String(100),
        nullable=False
    )

    email = db.Column(
        db.String(120),
        unique=True,
        nullable=False
    )

    password_hash = db.Column(
        db.String(255),
        nullable=False
    )

    role = db.Column(
        db.String(20),
        nullable=False,
        default="MEMBER"
    )

    verification_status = db.Column(
        db.String(20),
        nullable=False,
        default="PENDING"
    )

    created_at = db.Column(
        db.DateTime,
        default=lambda: datetime.now(timezone.utc)
    )
    wallet = db.relationship(
        "Wallet",
        back_populates="user",
        uselist=False
    )