from recommender import recommend_shelters


def main():
    num_people = int(input("Enter number of people: ").strip())
    distance_level = input("How far can you travel? (near / medium / far): ").strip().lower()
    accessibility_required = input("Accessibility needed? (easy / moderate / difficult): ").strip().lower()
    elevation_input = input("Your elevation level? (low / medium / high): ").strip().lower()
    proximity_input = input("How close to water? (very close / moderate / far): ").strip().lower()
    medical_input = input("Medical support needed? (none / basic / advanced): ").strip().lower()

    data = recommend_shelters(
        num_people=num_people,
        distance_level=distance_level,
        accessibility_required=accessibility_required,
        elevation_input=elevation_input,
        proximity_input=proximity_input,
        medical_input=medical_input,
    )

    if not data["recommendations"]:
        print("\nNo shelters matched your criteria.")
        return

    print("\nRanked shelters:\n")
    for shelter in data["recommendations"]:
        print(
            f"{shelter['name']}: score={shelter['score']}, "
            f"distance={shelter['distance']} km, beds={shelter['available_beds']}, "
            f"access={shelter['accessibility']}"
        )

    best = data["best"]
    print(f"\nBest match: {best['name']} (score {best['score']})")


if __name__ == "__main__":
    main()
