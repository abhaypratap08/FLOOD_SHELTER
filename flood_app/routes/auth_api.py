from flask import Blueprint, g, jsonify, request

from ..models import USER_ROLES
from ..schemas.auth import parse_auth_json, validate_login_payload, validate_signup_payload
from ..services.auth import AuthService, login_required, roles_required

api_auth_bp = Blueprint("api_auth", __name__, url_prefix="/auth")


def _user_payload(user):
    return {
        "id": user.id,
        "full_name": user.full_name,
        "email": user.email,
        "role": user.role,
        "is_active": user.is_active,
    }


@api_auth_bp.route("/signup", methods=["POST"])
def signup():
    payload = parse_auth_json(request)
    try:
        validate_signup_payload(payload, ("citizen",))
        user = AuthService().create_user(
            full_name=payload["full_name"],
            email=payload["email"],
            password=payload["password"],
            role=payload["role"],
        )
        AuthService().login_user(user)
    except ValueError as exc:
        return jsonify({"error": str(exc)}), 400
    return jsonify({"user": _user_payload(user)}), 201


@api_auth_bp.route("/login", methods=["POST"])
def login():
    payload = parse_auth_json(request)
    try:
        validate_login_payload(payload)
        user = AuthService().authenticate(payload["email"], payload["password"])
        AuthService().login_user(user)
    except ValueError as exc:
        return jsonify({"error": str(exc)}), 400
    return jsonify({"user": _user_payload(user)})


@api_auth_bp.route("/logout", methods=["POST"])
@login_required
def logout():
    AuthService().logout_user()
    return jsonify({"ok": True})


@api_auth_bp.route("/me", methods=["GET"])
@login_required
def me():
    return jsonify({"user": _user_payload(g.current_user)})


@api_auth_bp.route("/roles", methods=["GET"])
@roles_required("admin", "response_officer")
def roles():
    return jsonify({"roles": list(USER_ROLES)})
