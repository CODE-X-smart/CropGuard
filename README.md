# CropGuard AI: Early Crop Disease and Pest Detection & Advisory System

CropGuard AI is an early crop disease and pest detection and advisory system specifically built for Indian farmers. 

Unlike traditional reactive leaf diagnosis tools, CropGuard AI introduces a **Two-Stage "Predict-then-Detect" Pipeline**:
1. **Stage A (Pre-Symptomatic Outbreak Risk Prediction)**: Predicts disease outbreak probabilities *before visible symptoms appear* using epidemiological micro-climate models (Van der Plank disease triangle: temperature, relative humidity, rainfall, leaf wetness duration, growth stage, and regional vector density).
2. **Stage B (Image-Based Confirmation & Severity Grading)**: On-device/lightweight PyTorch MobileNetV3 CNN classifies leaf diseases and calculates `% leaf area infected` (lesion severity) using HSV color space segmentation.
3. **Fusion Layer**: Synthesizes Stage A epidemiological risk with Stage B visual confidence into a confidence-weighted actionable advisory with paraphrased ICAR (Indian Council of Agricultural Research) treatment guidelines.

---

## Technical Architecture

```
d:\ANTIGRAVITY\document (sih)\
├── RESEARCH.md                   # Citation-backed research & dataset analysis
├── LIMITATIONS.md                # Technical boundaries & prototype disclosures
├── README.md                     # Runnable setup instructions & verification guide
├── backend/                      # FastAPI REST Service & SQLite Database
│   ├── main.py                   # REST API routes & CORS setup
│   ├── ml_engine.py              # PyTorch MobileNetV3 & Stage A risk calculation
│   ├── database.py               # SQLite schema (cropguard.db)
│   ├── data_fixtures.py          # ICAR advisory & district outbreak data seeds
│   ├── config.py                 # System configuration
│   └── test_backend.py           # Automated backend API test suite
├── ml/                           # Machine Learning Training & Datasets
│   ├── generate_dataset.py       # Synthetic plant leaf dataset generator
│   ├── train_stage_b.py          # PyTorch CNN training script
│   ├── train_stage_a.py          # Stage A weather risk model training script
│   ├── cropguard_mobilenetv3.pth # Saved PyTorch model checkpoint
│   ├── stage_a_risk_model.pkl    # Saved scikit-learn Stage A model
│   └── sample_leaves/            # Test images for API verification
└── frontend/                     # React + Vite + Tailwind CSS Application
    ├── src/
    │   ├── App.jsx               # App container & navigation tabs
    │   ├── i18n/translations.js  # English & Hindi (hi) translation dictionary
    │   ├── api/client.js         # Axios API client
    │   └── components/           # StageAAlertBanner, ImageDiagnosisCard, FusionResultCard, etc.
```

---

## Getting Started & Execution Instructions

### Prerequisites
- **Python**: Python 3.10+ (Anaconda / Virtualenv)
- **Node.js**: Node.js v18+ and `npm`

---

### Step 1: Backend & ML Setup

1. **Generate Dataset & Sample Test Images**:
   ```bash
   python ml/generate_dataset.py
   ```
   *Generates 300 leaf images across 5 classes (`Tomato_Early_Blight`, `Tomato_Late_Blight`, `Potato_Early_Blight`, `Corn_Common_Rust`, `Healthy_Leaf`) and 4 sample test images in `ml/sample_leaves/`.*

2. **Train Stage A & Stage B Machine Learning Models**:
   ```bash
   python ml/train_stage_a.py
   python ml/train_stage_b.py
   ```
   *Trains the PyTorch MobileNetV3 CNN model and scikit-learn risk predictor, saving weights to `ml/cropguard_mobilenetv3.pth` and `ml/stage_a_risk_model.pkl`.*

3. **Initialize & Seed SQLite Database**:
   ```bash
   python backend/data_fixtures.py
   ```
   *Seeds `backend/cropguard.db` with ICAR treatment advisories and 10 Indian district outbreak risk records (Nashik, Karnal, Ludhiana, Anand, Guntur, Shimla, etc.).*

4. **Run Automated Backend Verification Test Suite**:
   ```bash
   python backend/test_backend.py
   ```
   *Executes test suite asserting responses from `/health`, `/predict-risk`, `/diagnose`, and `/dashboard-data`.*

5. **Start FastAPI Backend Server**:
   ```bash
   python -m uvicorn backend.main:app --reload --port 8000
   ```
   *API will be live at `http://127.0.0.1:8000`. Swagger API docs available at `http://127.0.0.1:8000/docs`.*

---

### Step 2: Frontend Setup

1. **Install Dependencies & Build Bundle**:
   ```bash
   cd frontend
   npm install
   npm run build
   ```

2. **Run Vite Development Server**:
   ```bash
   npm run dev
   ```
   *App accessible at `http://localhost:5173`.*

---

## Core REST API Endpoints

- `GET /health`: Health check and loaded ML model status.
- `POST /predict-risk`: Stage A pre-symptomatic weather & epidemiological risk calculation.
- `POST /diagnose`: Full diagnosis pipeline (Leaf image upload + crop type + district -> Stage B CNN inference + Severity % + Fusion + ICAR treatment).
- `GET /recommend/{disease_id}`: Retrieves organic & chemical treatment options for a disease.
- `GET /dashboard-data`: Extension Officer Dashboard payload (district risk heatmaps, cluster counts, recent farmer diagnoses).

---

## Verification & Deliverables Checklist

- [x] **`RESEARCH.md`**: Grounding document with cited findings on MobileNetV3, PlantVillage/PlantDoc domain shift, and Van der Plank disease triangle models.
- [x] **`LIMITATIONS.md`**: Transparent disclosures regarding dataset scale (5 classes), Stage A POC scope, and absence of live government APIs.
- [x] **Trained PyTorch Model**: MobileNetV3 model trained with saved metrics (`ml/training_metrics.json`).
- [x] **Verified `/diagnose` Endpoint**: Tested with 4 sample leaf images.
- [x] **Verified `/predict-risk` Endpoint**: Tested with high-risk and low-risk microclimate weather scenarios.
- [x] **Mobile-Responsive Frontend**: React + Vite UI with English/Hindi (`en`/`hi`) translation toggle.
- [x] **Admin Dashboard**: Heatmap grid and cluster counts across 10 monitored districts.
