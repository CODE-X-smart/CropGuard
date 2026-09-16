import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ML_DIR = os.path.join(BASE_DIR, "ml")

STAGE_B_MODEL_PATH = os.path.join(ML_DIR, "cropguard_mobilenetv3.pth")
STAGE_A_MODEL_PATH = os.path.join(ML_DIR, "stage_a_risk_model.pkl")
DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "cropguard.db")
SAMPLE_LEAVES_DIR = os.path.join(ML_DIR, "sample_leaves")

CLASSES = [
    "Corn_Common_Rust",
    "Healthy_Leaf",
    "Potato_Early_Blight",
    "Tomato_Early_Blight",
    "Tomato_Late_Blight"
]
