# routes/forecast.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import Forecast
from schemas import (
    ForecastInput,
    ForecastResponse,
    MaterialPrediction,
    ForecastWithPredictions,
)
import joblib
import pandas as pd

from material_index_map import MATERIAL_INDEX_TO_NAME

router = APIRouter(prefix="/forecast", tags=["Forecast API"])


# -----------------------------------
# 🔥 Load Model + Scaler Once
# -----------------------------------
try:
    model = joblib.load("Balanced_Material_Model.pkl")
    y_scaler = joblib.load("Balanced_YScaler.pkl")
    print("✅ ML Model + Scaler Loaded")
except:
    model, y_scaler = None, None
    print("⚠️ MODEL LOAD FAILED — Check file paths")


INPUT_FEATURES = [
    "project_category_main",
    "project_type",
    "project_budget_price_in_lake",
    "state",
    "terrain",
    "Distance_from_Storage_unit",
    "transmission_line_length_km",
]


# ======================================================================================
# 1️⃣ PREDICT + SAVE to DATABASE (Your Existing Feature Improved)
# ======================================================================================
@router.post("/save", response_model=ForecastWithPredictions)
def save_forecast(body: ForecastInput, db: Session = Depends(get_db)):

    if model is None:
        raise HTTPException(500, "ML model not loaded")

    # -------------- SAVE INPUT TO DB --------------
    entry = Forecast(
        project_category_main=body.project_category_main,
        project_type=body.project_type,
        project_budget_price_in_lake=body.project_budget_price_in_lake,
        state=body.state,
        terrain=body.terrain,
        distance_from_storage_unit=body.Distance_from_Storage_unit,
        transmission_line_length_km=body.transmission_line_length_km,
        location=body.location,
        project_name=body.project_name,
    )

    db.add(entry)
    db.commit()
    db.refresh(entry)

    # -------------- PREPARE DATAFRAME FOR MODEL --------------
    X_df = pd.DataFrame([{
        "project_category_main": body.project_category_main,
        "project_type": body.project_type,
        "project_budget_price_in_lake": body.project_budget_price_in_lake,
        "state": body.state,
        "terrain": body.terrain,
        "Distance_from_Storage_unit": body.Distance_from_Storage_unit,
        "transmission_line_length_km": body.transmission_line_length_km,
    }])

    scaled_output = model.predict(X_df)
    final_pred = y_scaler.inverse_transform(scaled_output)[0]

    # -------------- MAP PREDICTIONS TO MATERIAL NAMES --------------
    predictions = [
        MaterialPrediction(
            material_name=MATERIAL_INDEX_TO_NAME.get(i, f"material_{i}"),
            predicted_value=float(v)
        )
        for i, v in enumerate(final_pred)
    ]

    print("\n📌 Forecast Saved → ID:", entry.id)
    print("██████ MODEL OUTPUT ██████")
    print(final_pred)

    return ForecastWithPredictions(forecast=entry, predictions=predictions)



# ======================================================================================
# 2️⃣ ONLY PREDICT (NO DATABASE SAVE) — For UI Instant Forecast ⚡
# ======================================================================================
@router.post("/predict", response_model=list[MaterialPrediction])
def predict_only(body: ForecastInput):

    if model is None:
        raise HTTPException(500, "ML model not loaded")

    X_df = pd.DataFrame([{
        "project_category_main": body.project_category_main,
        "project_type": body.project_type,
        "project_budget_price_in_lake": body.project_budget_price_in_lake,
        "state": body.state,
        "terrain": body.terrain,
        "Distance_from_Storage_unit": body.Distance_from_Storage_unit,
        "transmission_line_length_km": body.transmission_line_length_km,
    }])

    scaled_output = model.predict(X_df)
    final_pred = y_scaler.inverse_transform(scaled_output)[0]

    results = [
        MaterialPrediction(
            material_name=MATERIAL_INDEX_TO_NAME.get(i, f"material_{i}"),
            predicted_value=float(v)
        )
        for i, v in enumerate(final_pred)
    ]

    return results
