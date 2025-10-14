# 🏥 Test Diabète - Centre Hospitalier Felix Guichard

Application web de dépistage précoce du diabète basée sur l'analyse des symptômes. Cette interface permet aux patients de réaliser une évaluation préliminaire de leur risque de diabète grâce à un questionnaire médical intelligent.

## 🎯 Fonctionnalités

### ✅ Interface Patient
- **Questionnaire interactif** : 16 questions sur les symptômes du diabète
- **Design responsive** : Optimisé pour desktop, tablette et mobile
- **Menu burger** : Navigation mobile avec animation croix
- **Résultats détaillés** : Probabilités, niveau de risque et recommandations

### 🔬 Analyse Médicale
- **API de prédiction** : Connexion à un modèle d'IA pour l'analyse
- **Évaluation en temps réel** : Résultats instantanés
- **Recommandations personnalisées** : Conseils selon le niveau de risque
- **Visualisation des probabilités** : Barres de progression interactives

### 🎨 Design & UX
- **Interface moderne** : Design professionnel aux couleurs de l'établissement
- **Formulaire en colonnes** : Organisation optimisée des questions
- **Animations fluides** : Transitions et effets visuels
- **Accessibilité** : Labels ARIA et navigation au clavier

## 🛠️ Technologies Utilisées

- **Frontend** : React 18 + Vite
- **Styling** : CSS3 avec Grid et Flexbox
- **State Management** : React Hooks (useState)
- **API** : Fetch API pour les requêtes HTTP
- **Build Tool** : Vite pour le développement et la production

## 📋 Prérequis

- Node.js (version 16 ou supérieure)
- npm ou yarn
- API Backend fonctionnelle sur `http://127.0.0.1:8000`

## 🚀 Installation

### 1. Cloner le projet
```bash
git clone [URL_DU_REPO]
cd Site_diabete
```

### 2. Installer les dépendances
```bash
npm install
```

### 3. Configuration de l'environnement
Créer un fichier `.env` à la racine du projet :
```env
VITE_API_URL=http://127.0.0.1:8000
VITE_PREDICT_ENDPOINT=/predict
```

### 4. Lancer le serveur de développement
```bash
npm run dev
```

L'application sera accessible sur `http://localhost:5173`

## 🔧 Scripts Disponibles

```bash
# Développement
npm run dev          # Lance le serveur de développement

# Production
npm run build        # Génère les fichiers de production
npm run preview      # Prévisualise la version de production

# Qualité du code
npm run lint         # Vérifie le code avec ESLint
```

## 📁 Structure du Projet

```
Site_diabete/
├── public/
├── src/
│   ├── assets/
│   │   ├── logo_bp.png
│   │   ├── facebook.svg
│   │   ├── instagram.svg
│   │   ├── twitter.svg
│   │   └── youtube.svg
│   ├── App.jsx          # Composant principal
│   ├── App.css          # Styles CSS
│   └── main.jsx         # Point d'entrée React
├── .env                 # Variables d'environnement
├── .gitignore
├── package.json
├── vite.config.js
└── README.md
```

## 🔗 API Backend

L'application communique avec une API Python/FastAPI qui doit exposer :

### Endpoint de Prédiction
```
POST /predict
Content-Type: application/json

{
  "age": 45,
  "gender": "Female",
  "polyuria": "No",
  "polydipsia": "Yes",
  // ... autres symptômes
}
```

### Réponse Attendue
```json
{
  "success": true,
  "prediction": 1,
  "prediction_label": "Diabète détecté",
  "probabilities": {
    "no_diabetes": 0.2543,
    "diabetes": 0.7457
  },
  "confidence": 0.7457,
  "risk_level": "Élevé"
}
```

## 📱 Responsive Design

### Desktop (> 768px)
- Layout en colonnes pour le formulaire
- Navigation horizontale
- Sidebar potentielle pour les résultats

### Tablette (768px - 480px)
- Formulaire adaptatif
- Menu burger activé
- Colonnes réduites

### Mobile (< 480px)
- Interface single-column
- Boutons radio optimisés
- Navigation par menu burger

## 🎨 Personnalisation

### Couleurs Principales
```css
:root {
  --primary-color: #009ad6;      /* Bleu principal */
  --success-color: #28a745;      /* Vert succès */
  --danger-color: #dc3545;       /* Rouge danger */
  --warning-color: #ffc107;      /* Jaune attention */
}
```

### Typographie
- **Titres** : Font-weight bold, tailles variables
- **Labels** : Font-weight 500 pour la lisibilité
- **Texte** : Font-family system par défaut

## 🔒 Sécurité

- **Validation côté client** : Vérification des champs requis
- **HTTPS recommandé** : Pour la production
- **CORS** : Configuration requise côté API
- **Données sensibles** : Pas de stockage local des données médicales

## 🚀 Déploiement

### Build de Production
```bash
npm run build
```

Les fichiers optimisés seront générés dans le dossier `dist/`

## 👥 Contribution

1. Fork le projet
2. Créer une branche feature (`git checkout -b feature/amelioration`)
3. Commiter les changements (`git commit -m 'Ajout fonctionnalité'`)
4. Push vers la branche (`git push origin feature/amelioration`)
5. Ouvrir une Pull Request

## 📞 Support

Pour toute question ou problème :
- **Email** : michel.payet974@live.fr
- **Documentation** : Voir le wiki du projet
- **Issues** : Utiliser le système d'issues GitHub

## 📄 Licence

Ce projet est sous licence MIT. Voir le fichier `LICENSE` pour plus de détails.

## 🏥 À Propos

Développé par moi

---

**⚠️ Avertissement Médical** : Cette application est un outil d'aide au dépistage et ne remplace pas une consultation médicale. Les résultats doivent toujours être confirmés par un professionnel de santé.
