import sqlite3
from typing import Dict, List

from membership_func import get_fuzzy_simulator

DB_PATH = "shelter.db"

DISTANCE_MAP = {"near": 3, "medium": 10, "far": 18}
ACCESS_MAP = {"difficult": 2, "moderate": 5, "easy": 8}
ELEVATION_MAP = {"low": 2, "medium": 5, "high": 8}
PROXIMITY_MAP = {"very close": 2, "moderate": 5, "far": 8}
MEDICAL_MAP = {"none": 2, "basic": 5, "advanced": 8}


def _query_shelters(num_people: int, max_distance: float, accessibility_required: str):
    conn = sqlite3.connect(DB_PATH)
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
          AND LOWER(accessibility) = ?
        """,
        (num_people, max_distance, accessibility_required),
    )
    rows = cursor.fetchall()
    conn.close()
    return rows


def recommend_shelters(
    num_people: int,
    distance_level: str,
    accessibility_required: str,
    elevation_input: str,
    proximity_input: str,
    medical_input: str,
) -> Dict:
    distance_level = distance_level.strip().lower()
    accessibility_required = accessibility_required.strip().lower()
    elevation_input = elevation_input.strip().lower()
    proximity_input = proximity_input.strip().lower()
    medical_input = medical_input.strip().lower()

    max_distance = DISTANCE_MAP.get(distance_level, 10)
    elevation_num = ELEVATION_MAP.get(elevation_input, 5)
    proximity_num = PROXIMITY_MAP.get(proximity_input, 5)
    medical_num = MEDICAL_MAP.get(medical_input, 5)

    rows = _query_shelters(num_people, max_distance, accessibility_required)
    recommendations: List[Dict] = []

    for row in rows:
        access_num = ACCESS_MAP.get(row["accessibility"].lower(), 5)
        score = float(
            get_fuzzy_simulator(
                row["capacity"],
                row["distance"],
                access_num,
                elevation_num,
                proximity_num,
                medical_num,
            )
        )
        recommendations.append(
            {
                "name": row["name"],
                "capacity": row["capacity"],
                "available_beds": row["available_beds"],
                "distance": row["distance"],
                "accessibility": row["accessibility"],
                "elevation_level": row["elevation_level"],
                "proximity_to_water": row["proximity_to_water"],
                "medical_facility": row["medical_facility"],
                "score": round(score, 2),
                "lat": row["latitude"] if row["latitude"] is not None else 20.3000,
                "lng": row["longitude"] if row["longitude"] is not None else 85.8200,
            }
        )

    recommendations.sort(key=lambda item: item["score"], reverse=True)

    best = recommendations[0] if recommendations else None

    return {
        "filters": {
            "num_people": num_people,
            "distance_level": distance_level,
            "accessibility_required": accessibility_required,
            "elevation_input": elevation_input,
            "proximity_input": proximity_input,
            "medical_input": medical_input,
        },
        "inputs_numeric": {
            "distance": DISTANCE_MAP.get(distance_level, 10),
            "accessibility": ACCESS_MAP.get(accessibility_required, 5),
            "elevation": elevation_num,
            "proximity": proximity_num,
            "medical": medical_num,
        },
        "recommendations": recommendations,
        "best": best,
    }
