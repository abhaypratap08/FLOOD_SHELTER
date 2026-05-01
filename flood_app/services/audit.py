from ..db import db
from ..models import AuditLog


def write_audit_log(*, actor_user_id, shelter_id, entity_type, entity_id, action, before_state=None, after_state=None):
    entry = AuditLog(
        actor_user_id=actor_user_id,
        shelter_id=shelter_id,
        entity_type=entity_type,
        entity_id=str(entity_id),
        action=action,
        before_state=before_state,
        after_state=after_state,
    )
    db.session.add(entry)
    return entry
