from datetime import datetime, timezone

from app import db


class Transaction(db.Model):
    __tablename__ = "transactions"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    reference = db.Column(
        db.String(50),
        unique=True,
        nullable=False
    )

    transaction_type = db.Column(
        db.String(30),
        nullable=False
    )

    amount = db.Column(
        db.Numeric(15, 2),
        nullable=False
    )

    status = db.Column(
        db.String(20),
        nullable=False,
        default="COMPLETED"
    )

    initiated_by = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    remark = db.Column(
        db.String(255),
        nullable=True
    )

    idempotency_key = db.Column(
        db.String(100),
        unique=True,
        nullable=True
    )

    created_at = db.Column(
        db.DateTime,
        default=lambda: datetime.now(timezone.utc),
        nullable=False
    )