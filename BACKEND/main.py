from typing import Union, Dict, Any
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from model import ModelDiabetes
import os
from fastapi.middleware.cors import CORSMiddleware

# Initialisation de l'application FastAPI
app = FastAPI(
    title="API de Prédiction du Diabète",
    description="API pour prédire le risque de diabète basée sur des symptômes médicaux",
    version="1.0.0"
)

origins = [
    "http://localhost",
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialisation du modèle (global pour éviter de recharger à chaque requête)
model = None

@app.on_event("startup")
async def startup_event():
    """Charge le modèle au démarrage de l'application"""
    global model
    try:
        model = ModelDiabetes("Model_diabetes_RF.pkl")
        model.load_model()
        print("✅ Modèle chargé avec succès au démarrage")
    except Exception as e:
        print(f"❌ Erreur lors du chargement du modèle: {e}")
        model = None

# Modèle Pydantic pour valider les données d'entrée
class PatientData(BaseModel):
    """Modèle de données pour un patient"""
    age: int = Field(..., description="Âge du patient", example=45, ge=0, le=120)
    gender: str = Field(..., description="Genre du patient", example="Female")
    polyuria: str = Field(..., description="Polyurie (miction excessive)", example="No")
    polydipsia: str = Field(..., description="Polydipsie (soif excessive)", example="Yes")
    sudden_weight_loss: str = Field(..., description="Perte de poids soudaine", example="No")
    weakness: str = Field(..., description="Faiblesse", example="Yes")
    polyphagia: str = Field(..., description="Polyphagie (faim excessive)", example="No")
    genital_thrush: str = Field(..., description="Candidose génitale", example="No")
    visual_blurring: str = Field(..., description="Vision floue", example="No")
    itching: str = Field(..., description="Démangeaisons", example="Yes")
    irritability: str = Field(..., description="Irritabilité", example="No")
    delayed_healing: str = Field(..., description="Cicatrisation retardée", example="No")
    partial_paresis: str = Field(..., description="Parésie partielle", example="No")
    muscle_stiffness: str = Field(..., description="Raideur musculaire", example="Yes")
    alopecia: str = Field(..., description="Alopécie (perte de cheveux)", example="No")
    obesity: str = Field(..., description="Obésité", example="Yes")

    class Config:
        json_schema_extra = {
            "example": {
                "age": 25,
                "gender": "Male",
                "polyuria": "No",
                "polydipsia": "No",
                "sudden_weight_loss": "Yes",
                "weakness": "No",
                "polyphagia": "No",
                "genital_thrush": "No",
                "visual_blurring": "Yes",
                "itching": "No",
                "irritability": "No",
                "delayed_healing": "No",
                "partial_paresis": "No",
                "muscle_stiffness": "Yes",
                "alopecia": "No",
                "obesity": "Yes"
            }
        }
    


@app.get("/")
def read_root():
    """Page d'accueil de l'API"""
    return {
        "message": "API de Prédiction du Diabète",
        "version": "1.0.0",
        "status": "Modèle chargé" if model and model.is_loaded else "Modèle non disponible",
        "endpoints": {
            "prediction": "/predict",
            "health": "/health"
        }
    }

@app.get("/health")
def health_check():
    """Vérification de l'état de l'API et du modèle"""
    if not model:
        raise HTTPException(status_code=503, detail="Modèle non initialisé")
    
    if not model.is_loaded:
        raise HTTPException(status_code=503, detail="Modèle non chargé")
    
    model_info = model.get_model_info()
    return {
        "status": "healthy",
        "model_info": model_info,
        "message": "API et modèle opérationnels"
    }


@app.post("/predict")
def predict_diabetes(patient_data: PatientData):
    """
    Prédiction du risque de diabète pour un patient
    
    Args:
        patient_data: Données du patient au format JSON
        
    Returns:
        Résultat de la prédiction avec probabilités et niveau de risque
    """
    if not model:
        raise HTTPException(status_code=503, detail="Modèle non disponible")
    
    if not model.is_loaded:
        raise HTTPException(status_code=503, detail="Modèle non chargé")
    
    try:
        # Convertir les données Pydantic en dictionnaire
        patient_dict = patient_data.dict()
        
        # Faire la prédiction avec votre classe
        result = model.predict_from_json(patient_dict)
        
        if not result.get("success", False):
            raise HTTPException(
                status_code=400, 
                detail=f"Erreur de prédiction: {result.get('error', 'Erreur inconnue')}"
            )
        
        return result
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur interne: {str(e)}")