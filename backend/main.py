import os
import json
import sqlite3
from typing import Optional
from fastapi import FastAPI, File, UploadFile, Form, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from backend.config import CLASSES, DB_PATH
from backend.database import get_db, init_db
from backend.ml_engine import engine

app = FastAPI(
    title="CropGuard AI Backend API",
    description="Early Crop Disease and Pest Detection & Advisory System for Indian Farmers",
    version="1.0.0"
)

# Enable CORS for React Vite frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def startup_event():
    init_db()
    print("CropGuard AI FastAPI Backend successfully started!")

# Request Models
class RiskPredictRequest(BaseModel):
    crop_type: str = "Tomato"
    growth_stage: str = "Flowering"
    district: str = "Nashik"
    temperature: float = 21.5
    humidity: float = 88.0
    rainfall_mm: float = 12.0
    leaf_wetness_hours: float = 11.5

@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "system": "CropGuard AI",
        "stage_a_ready": engine.stage_a_model is not None,
        "stage_b_ready": engine.stage_b_model is not None,
        "supported_classes": CLASSES
    }

@app.post("/predict-risk")
def predict_risk(req: RiskPredictRequest):
    """Stage A: Pre-symptomatic outbreak risk prediction based on microclimate & Van der Plank disease triangle."""
    risk_res = engine.predict_stage_a_risk(
        crop_type=req.crop_type,
        growth_stage=req.growth_stage,
        temperature=req.temperature,
        humidity=req.humidity,
        rainfall_mm=req.rainfall_mm,
        leaf_wetness_hours=req.leaf_wetness_hours
    )
    risk_res["district"] = req.district
    return risk_res

@app.get("/recommend/{disease_id}")
def get_recommendation(disease_id: str):
    """Fetches ICAR/KVK advisory treatment for a specific disease ID."""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM advisories WHERE id = ?", (disease_id,))
    row = cursor.fetchone()
    conn.close()

    if not row:
        # Fallback to healthy or general advisory
        return {
            "id": disease_id,
            "crop_type": "General",
            "disease_name": disease_id.replace("_", " "),
            "scientific_name": "N/A",
            "organic_treatment": "Apply Neem Oil (5ml/L) and remove infected leaves.",
            "chemical_treatment": "Consult local KVK for recommended foliar spray.",
            "key_visual_features": "Foliage discoloration or spot lesions.",
            "disclaimer": "Consult local agriculture extension officer for exact dosage."
        }

    return dict(row)

@app.post("/diagnose")
async def diagnose_leaf(
    file: UploadFile = File(...),
    crop_type: str = Form("Tomato"),
    growth_stage: str = Form("Flowering"),
    district: str = Form("Nashik"),
    state: str = Form("Maharashtra"),
    temperature: float = Form(21.5),
    humidity: float = Form(88.0),
    rainfall_mm: float = Form(12.0),
    leaf_wetness_hours: float = Form(11.5)
):
    """Full Pipeline: Stage A risk + Stage B CNN diagnosis + Severity Grading + Fusion + Treatment Lookup."""
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Uploaded file must be a valid image.")

    image_bytes = await file.read()

    # 1. Run Stage A Risk Engine
    stage_a_res = engine.predict_stage_a_risk(
        crop_type=crop_type,
        growth_stage=growth_stage,
        temperature=temperature,
        humidity=humidity,
        rainfall_mm=rainfall_mm,
        leaf_wetness_hours=leaf_wetness_hours
    )

    # 2. Run Stage B Image CNN Classification & Severity
    try:
        stage_b_res = engine.predict_stage_b_image(image_bytes)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Image inference failed: {str(e)}")

    # 3. Run Fusion Engine
    fusion_res = engine.fuse_stage_a_and_b(stage_a_res, stage_b_res)

    # 4. Fetch Treatment Advisory
    advisory = get_recommendation(fusion_res["disease_id"])

    # 5. Log Diagnosis to SQLite Database
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO farmer_diagnoses (
            district_name, state, crop_type, disease_predicted, severity_pct,
            stage_a_risk, stage_b_confidence, fusion_confidence, created_at
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, datetime('now'))
    ''', (
        district, state, crop_type, fusion_res["disease_id"],
        fusion_res["severity_pct"], stage_a_res["stage_a_risk_score"],
        stage_b_res["confidence_pct"], fusion_res["fusion_confidence_pct"]
    ))
    conn.commit()
    conn.close()

    return {
        "crop_type": crop_type,
        "district": district,
        "state": state,
        "stage_a": stage_a_res,
        "stage_b": stage_b_res,
        "fusion": fusion_res,
        "treatment_advisory": advisory
    }

@app.get("/dashboard-data")
def get_dashboard_data(
    crop_filter: Optional[str] = Query(None),
    alert_filter: Optional[str] = Query(None)
):
    """Extension Officer Dashboard: Regional outbreak heatmaps, cluster stats, and case logs."""
    conn = get_db()
    cursor = conn.cursor()

    # Query district outbreak risks
    query_dist = "SELECT * FROM district_risks"
    params = []
    if alert_filter and alert_filter != "ALL":
        query_dist += " WHERE alert_level = ?"
        params.append(alert_filter)
    cursor.execute(query_dist, params)
    district_rows = [dict(row) for row in cursor.fetchall()]

    # Query recent farmer diagnoses
    cursor.execute("SELECT * FROM farmer_diagnoses ORDER BY id DESC LIMIT 20")
    diagnoses_rows = [dict(row) for row in cursor.fetchall()]

    conn.close()

    # Aggregate cluster statistics
    total_districts = len(district_rows)
    high_risk_count = sum(1 for d in district_rows if d["alert_level"] == "HIGH")
    mod_risk_count = sum(1 for d in district_rows if d["alert_level"] == "MODERATE")
    low_risk_count = sum(1 for d in district_rows if d["alert_level"] == "LOW")

    return {
        "summary": {
            "total_districts_monitored": total_districts,
            "high_risk_clusters": high_risk_count,
            "moderate_risk_clusters": mod_risk_count,
            "low_risk_clusters": low_risk_count,
            "total_farmer_reports": len(diagnoses_rows)
        },
        "district_heatmap": district_rows,
        "recent_diagnoses": diagnoses_rows
    }
