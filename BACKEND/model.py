
import joblib
import pandas as pd
import numpy as np
from typing import Dict, Union, List, Any
import os


class ModelDiabetes:
    """
    Classe pour charger et utiliser le modèle de prédiction du diabète en inférence.
    Conçue pour être utilisée dans une API FastAPI.
    """
    
    def __init__(self, model_path: str = "Model_diabetes_RF.pkl"):

        self.model_path = model_path
        self.model = None
        self.is_loaded = False
        

        self.feature_columns = [
            'age', 'gender', 'polyuria', 'polydipsia', 'sudden_weight_loss', 'weakness', 
            'polyphagia', 'genital_thrush', 'visual_blurring', 'itching', 
            'irritability', 'delayed_healing', 'partial_paresis', 
            'muscle_stiffness', 'alopecia', 'obesity'
        ]
        
        # Encodages pour les variables catégorielles
        self.encodings = {
            'gender': {'Female': 0, 'Male': 1},
            'polyuria': {'No': 0, 'Yes': 1},
            'polydipsia': {'No': 0, 'Yes': 1},
            'sudden_weight_loss': {'No': 0, 'Yes': 1},
            'weakness': {'No': 0, 'Yes': 1},
            'polyphagia': {'No': 0, 'Yes': 1},
            'genital_thrush': {'No': 0, 'Yes': 1},
            'visual_blurring': {'No': 0, 'Yes': 1},
            'itching': {'No': 0, 'Yes': 1},
            'irritability': {'No': 0, 'Yes': 1},
            'delayed_healing': {'No': 0, 'Yes': 1},
            'partial_paresis': {'No': 0, 'Yes': 1},
            'muscle_stiffness': {'No': 0, 'Yes': 1},
            'alopecia': {'No': 0, 'Yes': 1},
            'obesity': {'No': 0, 'Yes': 1}
        }
        
    def load_model(self):

        try:
            if os.path.exists(self.model_path):
                self.model = joblib.load(self.model_path)
                self.is_loaded = True
                print(f"✅ Modèle chargé depuis: {self.model_path}")
            else:
                raise FileNotFoundError(f"Le fichier {self.model_path} n'existe pas")
        except Exception as e:
            print(f"❌ Erreur lors du chargement du modèle: {e}")
            raise e
    
    def encode_categorical_features(self, data: pd.DataFrame) -> pd.DataFrame:

        data_encoded = data.copy()
        
        for column, mapping in self.encodings.items():
            if column in data_encoded.columns:
                # Gérer les valeurs inconnues en les remplaçant par la première valeur connue
                data_encoded[column] = data_encoded[column].apply(
                    lambda x: mapping.get(x, list(mapping.values())[0])
                )
        
        return data_encoded
    
    def preprocess_input(self, input_data: Union[Dict, List[Dict], pd.DataFrame]) -> pd.DataFrame:
 
        # Convertir en DataFrame 
        if isinstance(input_data, dict):
            df = pd.DataFrame([input_data])
        elif isinstance(input_data, list):
            df = pd.DataFrame(input_data)
        elif isinstance(input_data, pd.DataFrame):
            df = input_data.copy()
        else:
            raise ValueError("Les données doivent être un dict, une liste de dict ou un DataFrame")
        
        # Vérifier les colonnes requises
        missing_columns = set(self.feature_columns) - set(df.columns)
        if missing_columns:
            raise ValueError(f"Colonnes manquantes: {missing_columns}")
        
        # Sélectionner uniquement les colonnes nécessaires dans le bon ordre
        df = df[self.feature_columns]
        
        # Encoder les variables catégorielles
        df_encoded = self.encode_categorical_features(df)
        
        return df_encoded
    
    def predict(self, input_data: Union[Dict, List[Dict], pd.DataFrame]) -> List[int]:

        if not self.is_loaded:
            raise ValueError("Le modèle n'est pas chargé. Utilisez load_model() d'abord.")
        
        # Prétraiter les données
        processed_data = self.preprocess_input(input_data)
        
        # Faire la prédiction
        predictions = self.model.predict(processed_data)
        
        return predictions.tolist()
    
    def predict_proba(self, input_data: Union[Dict, List[Dict], pd.DataFrame]) -> List[List[float]]:

        if not self.is_loaded:
            raise ValueError("Le modèle n'est pas chargé. Utilisez load_model() d'abord.")
        
        # Prétraiter les données
        processed_data = self.preprocess_input(input_data)
        
        # Calculer les probabilités
        probabilities = self.model.predict_proba(processed_data)
        
        return probabilities.tolist()
    
    def validate_json_input(self, json_data: Dict) -> Dict[str, Any]:

        validated_data = {}
        
        # Valider chaque champ médical 
        for field in self.feature_columns:
            if field not in json_data:
                raise ValueError(f"Champ manquant: {field}")
            
            value = json_data[field]
            
            # Traitement spécifique selon le type de champ
            if field == 'age':
                # Age est un nombre
                try:
                    validated_data[field] = int(value)
                    if validated_data[field] < 0 or validated_data[field] > 120:
                        raise ValueError(f"L'âge doit être entre 0 et 120 ans, reçu {validated_data[field]}")
                except (ValueError, TypeError):
                    raise ValueError(f"L'âge doit être un nombre entier, reçu {value}")
            elif field == 'gender':
                # Gender est une chaîne
                validated_data[field] = str(value).strip()
                if validated_data[field] not in self.encodings['gender']:
                    raise ValueError(f"Genre invalide. Valeurs acceptées: {list(self.encodings['gender'].keys())}")
            else:
                # Toutes les autres colonnes sont binaires (Yes/No ou 0/1)
                if isinstance(value, str):
                    value_str = value.strip()
                    if value_str in ['Yes', 'No']:
                        validated_data[field] = value_str
                    elif value_str in ['1', '0']:
                        validated_data[field] = 'Yes' if value_str == '1' else 'No'
                    else:
                        raise ValueError(f"Valeur invalide pour {field}: attendu 'Yes'/'No' ou '1'/'0', reçu '{value}'")
                elif isinstance(value, (int, float)):
                    if value in [0, 1]:
                        validated_data[field] = 'Yes' if value == 1 else 'No'
                    else:
                        raise ValueError(f"Valeur numérique invalide pour {field}: attendu 0 ou 1, reçu {value}")
                else:
                    raise ValueError(f"Type invalide pour {field}: attendu str, int ou float, reçu {type(value)}")
                
                # Vérifier que la valeur est dans les encodages
                if validated_data[field] not in self.encodings[field]:
                    raise ValueError(f"Valeur invalide pour {field}. Valeurs acceptées: {list(self.encodings[field].keys())}")
        
        return validated_data
    
    def predict_from_json(self, json_data: Dict) -> Dict[str, Any]:
        """
        Fait une prédiction à partir de données JSON du frontend.
        Méthode optimisée pour les APIs avec validation complète.
        
        Args:
            json_data (Dict): Données JSON du patient
            
        Returns:
            Dict[str, Any]: Résultat de la prédiction avec probabilités et métadonnées
        """
        if not self.is_loaded:
            raise ValueError("Le modèle n'est pas chargé. Utilisez load_model() d'abord.")
        
        try:
            # Valider et nettoyer les données d'entrée
            validated_data = self.validate_json_input(json_data)
            
            # Faire la prédiction
            prediction = self.predict(validated_data)[0]
            probabilities = self.predict_proba(validated_data)[0]
            
            # Préparer la réponse
            result = {
                "success": True,
                "patient_id": validated_data.get('id', 'N/A'),
                "prediction": int(prediction),
                "prediction_label": "Diabète détecté" if prediction == 1 else "Pas de diabète détecté",
                "probabilities": {
                    "no_diabetes": round(probabilities[0], 4),
                    "diabetes": round(probabilities[1], 4)
                },
                "confidence": round(max(probabilities), 4),
                "risk_level": self._get_risk_level(probabilities[1]),
                "input_data": validated_data
            }
            
            return result
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "message": "Erreur lors de la prédiction"
            }
    
    def _get_risk_level(self, diabetes_probability: float) -> str:
        """
        Détermine le niveau de risque basé sur la probabilité de diabète.
        
        Args:
            diabetes_probability (float): Probabilité de diabète (0-1)
            
        Returns:
            str: Niveau de risque
        """
        if diabetes_probability < 0.3:
            return "Faible"
        elif diabetes_probability < 0.6:
            return "Modéré"
        elif diabetes_probability < 0.8:
            return "Élevé"
        else:
            return "Très élevé"
    
    def predict_single(self, patient_data: Dict) -> Dict[str, Any]:
        """
        Fait une prédiction pour un seul patient et retourne un résultat détaillé.
        
        Args:
            patient_data (Dict): Données du patient
            
        Returns:
            Dict[str, Any]: Résultat de la prédiction avec probabilités
        """
        prediction = self.predict(patient_data)[0]
        probabilities = self.predict_proba(patient_data)[0]
        
        result = {
            "prediction": int(prediction),
            "prediction_label": "Diabète" if prediction == 1 else "Pas de diabète",
            "probability_no_diabetes": round(probabilities[0], 4),
            "probability_diabetes": round(probabilities[1], 4),
            "confidence": round(max(probabilities), 4)
        }
        
        return result
    
    def get_model_info(self) -> Dict[str, Any]:
        """
        Retourne des informations sur le modèle chargé.
        
        Returns:
            Dict[str, Any]: Informations sur le modèle
        """
        info = {
            "model_loaded": self.is_loaded,
            "model_type": type(self.model).__name__ if self.model else None,
            "feature_columns": self.feature_columns,
            "num_features": len(self.feature_columns),
            "categorical_encodings": self.encodings
        }
        
        if self.model and hasattr(self.model, 'n_estimators'):
            info["n_estimators"] = self.model.n_estimators
        if self.model and hasattr(self.model, 'max_depth'):
            info["max_depth"] = self.model.max_depth
        if self.model and hasattr(self.model, 'random_state'):
            info["random_state"] = self.model.random_state
            
        return info
