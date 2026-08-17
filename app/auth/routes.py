from flask import (
    Blueprint,
    render_template,
    redirect,
    url_for,
    flash
)

from flask_login import login_user, logout_user, login_required, current_user

from werkzeug.security import (
    generate_password_hash,
    check_password_hash
)

from app import db
from app.models.user import User
from app.auth.forms import RegistrationForm, LoginForm


auth = Blueprint(
    "auth",
    __name__,
    url_prefix="/auth",
    template_folder="templates"
)

@auth.route("/register", methods=["GET", "POST"])
def register():

    form = RegistrationForm()

    if form.validate_on_submit():

        existing_user = db.session.scalar(
            db.select(User).where(
                User.email == form.email.data.lower().strip()
            )
        )

        if existing_user:
            flash("An account with this email already exists.", "danger")
            return redirect(url_for("auth.register"))

        user = User(
            name=form.name.data.strip(),
            email=form.email.data.lower().strip(),
            password_hash=generate_password_hash(
                form.password.data
            )
        )

        db.session.add(user)
        db.session.commit()

        flash(
            "Account created successfully. Please log in.",
            "success"
        )

        return redirect(url_for("auth.login"))

    return render_template(
        "auth/register.html",
        form=form
    )
@auth.route("/login", methods=["GET", "POST"])
def login():

    form = LoginForm()

    if form.validate_on_submit():

        email = form.email.data.lower().strip()

        user = db.session.scalar(
            db.select(User).where(
                User.email == email
            )
        )

        if user is None:
            flash("Invalid email or password.", "danger")
            return redirect(url_for("auth.login"))

        if not check_password_hash(
            user.password_hash,
            form.password.data
        ):
            flash("Invalid email or password.", "danger")
            return redirect(url_for("auth.login"))

        if user.verification_status == "PENDING":
            flash(
                "Your account is waiting for admin verification.",
                "warning"
            )
            return redirect(url_for("auth.login"))

        if user.verification_status == "REJECTED":
            flash(
                "Your account has been rejected. Please contact the administrator.",
                "danger"
            )
            return redirect(url_for("auth.login"))

        login_user(user)


        flash("Login successful!", "success")

        return redirect(url_for("main.dashboard"))
    return render_template(
        "auth/login.html",
        form=form
    )
@auth.route("/logout")
@login_required
def logout():

    logout_user()

    flash("You have been logged out.", "success")

    return redirect(url_for("auth.login"))