#!/bin/bash

# Configuration
RESOURCE_GROUP="diabete-app-rg"
LOCATION="westeurope"
CONTAINER_APP_ENV="diabete-env"
BACKEND_APP_NAME="diabete-backend"
FRONTEND_APP_NAME="diabete-frontend"
REGISTRY_NAME="diabeteregistry"

echo "🚀 Déploiement Azure Container Apps pour l'application Diabète"

# 1. Créer le groupe de ressources
echo "📦 Création du groupe de ressources..."
az group create \
  --name $RESOURCE_GROUP \
  --location $LOCATION

# 2. Créer Azure Container Registry
echo "🐳 Création d'Azure Container Registry..."
az acr create \
  --resource-group $RESOURCE_GROUP \
  --name $REGISTRY_NAME \
  --sku Basic \
  --admin-enabled true

# 3. Construire et pousser l'image Docker du backend
echo "🔨 Construction de l'image Docker backend..."
cd BACKEND
az acr build \
  --registry $REGISTRY_NAME \
  --image diabete-backend:latest \
  .

# 4. Créer l'environnement Container Apps
echo "🏗️ Création de l'environnement Container Apps..."
az containerapp env create \
  --name $CONTAINER_APP_ENV \
  --resource-group $RESOURCE_GROUP \
  --location $LOCATION

# 5. Déployer le backend Container App
echo "🚢 Déploiement du backend..."
az containerapp create \
  --name $BACKEND_APP_NAME \
  --resource-group $RESOURCE_GROUP \
  --environment $CONTAINER_APP_ENV \
  --image $REGISTRY_NAME.azurecr.io/diabete-backend:latest \
  --target-port 8000 \
  --ingress external \
  --registry-server $REGISTRY_NAME.azurecr.io \
  --cpu 0.5 \
  --memory 1Gi \
  --min-replicas 1 \
  --max-replicas 10

# 6. Obtenir l'URL du backend
BACKEND_URL=$(az containerapp show \
  --name $BACKEND_APP_NAME \
  --resource-group $RESOURCE_GROUP \
  --query properties.configuration.ingress.fqdn \
  --output tsv)

echo "✅ Backend déployé à : https://$BACKEND_URL"

# 7. Créer Static Web App pour le frontend
echo "🌐 Création de Static Web App..."
cd ../FRONTEND

# Créer le fichier .env.production avec l'URL du backend
echo "VITE_API_URL=https://$BACKEND_URL" > .env.production
echo "VITE_PREDICT_ENDPOINT=/predict" >> .env.production

az staticwebapp create \
  --name $FRONTEND_APP_NAME \
  --resource-group $RESOURCE_GROUP \
  --source https://github.com/michel97400/diabete-test-app \
  --location $LOCATION \
  --branch main \
  --app-location "FRONTEND" \
  --output-location "dist" \
  --login-with-github

echo "🎉 Déploiement terminé !"
echo "Frontend: Check Azure portal for Static Web App URL"
echo "Backend: https://$BACKEND_URL"