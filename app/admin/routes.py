from decimal import Decimal

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

from app.models.user import User
from app.models.wallet import Wallet
from app.models.ledger_entry import LedgerEntry
from app.models.transaction import Transaction

from app.services.ledger_service import (
    admin_credit,
    admin_debit
)


admin = Blueprint(
    "admin",
    __name__,
    url_prefix="/admin",
    template_folder="templates"
)


# ============================================================
# ADMIN - CONTROL PANEL
# ============================================================
@admin.route("/")
@login_required
def dashboard():
    if current_user.role != "ADMIN":
        flash("Access denied. Admins only.", "danger")
        return redirect(url_for("main.dashboard"))

    users_count = db.session.scalar(
        db.select(db.func.count(User.id))
    ) or 0

    wallets_count = db.session.scalar(
        db.select(db.func.count(Wallet.id))
    ) or 0

    transactions_count = db.session.scalar(
        db.select(db.func.count(Transaction.id))
    ) or 0

    return render_template(
        "admin/dashboard.html",
        users_count=users_count,
        wallets_count=wallets_count,
        transactions_count=transactions_count
    )


# ============================================================
# ADMIN - PENDING USERS
# ============================================================

@admin.route("/users")
@login_required
def users():

    if current_user.role != "ADMIN":
        flash("Access denied. Admins only.", "danger")
        return redirect(url_for("main.dashboard"))

    users = db.session.scalars(
        db.select(User)
        .order_by(User.id)
    ).all()

    return render_template(
        "admin/users.html",
        users=users
    )


# ============================================================
# ADMIN - VERIFY USER
# ============================================================

@admin.route(
    "/users/<int:user_id>/verify",
    methods=["POST"]
)
@login_required
def verify_user(user_id):

    if current_user.role != "ADMIN":
        flash("Access denied. Admins only.", "danger")
        return redirect(url_for("main.dashboard"))

    user = db.session.get(User, user_id)

    if user is None:
        flash("User not found.", "danger")
        return redirect(url_for("admin.users"))

    if user.verification_status != "PENDING":
        flash(
            "This user has already been processed.",
            "warning"
        )
        return redirect(url_for("admin.users"))

    # Verify the user
    user.verification_status = "VERIFIED"

    # Check whether the user already has a wallet
    existing_wallet = db.session.scalar(
        db.select(Wallet).where(
            Wallet.user_id == user.id
        )
    )

    if existing_wallet is None:

        existing_wallet_numbers = db.session.scalars(
            db.select(Wallet.wallet_number)
        ).all()

        used_numbers = []

        for number in existing_wallet_numbers:
            if number.startswith("PL"):
                try:
                    used_numbers.append(int(number[2:]))
                except ValueError:
                    pass

        next_wallet_number = (
            max(used_numbers, default=0) + 1
        )

        wallet_number = f"PL{next_wallet_number:08d}"

        wallet = Wallet(
            wallet_number=wallet_number,
            user_id=user.id,
            balance=Decimal("0.00"),
            status="ACTIVE"
        )

        db.session.add(wallet)

    db.session.commit()

    flash(
        f"{user.name} has been verified and wallet created successfully.",
        "success"
    )

    return redirect(url_for("admin.users"))


# ============================================================
# ADMIN - REJECT USER
# ============================================================

@admin.route(
    "/users/<int:user_id>/reject",
    methods=["POST"]
)
@login_required
def reject_user(user_id):

    if current_user.role != "ADMIN":
        flash("Access denied. Admins only.", "danger")
        return redirect(url_for("main.dashboard"))

    user = db.session.get(User, user_id)

    if user is None:
        flash("User not found.", "danger")
        return redirect(url_for("admin.users"))

    if user.verification_status != "PENDING":
        flash(
            "This user has already been processed.",
            "warning"
        )
        return redirect(url_for("admin.users"))

    user.verification_status = "REJECTED"

    db.session.commit()

    flash(
        f"{user.name} has been rejected.",
        "danger"
    )

    return redirect(url_for("admin.users"))


# ============================================================
# ADMIN - WALLET LIST
# ============================================================

