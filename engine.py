import pandas as pd
import os

def analyze_symptoms(symptoms):
    """
    Analyzes input symptoms and returns the estimated condition and
    the required medical specialty.
    """
    if not symptoms:
        return {"condition": "Unknown", "specialty": "General Physician"}

    symptoms = symptoms.lower()

    # Mapping keywords to specific diseases and departments.
    # Note: Keys changed from 'disease' to 'condition' to match your app.py logic.
    mapping = {
        "itch": {"condition": "Psoriasis", "specialty": "Dermatologist"},
        "rash": {"condition": "Fungal infection", "specialty": "Dermatologist"},
        "chest pain": {"condition": "Hypertension", "specialty": "Cardiologist"},
        "heart": {"condition": "Heart Attack", "specialty": "Cardiologist"},
        "fever": {"condition": "Typhoid", "specialty": "General Physician"},
        "cough": {"condition": "Common Cold", "specialty": "General Physician"},
        "stomach": {"condition": "Gastroenteritis", "specialty": "Gastroenterologist"},
        "headache": {"condition": "Migraine", "specialty": "Neurologist"}
    }

    # Search for keywords in the user input
    for key in mapping:
        if key in symptoms:
            return mapping[key]

    # Fallback if no keywords are matched
    return {"condition": "General Consultation", "specialty": "General Physician"}