# Flood Shelter Recommendation System using Fuzzy Logic

This project recommends safe flood shelters using fuzzy logic. It now supports:

- CLI mode (`user_input.py`)
- Desktop GUI (Tkinter) (`desktop_gui.py`)
- Web app (Flask + Bootstrap + Chart.js + Leaflet) (`app.py`)

## Features

- Fuzzy suitability score (`0-100`) for each shelter
- Ranked shelter recommendations
- Visual score bars and charts (bar + radar)
- Interactive map with shelter pins and score popups
- Geolocation-backed shelters (`latitude`/`longitude` stored in SQLite)
- JSON API endpoint for integrations (`/api/recommend`)

## Project Structure

- `membership_func.py`: fuzzy membership functions and rule base
- `recommender.py`: shared recommendation engine used by all interfaces
- `database.py`: creates and seeds `shelter.db`
- `user_input.py`: CLI app
- `desktop_gui.py`: desktop app (Tkinter)
- `app.py`: Flask backend + routes
- `PORTFOLIO.md`: resume bullets + showcase script/checklist
- `templates/index.html`: frontend page
- `static/css/styles.css`: app styles
- `static/js/app.js`: charts + map logic

## Setup

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python database.py
```

## Run

### 1) CLI

```bash
python user_input.py
```

### 2) Desktop GUI

```bash
python desktop_gui.py
```

### 3) Flask Web App

```bash
python app.py
```

Open `http://127.0.0.1:5000`.

## Data Model Note

The `shelters` table includes:

- operational fields: capacity, available beds, distance, accessibility
- risk/medical fields: elevation level, proximity to water, medical facility
- map fields: `latitude`, `longitude`

## Deploy

### Render

1. Push this repo to GitHub.
2. Create a new Web Service in Render.
3. Build command: `pip install -r requirements.txt`
4. Start command: `gunicorn app:app`
5. Add a one-time job/command to seed DB: `python database.py`

### Vercel

This repo includes `vercel.json` for Flask Python runtime.

1. Import project in Vercel.
2. Deploy.
3. Ensure `shelter.db` exists in deployment flow (run `python database.py` before deploy artifact build, or commit a prebuilt DB for demo use).

## Tech Stack

- Python
- Flask
- SQLite
- NumPy
- scikit-fuzzy
- Bootstrap 5
- Chart.js
- Leaflet + OpenStreetMap
