# 🩺 API de Prédiction du Diabète

Une API REST développée avec FastAPI pour prédire le risque de diabète basée sur des symptômes médicaux, utilisant un modèle de machine learning Random Forest.

## 📋 Table des matières

- [Vue d'ensemble](#-vue-densemble)
- [Modèle de Machine Learning](#-modèle-de-machine-learning)
- [Architecture de l'API](#-architecture-de-lapi)
- [Installation](#-installation)
- [Utilisation](#-utilisation)
- [Endpoints](#-endpoints)
- [Format des données](#-format-des-données)
- [Exemples](#-exemples)
- [Structure du projet](#-structure-du-projet)

## 🎯 Vue d'ensemble

Cette API permet de prédire le risque de diabète d'un patient en analysant 15 variables médicales. Le système utilise un modèle Random Forest entraîné sur des données médicales pour fournir :

- **Prédiction binaire** : Diabète détecté (1) ou pas de diabète (0)
- **Probabilités** : Niveau de confiance pour chaque classe
- **Niveau de risque** : Interprétation qualitative (Faible, Modéré, Élevé, Très élevé)

## 🤖 Modèle de Machine Learning

### Algorithme
- **Type** : Random Forest Classifier
- **Bibliothèque** : scikit-learn
- **Paramètres** :
  - `n_estimators=300` (300 arbres)
  - `max_depth=8` (profondeur maximale)
  - `min_samples_split=5`
  - `min_samples_leaf=2`
  - `random_state=42`

### Variables d'entrée (Features)

| Variable | Type | Description | Valeurs |
|----------|------|-------------|---------|
| `age` | Numérique | Âge du patient | 0-120 ans |
| `gender` | Catégorielle | Genre | Female, Male |
| `polyuria` | Binaire | Miction excessive | Yes, No |
| `polydipsia` | Binaire | Soif excessive | Yes, No |
| `sudden_weight_loss` | Binaire | Perte de poids soudaine | Yes, No |
| `weakness` | Binaire | Faiblesse | Yes, No |
| `polyphagia` | Binaire | Faim excessive | Yes, No |
| `genital_thrush` | Binaire | Candidose génitale | Yes, No |
| `visual_blurring` | Binaire | Vision floue | Yes, No |
| `itching` | Binaire | Démangeaisons | Yes, No |
| `irritability` | Binaire | Irritabilité | Yes, No |
| `delayed_healing` | Binaire | Cicatrisation retardée | Yes, No |
| `partial_paresis` | Binaire | Parésie partielle | Yes, No |
| `muscle_stiffness` | Binaire | Raideur musculaire | Yes, No |
| `alopecia` | Binaire | Perte de cheveux | Yes, No |
| `obesity` | Binaire | Obésité | Yes, No |

### Encodage des données
- **Genre** : Female=0, Male=1
- **Variables binaires** : No=0, Yes=1
- **Âge** : Valeur numérique directe

## 🏗️ Architecture de l'API

### Technologies utilisées
- **Framework** : FastAPI
- **Validation** : Pydantic
- **ML** : scikit-learn, joblib
- **Data** : pandas, numpy
- **Server** : Uvicorn

### Structure des classes

#### `ModelDiabetes` (model.py)
Classe principale pour l'inférence :
- `load_model()` : Charge le modèle .pkl
- `validate_json_input()` : Valide les données d'entrée
- `preprocess_input()` : Préprocessing et encodage
- `predict_from_json()` : Prédiction complète avec métadonnées
- `predict()` : Prédiction simple


#### `PatientData` (main.py)
Modèle Pydantic pour la validation des données d'entrée avec contraintes automatiques.

## 🚀 Installation

### Prérequis
- Python 3.8+
- pip

### Installation des dépendances

```bash
# Cloner le repository
git clone <repository-url>
cd API_model_diabete

# Créer un environnement virtuel
python -m venv .venv

# Activer l'environnement virtuel
# Windows
.venv\Scripts\activate
# Linux/Mac
source .venv/bin/activate

# Installer les dépendances
pip install fastapi uvicorn scikit-learn joblib pandas numpy pydantic
```

### Lancement de l'API

```bash
uvicorn main:app --reload
```

L'API sera accessible sur : `http://127.0.0.1:8000`

## 📖 Utilisation

### Documentation interactive
- **Swagger UI** : `http://127.0.0.1:8000/docs`
- **ReDoc** : `http://127.0.0.1:8000/redoc`

### Test rapide
```bash
curl -X POST "http://127.0.0.1:8000/predict" \
  -H "Content-Type: application/json" \
  -d '{
    "age": 45,
    "gender": "Female",
    "polyuria": "No",
    "polydipsia": "Yes",
    "sudden_weight_loss": "No",
    "weakness": "Yes",
    "polyphagia": "No",
    "genital_thrush": "No",
    "visual_blurring": "No",
    "itching": "Yes",
    "irritability": "No",
    "delayed_healing": "No",
    "partial_paresis": "No",
    "muscle_stiffness": "Yes",
    "alopecia": "No",
    "obesity": "Yes"
  }'
```

## 🔗 Endpoints

### `GET /`
Page d'accueil avec informations sur l'API.

### `POST /predict`
**Endpoint principal** pour la prédiction de diabète.

**Entrée** : JSON avec les 16 variables médicales
**Sortie** : Prédiction avec probabilités et métadonnées



## 📊 Format des données

### Entrée (JSON)
```json
{
  "age": 45,
  "gender": "Female",
  "polyuria": "No",
  "polydipsia": "Yes",
  "sudden_weight_loss": "No",
  "weakness": "Yes",
  "polyphagia": "No",
  "genital_thrush": "No",
  "visual_blurring": "No",
  "itching": "Yes",
  "irritability": "No",
  "delayed_healing": "No",
  "partial_paresis": "No",
  "muscle_stiffness": "Yes",
  "alopecia": "No",
  "obesity": "Yes"
}
```

### Sortie (JSON)
```json
{
  "success": true,
  "prediction": 0,
  "prediction_label": "Pas de diabète détecté",
  "probabilities": {
    "no_diabetes": 0.8234,
    "diabetes": 0.1766
  },
  "confidence": 0.8234,
  "risk_level": "Faible",
  "input_data": { ... }
}
```

### Niveaux de risque
- **Faible** : < 30% de probabilité de diabète
- **Modéré** : 30-60% de probabilité de diabète
- **Élevé** : 60-80% de probabilité de diabète
- **Très élevé** : > 80% de probabilité de diabète

## 📝 Exemples

### Python avec requests
```python
import requests

url = "http://127.0.0.1:8000/predict"
data = {
    "age": 45,
    "gender": "Female",
    "polyuria": "No",
    "polydipsia": "Yes",
    # ... autres champs
}

response = requests.post(url, json=data)
result = response.json()
print(f"Prédiction: {result['prediction_label']}")
print(f"Confiance: {result['confidence']:.2%}")
```

### JavaScript/Frontend
```javascript
const predictDiabetes = async (patientData) => {
  const response = await fetch('http://127.0.0.1:8000/predict', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(patientData)
  });
  
  const result = await response.json();
  return result;
};
```

## 📁 Structure du projet

```
API_model_diabete/
├── main.py                      # API FastAPI
├── model.py                     # Classe ModelDiabetes
├── Model_diabetes_RF.pkl        # Modèle ML entraîné
├── model_diab_V1-0.ipynb       # Notebook d'entraînement
├── README.md                    # Documentation
├── .gitignore                   # Fichiers Git ignorés
└── .venv/                       # Environnement virtuel
```

## 🔧 Développement

### Réentraîner le modèle
1. Ouvrir `model_diab_V1-0.ipynb`
2. Exécuter toutes les cellules
3. Le nouveau modèle sera sauvegardé automatiquement

### Modifications de l'API
- Modifier `model.py` pour la logique métier
- Modifier `main.py` pour les endpoints
- Redémarrer avec `uvicorn main:app --reload`

### Tests
L'API inclut une validation automatique et une gestion d'erreurs complète. Utilisez l'interface Swagger pour tester facilement tous les endpoints.

## 📞 Support

Pour toute question ou problème :
1. Vérifiez la documentation interactive sur `/docs`
2. Testez avec l'endpoint `/example` pour obtenir des données valides
3. Consultez les logs de l'API pour les erreurs détaillées

---

**Auteur** : michel97400  
**Version** : 1.0.0  
**Licence** : MIT