# ⚡ POWERGRID Material Demand Forecasting System (SIH)

An AI/ML-powered forecasting and planning application developed for **Smart India Hackathon (SIH)** to predict transmission line material and equipment requirements for **POWERGRID** infrastructure projects.

---

## 📌 Project Overview

This platform uses a multi-output machine learning regression pipeline to forecast the exact quantities of **132+ materials and equipment** needed for transmission projects based on key project parameters (voltage rating, terrain type, line length, budget, distance from storage unit, state/location, and project category).

### 🛠️ Architecture & Tech Stack

- **Backend**:
  - **FastAPI**: High-performance asynchronous REST API framework
  - **Machine Learning**: `scikit-learn` Pipeline with custom scaling (`Balanced_Material_Model.pkl` & `Balanced_YScaler.pkl`) predicting 132 unique items (steel, conductors, insulators, transformers, switchgear, hardware fittings, etc.)
  - **Database**: SQLite (`sih.db`) with SQLAlchemy ORM models for Users, Projects, Materials, and Forecast history
  - **Pydantic**: Strict data schema validation
- **Frontend**:
  - Interactive Single-Page Dashboard built with Tailwind CSS, Chart.js, and jsPDF
  - Project management, inventory tracking, live forecasting, and PDF export capabilities

---

## 📂 Repository Structure

```text
SIH-R/
├── README.md                  # Project documentation
├── start.sh                   # One-click startup script for Linux/macOS
├── .gitignore                 # Standard Python & environment ignores
└── SIH_Powergrid/
    ├── backend/
    │   ├── app.py                      # FastAPI application entrypoint & CORS
    │   ├── database.py                 # SQLAlchemy SQLite database setup
    │   ├── models.py                   # ORM data models (User, Project, Forecast, etc.)
    │   ├── schemas.py                  # Pydantic schemas for request/response validation
    │   ├── ml_engine.py                # ML prediction helper engine
    │   ├── material_index_map.py       # Mapping of 132 material names to model indices
    │   ├── Balanced_Material_Model.pkl # Trained ML Pipeline model
    │   ├── Balanced_YScaler.pkl        # Output target scaler
    │   ├── requirements.txt            # Python dependencies
    │   ├── sih.db                      # SQLite database with initial seed data
    │   └── routes/
    │       ├── auth_routes.py          # User authentication (Login / Register)
    │       ├── project_routes.py       # Project creation & user project listing
    │       ├── material_routes.py      # Material catalog & CRUD operations
    │       ├── forecast.py             # ML prediction & forecast persistence endpoints
    │       └── prediction_routes.py    # Historical prediction logs
    └── frontend/
        ├── index.html                  # Main interactive dashboard UI
        ├── index_Gemini_changes.html   # Updated dashboard variant
        └── index_old.html              # Baseline UI backup
```

---

## 🚀 Getting Started & Local Execution

### 1. Prerequisites
- Python 3.10+
- `pip` package manager

### 2. Option A: Quickstart (Recommended)
Make `start.sh` executable and run it:
```bash
chmod +x start.sh
./start.sh
```
This automatically starts:
- **Backend API**: `http://127.0.0.1:8000`
- **Interactive API Docs (Swagger UI)**: `http://127.0.0.1:8000/docs`
- **Frontend Application**: `http://127.0.0.1:3000/index.html`

---

### 3. Option B: Manual Setup

#### Run Backend
```bash
cd SIH_Powergrid/backend
pip install -r requirements.txt
python3 -m uvicorn app:app --host 127.0.0.1 --port 8000 --reload
```

#### Run Frontend
In a new terminal window:
```bash
cd SIH_Powergrid/frontend
python3 -m http.server 3000
```
Open your browser and navigate to:
👉 **`http://127.0.0.1:3000/index.html`**

---

## 📡 Key API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/` | Health check |
| `POST` | `/forecast/predict` | Generate instant ML material quantity predictions without saving |
| `POST` | `/forecast/save` | Generate predictions and save project forecast to SQLite database |
| `GET` | `/projects/user/{user_id}` | Fetch all projects associated with a user |
| `POST` | `/projects/create` | Create a new transmission line project |
| `POST` | `/auth/login` | User authentication |
| `POST` | `/auth/register` | New user registration |
| `GET` | `/docs` | Interactive Swagger UI API documentation |
