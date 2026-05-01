def parse_auth_form(form_data):
    return {
        "full_name": (form_data.get("full_name") or "").strip(),
        "email": (form_data.get("email") or "").strip().lower(),
        "password": form_data.get("password") or "",
        "role": "citizen",
    }


def parse_auth_json(request):
    payload = request.get_json(force=True, silent=True) or {}
    return {
        "full_name": (payload.get("full_name") or "").strip(),
        "email": (payload.get("email") or "").strip().lower(),
        "password": payload.get("password") or "",
        "role": "citizen",
    }


def validate_signup_payload(payload, allowed_roles):
    if not payload["full_name"]:
        raise ValueError("full_name is required")
    if not payload["email"] or "@" not in payload["email"]:
        raise ValueError("valid email is required")
    if len(payload["password"]) < 8:
        raise ValueError("password must be at least 8 characters")
    if payload["role"] not in allowed_roles:
        raise ValueError("invalid role")
    return payload


def validate_login_payload(payload):
    if not payload["email"] or "@" not in payload["email"]:
        raise ValueError("valid email is required")
    if not payload["password"]:
        raise ValueError("password is required")
    return payload
