from flask import Blueprint, g, redirect, render_template, request, url_for

from ..models import AuditLog
from ..schemas.shelter_management import validate_shelter_payload, validate_status_payload
from ..services.auth import login_required, roles_required
from ..services.shelter_management import ShelterManagementService

management_web_bp = Blueprint("management_web", __name__, url_prefix="/manage")


def _service():
    return ShelterManagementService()


def _form_defaults():
    return {
        "name": "",
        "capacity": "",
        "available_beds": "",
        "distance": "",
        "accessibility": "moderate",
        "elevation_level": "medium",
        "proximity_to_water": "moderate",
        "medical_facility": "basic",
        "latitude": "",
        "longitude": "",
    }


@management_web_bp.route("/shelters", methods=["GET"])
@roles_required("admin", "shelter_manager", "response_officer")
def shelters():
    filters = {
        "search": (request.args.get("search") or "").strip(),
        "accessibility": (request.args.get("accessibility") or "").strip().lower(),
        "medical_facility": (request.args.get("medical_facility") or "").strip().lower(),
    }
    if request.args.get("max_distance"):
        filters["max_distance"] = float(request.args["max_distance"])
    if request.args.get("min_beds"):
        filters["min_beds"] = int(request.args["min_beds"])
    items = _service().list_shelters(filters)
    return render_template("manage_shelters.html", items=items, filters=filters)


@management_web_bp.route("/shelters/new", methods=["GET", "POST"])
@roles_required("admin", "response_officer")
def create_shelter():
    error = None
    form_data = _form_defaults()
    if request.method == "POST":
        form_data.update(request.form.to_dict())
        try:
            payload = validate_shelter_payload(request.form.to_dict(), partial=False)
            shelter = _service().create_shelter(payload, g.current_user)
            return redirect(url_for("management_web.edit_shelter", shelter_id=shelter.id))
        except ValueError as exc:
            error = str(exc)
    return render_template("manage_shelter_form.html", shelter=None, form_data=form_data, error=error)


@management_web_bp.route("/shelters/<int:shelter_id>/edit", methods=["GET", "POST"])
@roles_required("admin", "shelter_manager", "response_officer")
def edit_shelter(shelter_id):
    try:
        shelter = _service().get_shelter(shelter_id)
    except LookupError:
        return redirect(url_for("management_web.shelters"))

    error = None
    form_data = _service().serialize_shelter(shelter)
    if request.method == "POST":
        form_data.update(request.form.to_dict())
        try:
            payload = validate_shelter_payload(request.form.to_dict(), partial=True)
            shelter = _service().update_shelter(shelter_id, payload, g.current_user)
            form_data = _service().serialize_shelter(shelter)
        except ValueError as exc:
            error = str(exc)
    return render_template("manage_shelter_form.html", shelter=shelter, form_data=form_data, error=error)


@management_web_bp.route("/shelters/<int:shelter_id>/status", methods=["GET", "POST"])
@roles_required("admin", "shelter_manager", "response_officer")
def shelter_status(shelter_id):
    try:
        shelter = _service().get_shelter(shelter_id)
    except LookupError:
        return redirect(url_for("management_web.shelters"))

    error = None
    latest_status = _service().serialize_latest_status(shelter.status_entries[-1] if shelter.status_entries else None)
    form_data = latest_status or {
        "available_beds": shelter.available_beds or "",
        "medical_support_level": "",
        "food_water_status": "",
        "shelter_status": "operational",
        "road_access_status": "",
        "notes": "",
    }
    if request.method == "POST":
        form_data.update(request.form.to_dict())
        try:
            payload = validate_status_payload(request.form.to_dict())
            status = _service().record_status(shelter_id, payload, g.current_user)
            latest_status = _service().serialize_latest_status(status)
            form_data = latest_status
        except ValueError as exc:
            error = str(exc)
    return render_template(
        "manage_shelter_status.html",
        shelter=shelter,
        latest_status=latest_status,
        form_data=form_data,
        error=error,
    )


@management_web_bp.route("/audit-logs", methods=["GET"])
@roles_required("admin", "response_officer")
def audit_logs():
    items = (
        AuditLog.query.order_by(AuditLog.created_at.desc(), AuditLog.id.desc())
        .limit(100)
        .all()
    )
    return render_template("manage_audit_logs.html", items=items)
