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

- `flood_app/config.py`: environment-based application config
- `flood_app/routes/`: Flask web and API routes
- `flood_app/services/`: recommendation service + service factory
- `flood_app/repositories/`: database access layer
- `flood_app/models/`: SQLAlchemy models
- `flood_app/schemas/`: shared input choices and validation
- `membership_func.py`: fuzzy membership functions and rule base
- `recommender.py`: compatibility wrapper for legacy CLI/desktop entry points
- `database.py`: creates and seeds `shelter.db`
- `import_shelters.py`: imports a real/custom shelter CSV into `shelter.db`
- `shelters_template.csv`: starter CSV layout for real shelter imports
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

Optional environment overrides:

```bash
set FLASK_DEBUG=false
set FLASK_RUN_HOST=0.0.0.0
set FLASK_RUN_PORT=5000
set DB_PATH=C:\path\to\shelter.db
set DATABASE_URL=postgresql+psycopg://postgres:password@localhost:5432/flood_shelter
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

The app now also tracks simple dataset metadata in `app_metadata` so the UI can distinguish demo data from imported data.

The backend model layer is now scaffolded for the next production entities:

- `users`
- `shelter_status`
- `recommendation_logs`
- `alerts`
- `audit_logs`

These are defined as SQLAlchemy models and are intended to be created through migrations, not by `database.py`.

## PostgreSQL And Migrations

Install dependencies:

```bash
pip install -r requirements.txt
```

Point the app at PostgreSQL:

```bash
set DATABASE_URL=postgresql+psycopg://postgres:password@localhost:5432/flood_shelter
```

Initialize migrations once:

```bash
flask --app "flood_app:create_app" db init
```

Create and apply a migration:

```bash
flask --app "flood_app:create_app" db migrate -m "initial production schema"
flask --app "flood_app:create_app" db upgrade
```

## Replacing Demo Data

The default `database.py` seeds demo shelters such as `Shelter A` to `Shelter Z`. To replace them with a real dataset:

```bash
python import_shelters.py shelters_template.csv
```

Expected CSV columns:

- `name`
- `capacity`
- `available_beds`
- `distance`
- `accessibility`
- `elevation_level`
- `proximity_to_water`
- `medical_facility`
- `latitude`
- `longitude`

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
