import os
import sys
import json
import requests
from PIL import Image

# Ensure PYTHONPATH includes root
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi.testclient import TestClient
from backend.main import app
from backend.config import SAMPLE_LEAVES_DIR

def run_backend_tests():
    print("=== Running CropGuard AI Backend Automated Endpoint Verification ===")
    client = TestClient(app)

    # Test 1: Health Check
    print("\n[TEST 1] GET /health ...")
    res = client.get("/health")
    assert res.status_code == 200, f"Health check failed: {res.text}"
    print(f"Health Response: {res.json()}")

    # Test 2: Predict Risk (Stage A Weather Scenarios)
    print("\n[TEST 2] POST /predict-risk (Scenario 1: High Blight Risk Weather) ...")
    high_risk_payload = {
        "crop_type": "Tomato",
        "growth_stage": "Flowering",
        "district": "Nashik",
        "temperature": 20.0,
        "humidity": 92.0,
        "rainfall_mm": 20.0,
        "leaf_wetness_hours": 14.0
    }
    res = client.post("/predict-risk", json=high_risk_payload)
    assert res.status_code == 200, f"Risk prediction failed: {res.text}"
    risk_data = res.json()
    print(f"High Risk Output: Score={risk_data['stage_a_risk_score']}%, Level={risk_data['alert_level']}, Threat={risk_data['primary_threat']}")
    assert risk_data["alert_level"] == "HIGH", f"Expected HIGH alert level, got {risk_data['alert_level']}"

    print("\n[TEST 2b] POST /predict-risk (Scenario 2: Low Risk Weather) ...")
    low_risk_payload = {
        "crop_type": "Tomato",
        "growth_stage": "Seedling",
        "district": "Guntur",
        "temperature": 34.0,
        "humidity": 45.0,
        "rainfall_mm": 0.0,
        "leaf_wetness_hours": 2.0
    }
    res = client.post("/predict-risk", json=low_risk_payload)
    assert res.status_code == 200
    risk_data_low = res.json()
    print(f"Low Risk Output: Score={risk_data_low['stage_a_risk_score']}%, Level={risk_data_low['alert_level']}")
    assert risk_data_low["alert_level"] == "LOW", f"Expected LOW alert level, got {risk_data_low['alert_level']}"

    # Test 3: Diagnose Image Uploads (Stage B + Severity + Fusion)
    sample_files = [
        "test_leaf_tomato_early_blight.jpg",
        "test_leaf_tomato_late_blight.jpg",
        "test_leaf_corn_rust.jpg",
        "test_leaf_healthy.jpg"
    ]

    print("\n[TEST 3] POST /diagnose (Testing 4 sample leaf images) ...")
    for sample_file in sample_files:
        img_path = os.path.join(SAMPLE_LEAVES_DIR, sample_file)
        assert os.path.exists(img_path), f"Sample image file missing: {img_path}"

        with open(img_path, "rb") as f:
            files = {"file": (sample_file, f, "image/jpeg")}
            data = {
                "crop_type": "Tomato" if "tomato" in sample_file else ("Corn/Maize" if "corn" in sample_file else "Potato"),
                "growth_stage": "Flowering",
                "district": "Nashik",
                "state": "Maharashtra",
                "temperature": 21.0,
                "humidity": 88.0,
                "rainfall_mm": 15.0,
                "leaf_wetness_hours": 12.0
            }
            res = client.post("/diagnose", files=files, data=data)
            assert res.status_code == 200, f"Diagnose endpoint failed for {sample_file}: {res.text}"
            diag_payload = res.json()

            disease_name = diag_payload["fusion"]["disease_name"]
            fusion_conf = diag_payload["fusion"]["fusion_confidence_pct"]
            severity_pct = diag_payload["fusion"]["severity_pct"]
            organic_rx = diag_payload["treatment_advisory"]["organic_treatment"][:40]

            print(f"  -> File: {sample_file} => Predicted: '{disease_name}' | Fusion Conf: {fusion_conf}% | Severity: {severity_pct}% | Rx: '{organic_rx}...'")

    # Test 4: Admin Dashboard Data
    print("\n[TEST 4] GET /dashboard-data ...")
    res = client.get("/dashboard-data")
    assert res.status_code == 200
    dash_data = res.json()
    print(f"Dashboard Summary: Monitored Districts={dash_data['summary']['total_districts_monitored']}, High Risk Clusters={dash_data['summary']['high_risk_clusters']}")
    assert len(dash_data["district_heatmap"]) >= 10, "Expected at least 10 district heatmap records"

    print("\n=== ALL BACKEND ENDPOINTS PASSED VERIFICATION SUCCESSFULLY! ===")

if __name__ == "__main__":
    run_backend_tests()
