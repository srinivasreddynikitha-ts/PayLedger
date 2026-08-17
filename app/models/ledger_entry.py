from datetime import datetime, timezone

from app import db


class LedgerEntry(db.Model):
    __tablename__ = "ledger_entries"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    transaction_id = db.Column(
        db.Integer,
        db.ForeignKey("transactions.id"),
        nullable=False
    )

    wallet_id = db.Column(
        db.Integer,
        db.ForeignKey("wallets.id"),
        nullable=True
    )

    account_type = db.Column(
        db.String(20),
        nullable=False,
        default="WALLET"
    )

    entry_type = db.Column(
        db.String(10),
        nullable=False
    )

    amount = db.Column(
        db.Numeric(15, 2),
        nullable=False
    )

    created_at = db.Column(
        db.DateTime,
        default=lambda: datetime.now(timezone.utc),
        nullable=False
    )