# Portfolio Pack: Flood Shelter Fuzzy Recommender

## 1) Resume Bullets

- Built a flood shelter recommendation system using fuzzy logic (Mamdani inference) to rank shelters with a `0-100` suitability score under uncertain emergency conditions.
- Engineered a full-stack Flask app with interactive charts (Chart.js) and geospatial map visualization (Leaflet/OpenStreetMap) for real-time shelter decision support.
- Developed a reusable recommendation core consumed by CLI, desktop GUI (Tkinter), and web interfaces, reducing logic duplication and improving maintainability.
- Designed SQLite data model with geolocation (`latitude`, `longitude`) and operational attributes (beds, distance, accessibility, medical support) to power map-aware recommendations.
- Prepared production-style deployment for Render/Vercel with `gunicorn`, configuration files, and reproducible setup for portfolio demonstration.

## 2) ATS-Friendly Project Summary

Flood Shelter Fuzzy Recommender is a decision-support application that uses fuzzy logic to recommend suitable flood shelters based on distance tolerance, accessibility requirements, elevation risk, proximity to water, medical urgency, and available beds. The system includes a Flask web interface, interactive score visualizations, and a Leaflet-based map of recommended shelters. It also provides CLI and desktop GUI clients driven by a shared recommendation engine.

## 3) Interview Demo Script (60-90 seconds)

1. Open the web app home screen and explain the goal: ranking safest shelters, not just nearest shelters.
2. Select user constraints (people count, accessibility, medical need) and submit.
3. Show ranked output and highlight the top shelter score.
4. Show charts:
   - bar chart for shelter score comparison,
   - radar chart for user input profile.
5. Open map section and click a pin to display shelter name, score, and distance.
6. Mention architecture: fuzzy engine + SQLite + Flask + map/chart frontend + deployability.

## 4) Screenshot Checklist

- `01-home-form.png`: clean input form view
- `02-ranked-results.png`: recommendation cards and best match
- `03-score-chart.png`: bar chart section
- `04-map-pins.png`: shelter pins with popup
- `05-desktop-gui.png`: Tkinter app with ranked table

Tip: keep image widths consistent and include one short caption under each image in your portfolio page.

## 5) Suggested GitHub Repository Description

Fuzzy-logic flood shelter recommender with Flask web app, Tkinter desktop GUI, interactive charts, and Leaflet map visualization.
