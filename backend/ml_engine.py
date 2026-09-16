import os
import io
import pickle
import numpy as np
import torch
import torch.nn as nn
from PIL import Image
from torchvision import transforms, models
from backend.config import STAGE_B_MODEL_PATH, STAGE_A_MODEL_PATH, CLASSES

GROWTH_STAGE_MAP = {
    "Seedling": 0,
    "Vegetative": 1,
    "Flowering": 2,
    "Fruiting": 3
}

class MLInferenceEngine:
    def __init__(self):
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.classes = CLASSES
        self.stage_b_model = None
        self.stage_a_model = None
        self.load_models()

        self.transform = transforms.Compose([
            transforms.Resize((224, 224)),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
        ])

    def load_models(self):
        # Load Stage B PyTorch CNN
        if os.path.exists(STAGE_B_MODEL_PATH):
            print(f"Loading Stage B CNN weights from {STAGE_B_MODEL_PATH}...")
            checkpoint = torch.load(STAGE_B_MODEL_PATH, map_location=self.device)
            self.classes = checkpoint.get('classes', CLASSES)
            
            model = models.mobilenet_v3_small(weights=None, num_classes=len(self.classes))
            model.load_state_dict(checkpoint['model_state_dict'])
            model.to(self.device)
            model.eval()
            self.stage_b_model = model
            print("Stage B PyTorch CNN loaded successfully!")
        else:
            print("WARNING: Stage B CNN weights not found. Run ml/train_stage_b.py first!")

        # Load Stage A Risk Model
        if os.path.exists(STAGE_A_MODEL_PATH):
            print(f"Loading Stage A Risk model from {STAGE_A_MODEL_PATH}...")
            with open(STAGE_A_MODEL_PATH, 'rb') as f:
                self.stage_a_model = pickle.load(f)
            print("Stage A Risk model loaded successfully!")
        else:
            print("WARNING: Stage A model pickle not found.")

    def predict_stage_a_risk(self, crop_type, growth_stage, temperature, humidity, rainfall_mm, leaf_wetness_hours):
        """Calculates Stage A pre-symptomatic epidemiological risk using Van der Plank logic."""
        stage_idx = GROWTH_STAGE_MAP.get(growth_stage, 2)
        
        # ML Model prediction if available
        if self.stage_a_model:
            import pandas as pd
            features_df = pd.DataFrame([{
                'temperature': temperature,
                'relative_humidity': humidity,
                'rainfall_mm': rainfall_mm,
                'leaf_wetness_hours': leaf_wetness_hours,
                'growth_stage_idx': stage_idx
            }])
            pred_class = int(self.stage_a_model.predict(features_df)[0])
            probs = self.stage_a_model.predict_proba(features_df)[0]
            raw_risk_pct = float(probs[2] * 100.0 + probs[1] * 50.0)
        else:
            raw_risk_pct = 50.0

        # Epidemiological Van der Plank Disease Triangle Rule Calculation
        # Temperature favorability (optimal 18-26 C)
        temp_factor = max(0.0, 1.0 - abs(temperature - 22.0) / 18.0)
        # Humidity favorability (> 80% high risk)
        rh_factor = max(0.0, (humidity - 50.0) / 50.0)
        # Leaf wetness duration (> 10h high risk)
        lw_factor = min(1.0, leaf_wetness_hours / 14.0)
        # Vulnerability multiplier
        vuln = 1.2 if growth_stage in ["Flowering", "Fruiting"] else 0.9

        calculated_risk = min(99.0, max(5.0, (0.4 * rh_factor + 0.4 * lw_factor + 0.2 * temp_factor) * 100.0 * vuln))
        final_risk_score = round((raw_risk_pct * 0.4 + calculated_risk * 0.6), 1)

        if final_risk_score >= 70.0:
            alert_level = "HIGH"
        elif final_risk_score >= 40.0:
            alert_level = "MODERATE"
        else:
            alert_level = "LOW"

        # Determine primary potential threat
        if crop_type == "Tomato":
            threat = "Tomato Late Blight" if humidity > 85 and temperature < 23 else "Tomato Early Blight"
        elif crop_type == "Potato":
            threat = "Potato Early Blight"
        elif crop_type in ["Corn", "Corn/Maize", "Maize"]:
            threat = "Corn Common Rust"
        else:
            threat = "General Fungal Leaf Spot"

        reasoning = (
            f"High relative humidity ({humidity}%), prolonged leaf wetness ({leaf_wetness_hours}h), "
            f"and moderate temperatures ({temperature}°C) during vulnerable {growth_stage} stage create "
            f"ideal spore germination conditions according to Van der Plank epidemiological disease-triangle model."
        )

        return {
            "crop_type": crop_type,
            "growth_stage": growth_stage,
            "stage_a_risk_score": final_risk_score,
            "alert_level": alert_level,
            "primary_threat": threat,
            "reasoning": reasoning,
            "microclimate": {
                "temperature": temperature,
                "humidity": humidity,
                "rainfall_mm": rainfall_mm,
                "leaf_wetness_hours": leaf_wetness_hours
            }
        }

    def compute_leaf_severity(self, pil_image):
        """Estimates % leaf area affected using HSV color space segmentation."""
        img_np = np.array(pil_image.resize((224, 224)))
        
        # Convert RGB to HSV
        # Green leaf range in HSV (approx)
        r, g, b = img_np[:, :, 0], img_np[:, :, 1], img_np[:, :, 2]
        
        # Simple heuristic color segmentation for necrotic/rust/brown lesions
        # Non-green / brownish pixels
        is_green = (g > r) & (g > b) & (g > 60)
        is_brown_lesion = (r > g) | ((r > 120) & (g > 100) & (b < 80)) | ((r < 80) & (g < 60) & (b < 60))
        
        leaf_mask = is_green | is_brown_lesion
        total_leaf_pixels = np.sum(leaf_mask)
        if total_leaf_pixels == 0:
            total_leaf_pixels = 224 * 224

        lesion_pixels = np.sum(is_brown_lesion & leaf_mask)
        severity_pct = round(float((lesion_pixels / total_leaf_pixels) * 100.0), 1)

        if severity_pct < 1.0:
            severity_pct = 0.0
            grade = "Healthy / Minimal (<1%)"
        elif severity_pct < 15.0:
            grade = "Mild (<15% area infected)"
        elif severity_pct < 40.0:
            grade = "Moderate (15-40% area infected)"
        else:
            grade = "Severe (>40% area infected)"

        return severity_pct, grade

    def predict_stage_b_image(self, image_bytes):
        """Predicts disease class and confidence from uploaded leaf image."""
        if not self.stage_b_model:
            raise RuntimeError("Stage B model is not initialized!")

        pil_img = Image.open(io.BytesIO(image_bytes)).convert("RGB")
        input_tensor = self.transform(pil_img).unsqueeze(0).to(self.device)

        with torch.no_grad():
            outputs = self.stage_b_model(input_tensor)
            probabilities = torch.softmax(outputs, dim=1)[0].cpu().numpy()

        top_idx = int(np.argmax(probabilities))
        predicted_class = self.classes[top_idx]
        confidence_pct = round(float(probabilities[top_idx] * 100.0), 1)

        all_probs = {self.classes[i]: round(float(probabilities[i] * 100.0), 1) for i in range(len(self.classes))}
        
        # Calculate visual severity %
        severity_pct, severity_grade = self.compute_leaf_severity(pil_img)

        # If healthy predicted, zero severity
        if predicted_class == "Healthy_Leaf":
            severity_pct = 0.0
            severity_grade = "Healthy Foliage (0% lesion area)"

        return {
            "predicted_class": predicted_class,
            "confidence_pct": confidence_pct,
            "severity_pct": severity_pct,
            "severity_grade": severity_grade,
            "class_probabilities": all_probs
        }

    def fuse_stage_a_and_b(self, stage_a_res, stage_b_res):
        """Combines Stage A risk score and Stage B CNN confidence into unified diagnostic report."""
        risk_a = stage_a_res["stage_a_risk_score"]
        conf_b = stage_b_res["confidence_pct"]
        pred_b = stage_b_res["predicted_class"]

        # Weighted fusion score: 65% Image CNN confidence + 35% Pre-symptomatic weather risk score
        fusion_conf = round(0.65 * conf_b + 0.35 * risk_a, 1)

        explanation = (
            f"Stage-A Pre-Symptomatic Weather Risk ({risk_a}%) combined with Stage-B Image Vision Confidence "
            f"({conf_b}%) yields a weighted diagnostic confidence of {fusion_conf}%. "
            f"Detected visual features: {stage_b_res['severity_grade']} with key spot patterns matching {pred_b.replace('_', ' ')}."
        )

        return {
            "disease_id": pred_b,
            "disease_name": pred_b.replace('_', ' '),
            "fusion_confidence_pct": fusion_conf,
            "stage_a_risk_pct": risk_a,
            "stage_b_confidence_pct": conf_b,
            "severity_pct": stage_b_res["severity_pct"],
            "severity_grade": stage_b_res["severity_grade"],
            "confidence_weighted_explanation": explanation,
            "proactive_warning_pushed": risk_a >= 70.0
        }

# Global singleton instance
engine = MLInferenceEngine()
