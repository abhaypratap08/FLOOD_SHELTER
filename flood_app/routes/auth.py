from flask import Blueprint, g, redirect, render_template, request, url_for

from ..schemas.auth import parse_auth_form, validate_login_payload, validate_signup_payload
from ..services.auth import AuthService, login_required

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    error = None
    next_url = request.args.get("next") or request.form.get("next") or url_for("web.home")
    if request.method == "POST":
        payload = parse_auth_form(request.form)
        try:
            validate_login_payload(payload)
            user = AuthService().authenticate(payload["email"], payload["password"])
            AuthService().login_user(user)
            return redirect(next_url)
        except ValueError as exc:
            error = str(exc)

    return render_template("auth_login.html", error=error, next_url=next_url)


@auth_bp.route("/signup", methods=["GET", "POST"])
def signup():
    error = None
    next_url = request.args.get("next") or request.form.get("next") or url_for("web.home")
    if request.method == "POST":
        payload = parse_auth_form(request.form)
        try:
            validate_signup_payload(payload, ("citizen",))
            user = AuthService().create_user(
                full_name=payload["full_name"],
                email=payload["email"],
                password=payload["password"],
                role=payload["role"],
            )
            AuthService().login_user(user)
            return redirect(next_url)
        except ValueError as exc:
            error = str(exc)

    return render_template("auth_signup.html", error=error, next_url=next_url)


@auth_bp.route("/logout", methods=["POST"])
@login_required
def logout():
    AuthService().logout_user()
    return redirect(url_for("web.home"))


@auth_bp.route("/me", methods=["GET"])
@login_required
def me():
    return render_template("auth_profile.html", user=g.current_user)
