from flask import Flask, jsonify, render_template, request

from recommender import recommend_shelters

app = Flask(__name__)

CHOICES = {
    "distance_level": ["near", "medium", "far"],
    "accessibility_required": ["easy", "moderate", "difficult"],
    "elevation_input": ["low", "medium", "high"],
    "proximity_input": ["very close", "moderate", "far"],
    "medical_input": ["none", "basic", "advanced"],
}


@app.route("/", methods=["GET"])
def home():
    return render_template("index.html", choices=CHOICES, data=None, error=None)


@app.route("/recommend", methods=["POST"])
def recommend():
    try:
        num_people = int(request.form.get("num_people", "1"))
        if num_people < 1:
            raise ValueError("Number of people must be at least 1.")
    except ValueError:
        return render_template(
            "index.html",
            choices=CHOICES,
            data=None,
            error="Enter a valid number of people (>= 1).",
        )

    data = recommend_shelters(
        num_people=num_people,
        distance_level=request.form.get("distance_level", "medium"),
        accessibility_required=request.form.get("accessibility_required", "moderate"),
        elevation_input=request.form.get("elevation_input", "medium"),
        proximity_input=request.form.get("proximity_input", "moderate"),
        medical_input=request.form.get("medical_input", "basic"),
    )
    return render_template("index.html", choices=CHOICES, data=data, error=None)


@app.route("/api/recommend", methods=["POST"])
def api_recommend():
    payload = request.get_json(force=True, silent=True) or {}
    try:
        num_people = int(payload.get("num_people", 1))
    except (TypeError, ValueError):
        return jsonify({"error": "num_people must be an integer"}), 400

    data = recommend_shelters(
        num_people=num_people,
        distance_level=payload.get("distance_level", "medium"),
        accessibility_required=payload.get("accessibility_required", "moderate"),
        elevation_input=payload.get("elevation_input", "medium"),
        proximity_input=payload.get("proximity_input", "moderate"),
        medical_input=payload.get("medical_input", "basic"),
    )
    return jsonify(data)


if __name__ == "__main__":
    app.run(debug=True)
