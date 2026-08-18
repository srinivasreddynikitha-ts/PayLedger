from flask import (
    Blueprint,
    render_template,
    redirect,
    url_for,
    flash,
    request
)

from flask_login import login_required, current_user

from app import db
from app.models.wallet import Wallet
from app.models.ledger_entry import LedgerEntry
from app.models.transaction import Transaction
from app.models.user import User
from app.services.ledger_service import member_transfer
from app.auth.forms import TransferForm


main = Blueprint(
    "main",
    __name__,
    url_prefix="/",
    template_folder="templates",
    static_folder="static",
    static_url_path="/main-static"
)


@main.route("/")
def home():
    if current_user.is_authenticated:
        return redirect(url_for("main.dashboard"))

    return render_template("main/home.html")


# ============================================================
# VERIFIED USER CHECK
# ============================================================

def verified_user_required():

    if current_user.verification_status != "VERIFIED":

        flash(
            "Your account is not verified. Please contact the administrator.",
            "danger"
        )

        return redirect(url_for("auth.login"))

    return None


# ============================================================
# MEMBER DASHBOARD
# ============================================================

@main.route("/dashboard")
@login_required
def dashboard():

    check = verified_user_required()

    if check:
        return check

    return render_template(
        "main/dashboard.html"
    )


# ============================================================
# MEMBER WALLET
# ============================================================

@main.route("/wallet")
@login_required
def wallet():

    check = verified_user_required()

    if check:
        return check

    wallet = db.session.scalar(
        db.select(Wallet).where(
            Wallet.user_id == current_user.id
        )
    )

    if wallet is None:
        flash(
            "Wallet not available. Please contact the administrator.",
            "warning"
        )
        return redirect(url_for("main.dashboard"))

    return render_template(
        "main/wallet.html",
        wallet=wallet
    )


# ============================================================
# MEMBER TRANSACTIONS
# ============================================================

@main.route("/transactions")
@login_required
def transactions():

    check = verified_user_required()

    if check:
        return check

    wallet = db.session.scalar(
        db.select(Wallet).where(
            Wallet.user_id == current_user.id
        )
    )

    if wallet is None:
        flash(
            "Wallet not available. Please contact the administrator.",
            "warning"
        )
        return redirect(url_for("main.dashboard"))

    transaction_ids = db.session.scalars(
        db.select(LedgerEntry.transaction_id)
        .where(
            LedgerEntry.wallet_id == wallet.id
        )
        .distinct()
    ).all()

    transactions = db.session.scalars(
        db.select(Transaction)
        .where(
            Transaction.id.in_(transaction_ids)
        )
        .order_by(Transaction.created_at.desc())
    ).all()

    transaction_display = []

    for transaction in transactions:

        user_entry = db.session.scalar(
            db.select(LedgerEntry).where(
                LedgerEntry.transaction_id == transaction.id,
                LedgerEntry.wallet_id == wallet.id
            )
        )

        if transaction.transaction_type == "ADMIN_CREDIT":

            display_type = "Admin Credit"
            display_class = "credit"
            display_sign = "+"

        elif transaction.transaction_type == "ADMIN_DEBIT":

            display_type = "Admin Debit"
            display_class = "debit"
            display_sign = "-"

        elif transaction.transaction_type == "MEMBER_TRANSFER":

            if user_entry and user_entry.entry_type == "CREDIT":

                display_type = "Money Received"
                display_class = "credit"
                display_sign = "+"

            else:

                display_type = "Money Sent"
                display_class = "debit"
                display_sign = "-"

        else:

            display_type = transaction.transaction_type
            display_class = ""
            display_sign = ""

        transaction_display.append(
            {
                "transaction": transaction,
                "display_type": display_type,
                "display_class": display_class,
                "display_sign": display_sign
            }
        )

    return render_template(
        "main/transactions.html",
        transaction_display=transaction_display
    )


# ============================================================
# TRANSACTION DETAILS
# ============================================================

