from datetime import datetime
from backend.database import get_db, init_db

ICAR_ADVISORIES = [
    {
        "id": "Tomato_Early_Blight",
        "crop_type": "Tomato",
        "disease_name": "Tomato Early Blight",
        "scientific_name": "Alternaria solani",
        "organic_treatment": "Apply Neem oil (5ml/L water) or bio-fungicide Trichoderma viride (5g/L). Maintain proper plant spacing and destroy infected lower leaves.",
        "chemical_treatment": "Foliar spray of Mancozeb 75% WP @ 2.5g/L or Chlorothalonil 75% WP @ 2g/L at 10-14 day intervals upon early symptom appearance.",
        "key_visual_features": "Concentric target-like brown rings on older leaves, surrounded by yellow chlorotic halos.",
        "disclaimer": "Advisory based on ICAR-IARI Solanaceous crop guidelines. Consult your local Krishi Vigyan Kendra (KVK) officer for exact dosage and tank-mix calibration."
    },
    {
        "id": "Tomato_Late_Blight",
        "crop_type": "Tomato",
        "disease_name": "Tomato Late Blight",
        "scientific_name": "Phytophthora infestans",
        "organic_treatment": "Spray Copper Hydroxide (2.5g/L) or Panchagavya (3%). Ensure rapid field drainage and remove waterlogged crop residues immediately.",
        "chemical_treatment": "Systemic spray of Metalaxyl 8% + Mancozeb 64% WP (Ridomil Gold) @ 2g/L or Azoxystrobin 23% EC @ 1ml/L during humid high-risk weather.",
        "key_visual_features": "Irregular dark water-soaked lesions expanding rapidly from leaf tips, with white mold growth under high humidity.",
        "disclaimer": "Advisory based on ICAR-IARI Solanaceous crop guidelines. Consult your local Krishi Vigyan Kendra (KVK) officer for exact dosage and tank-mix calibration."
    },
    {
        "id": "Potato_Early_Blight",
        "crop_type": "Potato",
        "disease_name": "Potato Early Blight",
        "scientific_name": "Alternaria solani",
        "organic_treatment": "Bio-control with Pseudomonas fluorescens @ 10g/L spray. Implement 3-year crop rotation with non-solanaceous crops.",
        "chemical_treatment": "Spray Propineb 70% WP @ 2g/L or Difenoconazole 25% EC @ 0.5ml/L at first sign of circular target spots.",
        "key_visual_features": "Small brown angular necrotic spots with target-like concentric rings on potato foliage.",
        "disclaimer": "Advisory based on ICAR-CPRI (Central Potato Research Institute) guidelines. Consult local district agriculture extension officer."
    },
    {
        "id": "Corn_Common_Rust",
        "crop_type": "Corn/Maize",
        "disease_name": "Corn Common Rust",
        "scientific_name": "Puccinia sorghi",
        "organic_treatment": "Dusting with fine sulfur powder (15kg/ha) or spraying Garlic bulb extract (5%). Plant resistant maize hybrid varieties.",
        "chemical_treatment": "Spray Mancozeb 75% WP @ 2.5g/L or Tebuconazole 25.9% EC @ 1ml/L at 14-day intervals during warm humid weather.",
        "key_visual_features": "Small elongated golden-brown to reddish-orange raised pustules scattered across both leaf surfaces.",
        "disclaimer": "Advisory based on ICAR-IIMR (Indian Institute of Maize Research) advisories. Confirm dosage with local extension agents."
    },
    {
        "id": "Healthy_Leaf",
        "crop_type": "General",
        "disease_name": "Healthy Foliage",
        "scientific_name": "N/A",
        "organic_treatment": "No disease symptoms detected. Continue routine organic soil enrichment with Farm Yard Manure (FYM) and bio-fertilizers.",
        "chemical_treatment": "No chemical treatment needed. Maintain optimal balanced N-P-K fertilization and irrigation scheduling.",
        "key_visual_features": "Uniform vibrant green leaf color, intact cuticle structure, no necrotic spots or pustules.",
        "disclaimer": "Routine agronomic maintenance recommended."
    }
]

