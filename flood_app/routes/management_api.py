from flask import Blueprint, g, jsonify, request

from ..models import AuditLog
from ..schemas.shelter_management import (
    parse_filter_args,
    parse_json_payload,
    validate_shelter_payload,
    validate_status_payload,
)
from ..services.auth import login_required, roles_required
from ..services.shelter_management import ShelterManagementService

management_api_bp = Blueprint("management_api", __name__)


def _service():
    return ShelterManagementService()


@management_api_bp.route("/shelters", methods=["GET"])
@login_required
def list_shelters():
    filters = parse_filter_args(request.args)
    return jsonify({"items": _service().list_shelters(filters)})


@management_api_bp.route("/shelters/<int:shelter_id>", methods=["GET"])
@login_required
def get_shelter(shelter_id):
    try:
        shelter = _service().get_shelter(shelter_id)
    except LookupError as exc:
        return jsonify({"error": str(exc)}), 404
    return jsonify({"item": _service().serialize_shelter(shelter)})


@management_api_bp.route("/shelters", methods=["POST"])
@roles_required("admin", "response_officer")
def create_shelter():
    payload = parse_json_payload(request)
    try:
        data = validate_shelter_payload(payload, partial=False)
        shelter = _service().create_shelter(data, g.current_user)
    except ValueError as exc:
        return jsonify({"error": str(exc)}), 400
    return jsonify({"item": _service().serialize_shelter(shelter)}), 201


@management_api_bp.route("/shelters/<int:shelter_id>", methods=["PUT", "PATCH"])
@roles_required("admin", "shelter_manager", "response_officer")
def update_shelter(shelter_id):
    payload = parse_json_payload(request)
    try:
        data = validate_shelter_payload(payload, partial=True)
        shelter = _service().update_shelter(shelter_id, data, g.current_user)
    except ValueError as exc:
        return jsonify({"error": str(exc)}), 400
    except LookupError as exc:
        return jsonify({"error": str(exc)}), 404
    return jsonify({"item": _service().serialize_shelter(shelter)})


@management_api_bp.route("/shelters/<int:shelter_id>/status", methods=["POST"])
@roles_required("admin", "shelter_manager", "response_officer")
def record_shelter_status(shelter_id):
    payload = parse_json_payload(request)
    try:
        data = validate_status_payload(payload)
        status = _service().record_status(shelter_id, data, g.current_user)
    except ValueError as exc:
        return jsonify({"error": str(exc)}), 400
    except LookupError as exc:
        return jsonify({"error": str(exc)}), 404
    return jsonify({"item": _service().serialize_latest_status(status)}), 201


@management_api_bp.route("/audit-logs", methods=["GET"])
@roles_required("admin", "response_officer")
def list_audit_logs():
    entries = (
        AuditLog.query.order_by(AuditLog.created_at.desc(), AuditLog.id.desc())
        .limit(100)
        .all()
    )
    return jsonify(
        {
            "items": [
                {
                    "id": entry.id,
                    "actor_user_id": entry.actor_user_id,
                    "shelter_id": entry.shelter_id,
                    "entity_type": entry.entity_type,
                    "entity_id": entry.entity_id,
                    "action": entry.action,
                    "before_state": entry.before_state,
                    "after_state": entry.after_state,
                    "created_at": entry.created_at.isoformat() if entry.created_at else None,
                }
                for entry in entries
            ]
        }
    )
