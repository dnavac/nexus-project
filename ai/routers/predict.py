from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import joblib
import numpy as np

router = APIRouter()

# Cargamos el modelo al iniciar (solo una vez en memoria)
model = joblib.load("lead_model.joblib")

class LeadScoreRequest(BaseModel):
    budget_millions: float      # Presupuesto en millones COP
    num_visits: int             # Visitas realizadas
    days_since_contact: int     # Días desde el primer contacto
    responds_fast: bool         # ¿Responde rápido?

@router.post("/lead-score")
async def predict_lead_score(request: LeadScoreRequest):
    try:
        features = np.array([[
            request.budget_millions,
            request.num_visits,
            request.days_since_contact,
            int(request.responds_fast)
        ]])

        probability = model.predict_proba(features)[0][1]  # Probabilidad de clase "compra"
        score = round(probability * 100, 2)

        return {
            "score": score,
            "label": "caliente" if score >= 70 else "tibio" if score >= 40 else "frío"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