@main.route("/transactions/<int:transaction_id>")
@login_required
def transaction_detail(transaction_id):

    check = verified_user_required()

    if check:
        return check

    wallet = db.session.scalar(
        db.select(Wallet).where(
            Wallet.user_id == current_user.id
        )
    )

    if wallet is None:
        flash(
            "Wallet not available. Please contact the administrator.",
            "warning"
        )
        return redirect(url_for("main.dashboard"))

    transaction = db.session.scalar(
        db.select(Transaction)
        .where(Transaction.id == transaction_id)
    )

    if transaction is None:
        flash(
            "Transaction not found.",
            "danger"
        )
        return redirect(url_for("main.transactions"))

    user_entry = db.session.scalar(
        db.select(LedgerEntry).where(
            LedgerEntry.transaction_id == transaction.id,
            LedgerEntry.wallet_id == wallet.id
        )
    )

    if user_entry is None:
        flash(
            "You are not authorized to view this transaction.",
            "danger"
        )
        return redirect(url_for("main.transactions"))

    if transaction.transaction_type == "ADMIN_CREDIT":

        display_type = "Admin Credit"
        display_class = "credit"
        display_sign = "+"

        sender_name = "PayLedger System"
        sender_wallet = "SYSTEM"

        receiver = db.session.get(User, wallet.user_id)
        receiver_name = receiver.name
        receiver_wallet = wallet.wallet_number

    elif transaction.transaction_type == "ADMIN_DEBIT":

        display_type = "Admin Debit"
        display_class = "debit"
        display_sign = "-"

        sender = db.session.get(User, wallet.user_id)
        sender_name = sender.name
        sender_wallet = wallet.wallet_number

        receiver_name = "PayLedger System"
        receiver_wallet = "SYSTEM"

    elif transaction.transaction_type == "MEMBER_TRANSFER":

        sender_entry = db.session.scalar(
            db.select(LedgerEntry).where(
                LedgerEntry.transaction_id == transaction.id,
                LedgerEntry.entry_type == "DEBIT",
                LedgerEntry.wallet_id.is_not(None)
            )
        )

        receiver_entry = db.session.scalar(
            db.select(LedgerEntry).where(
                LedgerEntry.transaction_id == transaction.id,
                LedgerEntry.entry_type == "CREDIT",
                LedgerEntry.wallet_id.is_not(None)
            )
        )

        sender_wallet_obj = db.session.get(
            Wallet,
            sender_entry.wallet_id
        )

        receiver_wallet_obj = db.session.get(
            Wallet,
            receiver_entry.wallet_id
        )

        sender = db.session.get(
            User,
            sender_wallet_obj.user_id
        )

        receiver = db.session.get(
            User,
            receiver_wallet_obj.user_id
        )

        sender_name = sender.name
        sender_wallet = sender_wallet_obj.wallet_number

        receiver_name = receiver.name
        receiver_wallet = receiver_wallet_obj.wallet_number

        if user_entry.entry_type == "DEBIT":
            display_type = "Money Sent"
            display_class = "debit"
            display_sign = "-"
        else:
            display_type = "Money Received"
            display_class = "credit"
            display_sign = "+"

    else:

        display_type = transaction.transaction_type
        display_class = ""
        display_sign = ""

        sender_name = "N/A"
        sender_wallet = "N/A"
        receiver_name = "N/A"
        receiver_wallet = "N/A"

    return render_template(
        "main/transaction_detail.html",
        transaction=transaction,
        display_type=display_type,
        display_class=display_class,
        display_sign=display_sign,
        sender_name=sender_name,
        sender_wallet=sender_wallet,
        receiver_name=receiver_name,
        receiver_wallet=receiver_wallet
    )


# ============================================================
# MEMBER TRANSFER
# ============================================================

@main.route("/transfer", methods=["GET", "POST"])
@login_required
def transfer():
    form = TransferForm()

    check = verified_user_required()

    if check:
        return check

    sender_wallet = db.session.scalar(
        db.select(Wallet).where(
            Wallet.user_id == current_user.id
        )
    )

    if sender_wallet is None:
        flash(
            "Wallet not available. Please contact the administrator.",
            "warning"
        )
        return redirect(url_for("main.dashboard"))

    if request.method == "POST":

        receiver_email = request.form.get(
            "receiver_email",
            ""
        ).strip().lower()

        amount = request.form.get("amount")
        remark = request.form.get("remark", "").strip()

        receiver = db.session.scalar(
            db.select(User).where(
                User.email == receiver_email
            )
        )

        if receiver is None:
            flash(
                "Receiver account not found.",
                "danger"
            )
            return redirect(url_for("main.transfer"))

        receiver_wallet = db.session.scalar(
            db.select(Wallet).where(
                Wallet.user_id == receiver.id
            )
        )

        try:

            member_transfer(
                sender_wallet=sender_wallet,
                receiver_wallet=receiver_wallet,
                amount=amount,
                member_user=current_user,
                remark=remark
            )

            db.session.commit()

            flash(
                "Money transferred successfully.",
                "success"
            )

            return redirect(
                url_for("main.transactions")
            )

        except ValueError as e:

            db.session.rollback()

            flash(
                str(e),
                "danger"
            )

        except Exception:

            db.session.rollback()

            flash(
                "Transfer failed. No changes were made.",
                "danger"
            )

    return render_template(
        "main/transfer.html",
        wallet=sender_wallet,
        form=form
    )