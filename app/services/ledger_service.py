from decimal import Decimal
from uuid import uuid4

from app import db
from app.models.transaction import Transaction
from app.models.ledger_entry import LedgerEntry


def _validate_amount(amount):
    try:
        amount = Decimal(str(amount))
    except Exception:
        raise ValueError("Invalid amount.")

    if amount <= Decimal("0.00"):
        raise ValueError("Amount must be greater than zero.")

    return amount


def _validate_wallet(wallet):
    if wallet is None:
        raise ValueError("Wallet not found.")

    if wallet.status != "ACTIVE":
        raise ValueError("Wallet is not active.")


def _validate_remark(remark):
    if not remark or not remark.strip():
        raise ValueError("Remark is required.")

    return remark.strip()


def admin_credit(wallet, amount, admin_user, remark):
    """
    Credit a member wallet.

    SYSTEM -> DEBIT
    WALLET -> CREDIT
    """

    amount = _validate_amount(amount)
    _validate_wallet(wallet)
    remark = _validate_remark(remark)

    transaction = Transaction(
        reference=f"TXN-{uuid4().hex[:12].upper()}",
        transaction_type="ADMIN_CREDIT",
        amount=amount,
        status="COMPLETED",
        initiated_by=admin_user.id,
        remark=remark
    )

    db.session.add(transaction)
    db.session.flush()

    db.session.add(
        LedgerEntry(
            transaction_id=transaction.id,
            wallet_id=None,
            account_type="SYSTEM",
            entry_type="DEBIT",
            amount=amount
        )
    )

    db.session.add(
        LedgerEntry(
            transaction_id=transaction.id,
            wallet_id=wallet.id,
            account_type="WALLET",
            entry_type="CREDIT",
            amount=amount
        )
    )

    wallet.balance += amount

    return transaction


def admin_debit(wallet, amount, admin_user, remark):
    """
    Debit a member wallet.

    WALLET -> DEBIT
    SYSTEM -> CREDIT
    """

    amount = _validate_amount(amount)
    _validate_wallet(wallet)
    remark = _validate_remark(remark)

    if wallet.balance < amount:
        raise ValueError("Insufficient wallet balance.")

    transaction = Transaction(
        reference=f"TXN-{uuid4().hex[:12].upper()}",
        transaction_type="ADMIN_DEBIT",
        amount=amount,
        status="COMPLETED",
        initiated_by=admin_user.id,
        remark=remark
    )

    db.session.add(transaction)
    db.session.flush()

    db.session.add(
        LedgerEntry(
            transaction_id=transaction.id,
            wallet_id=wallet.id,
            account_type="WALLET",
            entry_type="DEBIT",
            amount=amount
        )
    )

    db.session.add(
        LedgerEntry(
            transaction_id=transaction.id,
            wallet_id=None,
            account_type="SYSTEM",
            entry_type="CREDIT",
            amount=amount
        )
    )

    wallet.balance -= amount

    return transaction


def member_transfer(
    sender_wallet,
    receiver_wallet,
    amount,
    member_user,
    remark
):
    """
    Transfer money from one member wallet to another.

    SENDER WALLET -> DEBIT
    RECEIVER WALLET -> CREDIT
    """

    amount = _validate_amount(amount)

    _validate_wallet(sender_wallet)
    _validate_wallet(receiver_wallet)

    remark = _validate_remark(remark)

    if sender_wallet.id == receiver_wallet.id:
        raise ValueError(
            "You cannot transfer money to your own wallet."
        )

    if sender_wallet.balance < amount:
        raise ValueError(
            "Insufficient wallet balance."
        )

    transaction = Transaction(
        reference=f"TXN-{uuid4().hex[:12].upper()}",
        transaction_type="MEMBER_TRANSFER",
        amount=amount,
        status="COMPLETED",
        initiated_by=member_user.id,
        remark=remark
    )

    db.session.add(transaction)
    db.session.flush()

    # Sender wallet -> DEBIT
    db.session.add(
        LedgerEntry(
            transaction_id=transaction.id,
            wallet_id=sender_wallet.id,
            account_type="WALLET",
            entry_type="DEBIT",
            amount=amount
        )
    )

    # Receiver wallet -> CREDIT
    db.session.add(
        LedgerEntry(
            transaction_id=transaction.id,
            wallet_id=receiver_wallet.id,
            account_type="WALLET",
            entry_type="CREDIT",
            amount=amount
        )
    )

    sender_wallet.balance -= amount
    receiver_wallet.balance += amount

    return transaction
