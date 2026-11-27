# ml_engine.py
"""
POWERGRID ML Inference Engine Helper.
Loads the trained multi-output XGBoost pipeline and StandardScaler to predict material quantities.
"""

import os
import joblib
import pandas as pd
from material_index_map import MATERIAL_INDEX_TO_NAME

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(CURRENT_DIR, "Balanced_Material_Model.pkl")
SCALER_PATH = os.path.join(CURRENT_DIR, "Balanced_YScaler.pkl")

_model = None
_scaler = None


def get_model():
    """Lazily load and cache the ML model and scaler."""
    global _model, _scaler
    if _model is None:
        if os.path.exists(MODEL_PATH) and os.path.exists(SCALER_PATH):
            _model = joblib.load(MODEL_PATH)
            _scaler = joblib.load(SCALER_PATH)
        else:
            raise FileNotFoundError(
                f"Model or Scaler file missing. Looked in {MODEL_PATH} and {SCALER_PATH}"
            )
    return _model, _scaler


def predict_material_demands(
    category: str,
    project_type: str,
    budget_lakh: float,
    state: str,
    terrain: str,
    distance_from_storage: float,
    line_length_km: float,
):
    """
    Run multi-target regression inference across 132 materials.
    Returns list of dicts with material_name and predicted_value.
    """
    model, scaler = get_model()

    df = pd.DataFrame([{
        "project_category_main": category,
        "project_type": project_type,
        "project_budget_price_in_lake": budget_lakh,
        "state": state,
        "terrain": terrain,
        "Distance_from_Storage_unit": distance_from_storage,
        "transmission_line_length_km": line_length_km,
    }])

    scaled_preds = model.predict(df)
    final_preds = scaler.inverse_transform(scaled_preds)[0]

    return [
        {
            "material_name": MATERIAL_INDEX_TO_NAME.get(i, f"material_{i}"),
            "predicted_value": max(0.0, float(val))
        }
        for i, val in enumerate(final_preds)
    ]
