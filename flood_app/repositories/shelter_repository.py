import sqlite3
from dataclasses import asdict
from typing import List

from flask import has_app_context

from ..db import db
from ..models.shelter import Shelter


class ShelterRepository:
    def __init__(self, db_path: str):
        self.db_path = db_path

    def fetch_dataset_info(self) -> dict:
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='app_metadata'")
        has_metadata = cursor.fetchone() is not None

        dataset_info = {
            "source_type": "demo",
            "dataset_name": "Built-in demo shelters",
            "record_count": 0,
            "is_demo": True,
        }

        if has_metadata:
            cursor.execute("SELECT key, value FROM app_metadata")
            metadata = {row["key"]: row["value"] for row in cursor.fetchall()}
            dataset_info["source_type"] = metadata.get("source_type", dataset_info["source_type"])
            dataset_info["dataset_name"] = metadata.get("dataset_name", dataset_info["dataset_name"])

        cursor.execute("SELECT COUNT(*) AS count FROM shelters")
        dataset_info["record_count"] = int(cursor.fetchone()["count"])

        if not has_metadata:
            cursor.execute("SELECT COUNT(*) AS demo_count FROM shelters WHERE name GLOB 'Shelter [A-Z]'")
            demo_count = int(cursor.fetchone()["demo_count"])
            dataset_info["is_demo"] = demo_count == dataset_info["record_count"] and dataset_info["record_count"] > 0
            if not dataset_info["is_demo"]:
                dataset_info["source_type"] = "custom"
                dataset_info["dataset_name"] = "Imported shelter dataset"
        else:
            dataset_info["is_demo"] = dataset_info["source_type"] == "demo"

        conn.close()
        return dataset_info

    def fetch_candidates(self, min_beds: int, max_distance: float) -> List[dict]:
        if db is not None and Shelter is not None and has_app_context():
            return self._fetch_candidates_orm(min_beds, max_distance)
        return self._fetch_candidates_sqlite(min_beds, max_distance)

    def _fetch_candidates_orm(self, min_beds: int, max_distance: float) -> List[dict]:
        shelters = (
            Shelter.query.filter(Shelter.available_beds >= min_beds, Shelter.distance <= max_distance)
            .order_by(Shelter.distance.asc())
            .all()
        )
        return [asdict(shelter.to_record()) for shelter in shelters]

    def _fetch_candidates_sqlite(self, min_beds: int, max_distance: float) -> List[dict]:
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT name, capacity, available_beds, distance, accessibility,
                   elevation_level, proximity_to_water, medical_facility,
                   latitude, longitude
            FROM shelters
            WHERE available_beds >= ?
              AND distance <= ?
            """,
            (min_beds, max_distance),
        )
        rows = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return rows