@admin.route("/wallets")
@login_required
def wallets():

    if current_user.role != "ADMIN":
        flash("Access denied. Admins only.", "danger")
        return redirect(url_for("main.dashboard"))

    wallets = db.session.scalars(
        db.select(Wallet)
        .join(User)
        .where(
            User.verification_status == "VERIFIED"
        )
        .order_by(Wallet.id)
    ).all()

    return render_template(
        "admin/wallets.html",
        wallets=wallets
    )


# ============================================================
# ADMIN - CREDIT WALLET
# ============================================================

@admin.route(
    "/wallets/<int:wallet_id>/credit",
    methods=["POST"]
)
@login_required
def credit_wallet(wallet_id):

    if current_user.role != "ADMIN":
        flash("Access denied. Admins only.", "danger")
        return redirect(url_for("main.dashboard"))

    wallet = db.session.get(Wallet, wallet_id)

    if wallet is None:
        flash("Wallet not found.", "danger")
        return redirect(url_for("admin.wallets"))

    amount = request.form.get("amount")
    remark = request.form.get("remark")

    try:

        admin_credit(
            wallet=wallet,
            amount=amount,
            admin_user=current_user,
            remark=remark
        )

        db.session.commit()

        flash(
            f"₹{amount} credited successfully to "
            f"{wallet.wallet_number}.",
            "success"
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
            "Credit failed. No changes were made.",
            "danger"
        )

    return redirect(url_for("admin.wallets"))


# ============================================================
# ADMIN - DEBIT WALLET
# ============================================================

@admin.route(
    "/wallets/<int:wallet_id>/debit",
    methods=["POST"]
)
@login_required
def debit_wallet(wallet_id):

    if current_user.role != "ADMIN":
        flash("Access denied. Admins only.", "danger")
        return redirect(url_for("main.dashboard"))

    wallet = db.session.get(Wallet, wallet_id)

    if wallet is None:
        flash("Wallet not found.", "danger")
        return redirect(url_for("admin.wallets"))

    amount = request.form.get("amount")
    remark = request.form.get("remark")

    try:

        admin_debit(
            wallet=wallet,
            amount=amount,
            admin_user=current_user,
            remark=remark
        )

        db.session.commit()

        flash(
            f"₹{amount} debited successfully from "
            f"{wallet.wallet_number}.",
            "success"
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
            "Debit failed. No changes were made.",
            "danger"
        )

    return redirect(url_for("admin.wallets"))


# ============================================================
# ADMIN - TRANSACTION HISTORY
# ============================================================

@admin.route("/transactions")
@login_required
def transactions():

    if current_user.role != "ADMIN":
        flash("Access denied. Admins only.", "danger")
        return redirect(url_for("main.dashboard"))

    transactions = db.session.scalars(
        db.select(Transaction)
        .order_by(
            Transaction.created_at.desc()
        )
    ).all()

    transaction_display = []

    for transaction in transactions:

        entries = db.session.scalars(
            db.select(LedgerEntry).where(
                LedgerEntry.transaction_id == transaction.id
            )
        ).all()

        sender_name = "PayLedger System"
        sender_wallet = "SYSTEM"

        receiver_name = "PayLedger System"
        receiver_wallet = "SYSTEM"

        for entry in entries:

            if entry.wallet_id is None:
                continue

            wallet = db.session.get(
                Wallet,
                entry.wallet_id
            )

            if wallet is None:
                continue

            user = db.session.get(
                User,
                wallet.user_id
            )

            if user is None:
                continue

            if entry.entry_type == "DEBIT":

                sender_name = user.name
                sender_wallet = wallet.wallet_number

            elif entry.entry_type == "CREDIT":

                receiver_name = user.name
                receiver_wallet = wallet.wallet_number

        transaction_display.append(
            {
                "transaction": transaction,
                "sender_name": sender_name,
                "sender_wallet": sender_wallet,
                "receiver_name": receiver_name,
                "receiver_wallet": receiver_wallet
            }
        )

    return render_template(
        "admin/transactions.html",
        transaction_display=transaction_display
    )
