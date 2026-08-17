from decimal import Decimal

from app import db


class Wallet(db.Model):
    __tablename__ = "wallets"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    wallet_number = db.Column(
        db.String(20),
        unique=True,
        nullable=False
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        unique=True,
        nullable=False
    )

    user = db.relationship(
        "User",
        back_populates="wallet"
    )

    balance = db.Column(
        db.Numeric(15, 2),
        nullable=False,
        default=Decimal("0.00")
    )

    status = db.Column(
        db.String(20),
        nullable=False,
        default="ACTIVE"
    )