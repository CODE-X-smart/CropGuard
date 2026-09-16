import sqlite3
import json
from datetime import datetime
from backend.config import DB_PATH

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    cursor = conn.cursor()

    # Table 1: ICAR Treatment Advisories
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS advisories (
            id TEXT PRIMARY KEY,
            crop_type TEXT NOT NULL,
            disease_name TEXT NOT NULL,
            scientific_name TEXT,
            organic_treatment TEXT NOT NULL,
            chemical_treatment TEXT NOT NULL,
            key_visual_features TEXT NOT NULL,
            disclaimer TEXT NOT NULL
        )
    ''')

    # Table 2: District Outbreak Risk Heatmap Records
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS district_risks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            district_name TEXT NOT NULL,
            state TEXT NOT NULL,
            crop_type TEXT NOT NULL,
            risk_score REAL NOT NULL,
            primary_threat TEXT NOT NULL,
            temperature REAL NOT NULL,
            humidity REAL NOT NULL,
            rainfall_mm REAL NOT NULL,
            leaf_wetness_hours REAL NOT NULL,
            alert_level TEXT NOT NULL,
            updated_at TEXT NOT NULL
        )
    ''')

    # Table 3: Farmer Diagnosis Log Entries
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS farmer_diagnoses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            district_name TEXT NOT NULL,
            state TEXT NOT NULL,
            crop_type TEXT NOT NULL,
            disease_predicted TEXT NOT NULL,
            severity_pct REAL NOT NULL,
            stage_a_risk REAL NOT NULL,
            stage_b_confidence REAL NOT NULL,
            fusion_confidence REAL NOT NULL,
            created_at TEXT NOT NULL
        )
    ''')

    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()
    print("Database schema initialized successfully!")