DISTRICT_MOCK_DATA = [
    {
        "district_name": "Nashik",
        "state": "Maharashtra",
        "crop_type": "Tomato",
        "risk_score": 82.5,
        "primary_threat": "Tomato Late Blight",
        "temperature": 19.5,
        "humidity": 89.0,
        "rainfall_mm": 18.5,
        "leaf_wetness_hours": 13.0,
        "alert_level": "HIGH"
    },
    {
        "district_name": "Karnal",
        "state": "Haryana",
        "crop_type": "Tomato",
        "risk_score": 68.0,
        "primary_threat": "Tomato Early Blight",
        "temperature": 24.2,
        "humidity": 78.5,
        "rainfall_mm": 8.0,
        "leaf_wetness_hours": 9.5,
        "alert_level": "MODERATE"
    },
    {
        "district_name": "Ludhiana",
        "state": "Punjab",
        "crop_type": "Potato",
        "risk_score": 76.0,
        "primary_threat": "Potato Early Blight",
        "temperature": 23.0,
        "humidity": 82.0,
        "rainfall_mm": 12.0,
        "leaf_wetness_hours": 11.0,
        "alert_level": "HIGH"
    },
    {
        "district_name": "Anand",
        "state": "Gujarat",
        "crop_type": "Corn/Maize",
        "risk_score": 71.5,
        "primary_threat": "Corn Common Rust",
        "temperature": 21.0,
        "humidity": 91.0,
        "rainfall_mm": 15.0,
        "leaf_wetness_hours": 12.5,
        "alert_level": "HIGH"
    },
    {
        "district_name": "Guntur",
        "state": "Andhra Pradesh",
        "crop_type": "Tomato",
        "risk_score": 28.0,
        "primary_threat": "None (Low Risk)",
        "temperature": 32.5,
        "humidity": 55.0,
        "rainfall_mm": 0.0,
        "leaf_wetness_hours": 3.0,
        "alert_level": "LOW"
    },
    {
        "district_name": "Shimla",
        "state": "Himachal Pradesh",
        "crop_type": "Potato",
        "risk_score": 88.0,
        "primary_threat": "Potato Early Blight",
        "temperature": 16.5,
        "humidity": 93.0,
        "rainfall_mm": 22.0,
        "leaf_wetness_hours": 14.5,
        "alert_level": "HIGH"
    },
    {
        "district_name": "Varanasi",
        "state": "Uttar Pradesh",
        "crop_type": "Tomato",
        "risk_score": 54.0,
        "primary_threat": "Tomato Early Blight",
        "temperature": 26.0,
        "humidity": 72.0,
        "rainfall_mm": 4.5,
        "leaf_wetness_hours": 7.0,
        "alert_level": "MODERATE"
    },
    {
        "district_name": "Pune",
        "state": "Maharashtra",
        "crop_type": "Tomato",
        "risk_score": 79.0,
        "primary_threat": "Tomato Late Blight",
        "temperature": 20.1,
        "humidity": 87.5,
        "rainfall_mm": 14.0,
        "leaf_wetness_hours": 12.0,
        "alert_level": "HIGH"
    },
    {
        "district_name": "Indore",
        "state": "Madhya Pradesh",
        "crop_type": "Corn/Maize",
        "risk_score": 42.0,
        "primary_threat": "Corn Common Rust",
        "temperature": 28.0,
        "humidity": 65.0,
        "rainfall_mm": 2.0,
        "leaf_wetness_hours": 5.5,
        "alert_level": "MODERATE"
    },
    {
        "district_name": "Bathinda",
        "state": "Punjab",
        "crop_type": "Potato",
        "risk_score": 64.0,
        "primary_threat": "Potato Early Blight",
        "temperature": 24.8,
        "humidity": 76.0,
        "rainfall_mm": 6.0,
        "leaf_wetness_hours": 8.5,
        "alert_level": "MODERATE"
    }
]

FARMER_DIAGNOSES_SEED = [
    ("Nashik", "Maharashtra", "Tomato", "Tomato_Late_Blight", 32.5, 82.5, 94.2, 89.5),
    ("Karnal", "Haryana", "Tomato", "Tomato_Early_Blight", 18.0, 68.0, 91.0, 81.8),
    ("Ludhiana", "Punjab", "Potato", "Potato_Early_Blight", 22.4, 76.0, 88.5, 83.5),
    ("Anand", "Gujarat", "Corn/Maize", "Corn_Common_Rust", 41.0, 71.5, 96.0, 86.2),
    ("Shimla", "Himachal Pradesh", "Potato", "Potato_Early_Blight", 28.6, 88.0, 92.5, 90.7),
    ("Pune", "Maharashtra", "Tomato", "Tomato_Late_Blight", 15.0, 79.0, 89.0, 85.0),
    ("Varanasi", "Uttar Pradesh", "Tomato", "Healthy_Leaf", 0.0, 54.0, 98.0, 80.4),
    ("Indore", "Madhya Pradesh", "Corn/Maize", "Corn_Common_Rust", 19.5, 42.0, 87.0, 69.0),
    ("Bathinda", "Punjab", "Potato", "Potato_Early_Blight", 25.0, 64.0, 90.0, 79.6),
    ("Guntur", "Andhra Pradesh", "Tomato", "Healthy_Leaf", 0.0, 28.0, 99.0, 70.6)
]

def seed_data():
    init_db()
    conn = get_db()
    cursor = conn.cursor()

    # Clear existing
    cursor.execute("DELETE FROM advisories")
    cursor.execute("DELETE FROM district_risks")
    cursor.execute("DELETE FROM farmer_diagnoses")

    # Insert Advisories
    for adv in ICAR_ADVISORIES:
        cursor.execute('''
            INSERT INTO advisories (id, crop_type, disease_name, scientific_name, organic_treatment, chemical_treatment, key_visual_features, disclaimer)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (adv["id"], adv["crop_type"], adv["disease_name"], adv["scientific_name"], adv["organic_treatment"], adv["chemical_treatment"], adv["key_visual_features"], adv["disclaimer"]))

    # Insert District Risks
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    for d in DISTRICT_MOCK_DATA:
        cursor.execute('''
            INSERT INTO district_risks (district_name, state, crop_type, risk_score, primary_threat, temperature, humidity, rainfall_mm, leaf_wetness_hours, alert_level, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (d["district_name"], d["state"], d["crop_type"], d["risk_score"], d["primary_threat"], d["temperature"], d["humidity"], d["rainfall_mm"], d["leaf_wetness_hours"], d["alert_level"], now_str))

    # Insert Farmer Diagnoses
    for row in FARMER_DIAGNOSES_SEED:
        cursor.execute('''
            INSERT INTO farmer_diagnoses (district_name, state, crop_type, disease_predicted, severity_pct, stage_a_risk, stage_b_confidence, fusion_confidence, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], now_str))

    conn.commit()
    conn.close()
    print("Database seeded with ICAR advisories, district risk heatmaps, and farmer diagnosis logs successfully!")

if __name__ == "__main__":
    seed_data()
