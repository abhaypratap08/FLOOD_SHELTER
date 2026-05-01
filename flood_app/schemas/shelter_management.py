TEXT_FIELDS = {
    "name",
    "accessibility",
    "elevation_level",
    "proximity_to_water",
    "medical_facility",
}

INT_FIELDS = {"capacity", "available_beds"}
FLOAT_FIELDS = {"distance", "latitude", "longitude"}

STATUS_TEXT_FIELDS = {
    "medical_support_level",
    "food_water_status",
    "shelter_status",
    "road_access_status",
    "notes",
}
STATUS_INT_FIELDS = {"available_beds"}


def parse_json_payload(request):
    return request.get_json(force=True, silent=True) or {}


def validate_shelter_payload(payload, partial=False):
    allowed = TEXT_FIELDS | INT_FIELDS | FLOAT_FIELDS
    cleaned = {}

    for key, value in payload.items():
        if key not in allowed:
            continue
        if key in TEXT_FIELDS:
            cleaned[key] = (value or "").strip().lower() if key != "name" else (value or "").strip()
        elif key in INT_FIELDS:
            cleaned[key] = int(value) if value is not None else None
        elif key in FLOAT_FIELDS:
            cleaned[key] = float(value) if value is not None else None

    if not partial:
        required = {"name", "capacity", "available_beds", "distance"}
        missing = [field for field in required if field not in cleaned or cleaned[field] in ("", None)]
        if missing:
            raise ValueError(f"Missing required fields: {', '.join(missing)}")

    if "name" in cleaned and not cleaned["name"]:
        raise ValueError("name is required")

    return cleaned


def validate_status_payload(payload):
    allowed = STATUS_TEXT_FIELDS | STATUS_INT_FIELDS
    cleaned = {}

    for key, value in payload.items():
        if key not in allowed:
            continue
        if key in STATUS_TEXT_FIELDS:
            cleaned[key] = (value or "").strip().lower() if key != "notes" else (value or "").strip()
        elif key in STATUS_INT_FIELDS:
            cleaned[key] = int(value) if value is not None else None

    if not cleaned:
        raise ValueError("At least one status field must be provided")
    return cleaned


def parse_filter_args(args):
    filters = {}
    if args.get("search"):
        filters["search"] = args.get("search").strip()
    if args.get("accessibility"):
        filters["accessibility"] = args.get("accessibility").strip().lower()
    if args.get("medical_facility"):
        filters["medical_facility"] = args.get("medical_facility").strip().lower()
    if args.get("max_distance"):
        filters["max_distance"] = float(args.get("max_distance"))
    if args.get("min_beds"):
        filters["min_beds"] = int(args.get("min_beds"))
    return filters
