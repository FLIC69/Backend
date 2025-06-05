from fastapi import APIRouter, HTTPException
from app.db import DB
from typing import List
from pydantic import BaseModel
import requests
import os

router = APIRouter()

class PredictInput(BaseModel):
    features: List[float]
    model: str

@router.get("/")
def home():
    return "AI Home"

@router.post("/predict")
def predict(data: PredictInput):
    ai_url = os.getenv("MODEL_URL")
    print(ai_url)
    if not ai_url:
        raise HTTPException(status_code=500, detail="MODEL_URL environment variable not set")
    
    try:
        response = requests.post(ai_url, json=data.model_dump())
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=502, detail=f"Error communicating with model server: {e}")
    
    try:
        prediction = response.json()
    except ValueError:
        raise HTTPException(status_code=502, detail="Invalid response from model server (not JSON)")

    return {"prediction": prediction}

