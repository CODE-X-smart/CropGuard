import os
import pickle
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report

MODEL_SAVE_PATH = os.path.join(os.path.dirname(__file__), "stage_a_risk_model.pkl")

def generate_synthetic_weather_dataset(n_samples=1000):
    """Generates synthetic micro-climate epidemiological dataset."""
    np.random.seed(42)
    
    # Feature distributions based on Indian agricultural microclimates
    temps = np.random.uniform(10.0, 38.0, n_samples)          # °C
    rh = np.random.uniform(40.0, 98.0, n_samples)             # %
    rainfall = np.random.exponential(scale=15.0, size=n_samples) # mm
    leaf_wetness = np.random.uniform(0.0, 24.0, n_samples)   # hours
    growth_stage = np.random.choice([0, 1, 2, 3], size=n_samples) # Seedling, Vegetative, Flowering, Fruiting

    risk_scores = []
    risk_classes = []

    for i in range(n_samples):
        t, h, r, lw, g = temps[i], rh[i], rainfall[i], leaf_wetness[i], growth_stage[i]
        
        # Van der Plank Disease Triangle Risk Formula:
        # Favorable temp (18-28 C) + High RH (>80%) + Long leaf wetness (>8h) + Vulnerable growth stage (Flowering/Fruiting)
        temp_score = 1.0 - abs(t - 22.0) / 20.0
        temp_score = max(0.0, min(1.0, temp_score))

        rh_score = max(0.0, (h - 50.0) / 50.0)
        lw_score = max(0.0, lw / 18.0)
        growth_multiplier = 1.0 if g in [2, 3] else 0.75 # Flowering & Fruiting higher susceptibility

        raw_risk = (0.35 * rh_score + 0.35 * lw_score + 0.20 * temp_score + 0.10 * min(1.0, r / 30.0)) * growth_multiplier
        risk_percentage = min(100.0, max(0.0, raw_risk * 100.0))

        if risk_percentage < 35.0:
            cls = 0 # Low
        elif risk_percentage < 70.0:
            cls = 1 # Moderate
        else:
            cls = 2 # High (Outbreak Warning)

        risk_scores.append(risk_percentage)
        risk_classes.append(cls)

    df = pd.DataFrame({
        'temperature': temps,
        'relative_humidity': rh,
        'rainfall_mm': rainfall,
        'leaf_wetness_hours': leaf_wetness,
        'growth_stage_idx': growth_stage,
        'risk_class': risk_classes,
        'risk_score': risk_scores
    })

    return df

def train_stage_a():
    print("=== Training Stage A Epidemiological Outbreak Risk Model ===")
    df = generate_synthetic_weather_dataset(1200)
    
    X = df[['temperature', 'relative_humidity', 'rainfall_mm', 'leaf_wetness_hours', 'growth_stage_idx']]
    y = df['risk_class']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model = RandomForestClassifier(n_estimators=50, max_depth=6, random_state=42)
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    print("\nStage A Model Classification Report:")
    print(classification_report(y_test, y_pred, target_names=['Low Risk', 'Moderate Risk', 'High Risk']))

    with open(MODEL_SAVE_PATH, 'wb') as f:
        pickle.dump(model, f)

    print(f"Stage A risk model successfully saved to: {MODEL_SAVE_PATH}")

if __name__ == "__main__":
    train_stage_a()
