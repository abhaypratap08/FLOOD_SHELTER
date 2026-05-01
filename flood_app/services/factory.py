from ..config import Config
from .recommendation import RecommendationService


def build_recommendation_service(db_path: str | None = None) -> RecommendationService:
    return RecommendationService(db_path or Config.DB_PATH)


def recommend_shelters(
    num_people: int,
    distance_level: str,
    accessibility_required: str,
    elevation_input: str,
    proximity_input: str,
    medical_input: str,
):
    service = build_recommendation_service()
    return service.recommend(
        num_people=num_people,
        distance_level=distance_level,
        accessibility_required=accessibility_required,
        elevation_input=elevation_input,
        proximity_input=proximity_input,
        medical_input=medical_input,
    )
