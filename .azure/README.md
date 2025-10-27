# Déploiement sur Azure Container Apps

## Prérequis

1. **Azure CLI installé** : https://docs.microsoft.com/en-us/cli/azure/install-azure-cli
2. **Compte Azure actif** avec un abonnement
3. **Extensions Azure CLI** :
   ```bash
   az extension add --name containerapp
   az extension add --name staticwebapp
   ```

## Architecture déployée

```
┌─────────────────┐    ┌──────────────────────┐
│  Static Web App │───▶│  Container App       │
│  (Frontend)     │    │  (Backend API)       │
│  React + Vite   │    │  FastAPI + Python    │
└─────────────────┘    └──────────────────────┘
         │                        │
         ▼                        ▼
┌─────────────────┐    ┌──────────────────────┐
│ Azure CDN       │    │ Container Registry   │
│ Global          │    │ Docker Images        │
└─────────────────┘    └──────────────────────┘
```

## Déploiement automatique

### Option 1 : PowerShell (Windows)
```powershell
# Se connecter à Azure
az login

# Exécuter le script de déploiement
.\.azure\deploy.ps1
```

### Option 2 : Bash (Linux/macOS)
```bash
# Se connecter à Azure
az login

# Rendre le script exécutable
chmod +x .azure/deploy.sh

# Exécuter le script
./.azure/deploy.sh
```

## Déploiement manuel étape par étape

### 1. Créer le groupe de ressources
```bash
az group create \
  --name diabete-app-rg \
  --location westeurope
```

### 2. Créer Azure Container Registry
```bash
az acr create \
  --resource-group diabete-app-rg \
  --name diabeteregistry \
  --sku Basic \
  --admin-enabled true
```

### 3. Construire l'image Docker
```bash
cd BACKEND
az acr build \
  --registry diabeteregistry \
  --image diabete-backend:latest \
  .
```

### 4. Créer l'environnement Container Apps
```bash
az containerapp env create \
  --name diabete-env \
  --resource-group diabete-app-rg \
  --location westeurope
```

### 5. Déployer le backend
```bash
az containerapp create \
  --name diabete-backend \
  --resource-group diabete-app-rg \
  --environment diabete-env \
  --image diabeteregistry.azurecr.io/diabete-backend:latest \
  --target-port 8000 \
  --ingress external \
  --registry-server diabeteregistry.azurecr.io \
  --cpu 0.5 \
  --memory 1Gi \
  --min-replicas 1 \
  --max-replicas 10
```

### 6. Déployer le frontend
```bash
az staticwebapp create \
  --name diabete-frontend \
  --resource-group diabete-app-rg \
  --source https://github.com/michel97400/diabete-test-app \
  --location westeurope \
  --branch main \
  --app-location "FRONTEND" \
  --output-location "dist" \
  --login-with-github
```

## Configuration des variables d'environnement

### Backend Container App
Les variables sont configurées automatiquement :
- `PORT=8000`

### Frontend Static Web App
Créer `.env.production` avec :
```
VITE_API_URL=https://[backend-url].azurecontainerapps.io
VITE_PREDICT_ENDPOINT=/predict
```

## Mise à jour de l'application

### Backend
```bash
# Reconstruire l'image
az acr build --registry diabeteregistry --image diabete-backend:latest ./BACKEND

# Redémarrer l'application
az containerapp revision restart \
  --name diabete-backend \
  --resource-group diabete-app-rg
```

### Frontend
Le déploiement se fait automatiquement via GitHub Actions quand vous poussez sur la branche `main`.

## Monitoring et logs

### Container App logs
```bash
az containerapp logs show \
  --name diabete-backend \
  --resource-group diabete-app-rg \
  --follow
```

### Static Web App logs
Consultez le portail Azure > Static Web Apps > votre app > Functions
Y.061199184808ol
## Coûts estimés

- **Container App** : ~10-30€/mois (selon l'usage)
- **Static Web App** : Gratuit jusqu'à 100GB de bande passante
- **Container Registry** : ~5€/mois pour le stockage de base

## Nettoyage des ressources

```bash
az group delete --name diabete-app-rg --yes --no-wait
```