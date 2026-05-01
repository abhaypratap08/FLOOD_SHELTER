from ..db import db
from ..models import Shelter, ShelterStatus
from .audit import write_audit_log


class ShelterManagementService:
    def list_shelters(self, filters):
        query = Shelter.query
        if filters.get("search"):
            search = f"%{filters['search']}%"
            query = query.filter(Shelter.name.ilike(search))
        if filters.get("accessibility"):
            query = query.filter(Shelter.accessibility == filters["accessibility"])
        if filters.get("medical_facility"):
            query = query.filter(Shelter.medical_facility == filters["medical_facility"])
        if filters.get("max_distance") is not None:
            query = query.filter(Shelter.distance <= filters["max_distance"])
        if filters.get("min_beds") is not None:
            query = query.filter(Shelter.available_beds >= filters["min_beds"])
        return [self.serialize_shelter(row) for row in query.order_by(Shelter.name.asc()).all()]

    def get_shelter(self, shelter_id):
        shelter = db.session.get(Shelter, shelter_id)
        if shelter is None:
            raise LookupError("Shelter not found.")
        return shelter

    def create_shelter(self, payload, actor_user):
        shelter = Shelter(**payload)
        db.session.add(shelter)
        db.session.flush()
        write_audit_log(
            actor_user_id=actor_user.id,
            shelter_id=shelter.id,
            entity_type="shelter",
            entity_id=shelter.id,
            action="create",
            before_state=None,
            after_state=self.serialize_shelter(shelter),
        )
        db.session.commit()
        return shelter

    def update_shelter(self, shelter_id, payload, actor_user):
        shelter = self.get_shelter(shelter_id)
        before_state = self.serialize_shelter(shelter)
        for key, value in payload.items():
            setattr(shelter, key, value)
        db.session.flush()
        write_audit_log(
            actor_user_id=actor_user.id,
            shelter_id=shelter.id,
            entity_type="shelter",
            entity_id=shelter.id,
            action="update",
            before_state=before_state,
            after_state=self.serialize_shelter(shelter),
        )
        db.session.commit()
        return shelter

    def record_status(self, shelter_id, payload, actor_user):
        shelter = self.get_shelter(shelter_id)
        before_state = self.serialize_latest_status(shelter.status_entries[-1] if shelter.status_entries else None)
        status = ShelterStatus(
            shelter_id=shelter.id,
            updated_by_user_id=actor_user.id,
            **payload,
        )
        if payload.get("available_beds") is not None:
            shelter.available_beds = payload["available_beds"]
        db.session.add(status)
        db.session.flush()
        write_audit_log(
            actor_user_id=actor_user.id,
            shelter_id=shelter.id,
            entity_type="shelter_status",
            entity_id=status.id,
            action="status_update",
            before_state=before_state,
            after_state=self.serialize_latest_status(status),
        )
        db.session.commit()
        return status

    def serialize_shelter(self, shelter):
        latest_status = shelter.status_entries[-1] if shelter.status_entries else None
        return {
            "id": shelter.id,
            "name": shelter.name,
            "capacity": shelter.capacity,
            "available_beds": shelter.available_beds,
            "distance": shelter.distance,
            "accessibility": shelter.accessibility,
            "elevation_level": shelter.elevation_level,
            "proximity_to_water": shelter.proximity_to_water,
            "medical_facility": shelter.medical_facility,
            "latitude": shelter.latitude,
            "longitude": shelter.longitude,
            "latest_status": self.serialize_latest_status(latest_status),
        }

    def serialize_latest_status(self, status):
        if status is None:
            return None
        return {
            "id": status.id,
            "available_beds": status.available_beds,
            "medical_support_level": status.medical_support_level,
            "food_water_status": status.food_water_status,
            "shelter_status": status.shelter_status,
            "road_access_status": status.road_access_status,
            "notes": status.notes,
            "updated_by_user_id": status.updated_by_user_id,
            "recorded_at": status.recorded_at.isoformat() if status.recorded_at else None,
        }
