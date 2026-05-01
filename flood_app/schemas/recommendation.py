CHOICES = {
    "distance_level": ["near", "medium", "far"],
    "accessibility_required": ["easy", "moderate", "difficult"],
    "elevation_input": ["low", "medium", "high"],
    "proximity_input": ["very close", "moderate", "far"],
    "medical_input": ["none", "basic", "advanced"],
}


def validate_num_people(raw_value):
    num_people = int(raw_value)
    if num_people < 1:
        raise ValueError
    return num_people


def parse_form_payload(form_data):
    return form_data.to_dict(flat=True)


def parse_json_payload(request):
    return request.get_json(force=True, silent=True) or {}
