# Configuration
$ResourceGroup = "diabete-app-rg"
$Location = "westeurope"
$ContainerAppEnv = "diabete-env"
$BackendAppName = "diabete-backend"
$FrontendAppName = "diabete-frontend"
$RegistryName = "diabeteregistry"

Write-Host "🚀 Déploiement Azure Container Apps pour l'application Diabète" -ForegroundColor Green

# 1. Créer le groupe de ressources
Write-Host "📦 Création du groupe de ressources..." -ForegroundColor Yellow
az group create --name $ResourceGroup --location $Location

# 2. Créer Azure Container Registry
Write-Host "🐳 Création d'Azure Container Registry..." -ForegroundColor Yellow
az acr create --resource-group $ResourceGroup --name $RegistryName --sku Basic --admin-enabled true

# 3. Construire et pousser l'image Docker du backend
Write-Host "🔨 Construction de l'image Docker backend..." -ForegroundColor Yellow
Set-Location BACKEND
az acr build --registry $RegistryName --image diabete-backend:latest .

# 4. Créer l'environnement Container Apps
Write-Host "🏗️ Création de l'environnement Container Apps..." -ForegroundColor Yellow
az containerapp env create --name $ContainerAppEnv --resource-group $ResourceGroup --location $Location

# 5. Déployer le backend Container App
Write-Host "🚢 Déploiement du backend..." -ForegroundColor Yellow
az containerapp create `
  --name $BackendAppName `
  --resource-group $ResourceGroup `
  --environment $ContainerAppEnv `
  --image "$RegistryName.azurecr.io/diabete-backend:latest" `
  --target-port 8000 `
  --ingress external `
  --registry-server "$RegistryName.azurecr.io" `
  --cpu 0.5 `
  --memory 1Gi `
  --min-replicas 1 `
  --max-replicas 10

# 6. Obtenir l'URL du backend
$BackendUrl = az containerapp show --name $BackendAppName --resource-group $ResourceGroup --query properties.configuration.ingress.fqdn --output tsv

Write-Host "✅ Backend déployé à : https://$BackendUrl" -ForegroundColor Green

# 7. Créer Static Web App pour le frontend
Write-Host "🌐 Création de Static Web App..." -ForegroundColor Yellow
Set-Location ..\FRONTEND

# Créer le fichier .env.production avec l'URL du backend
"VITE_API_URL=https://$BackendUrl" | Out-File -FilePath .env.production -Encoding UTF8
"VITE_PREDICT_ENDPOINT=/predict" | Add-Content -Path .env.production -Encoding UTF8

az staticwebapp create `
  --name $FrontendAppName `
  --resource-group $ResourceGroup `
  --source "https://github.com/michel97400/diabete-test-app" `
  --location $Location `
  --branch main `
  --app-location "FRONTEND" `
  --output-location "dist" `
  --login-with-github

Write-Host "🎉 Déploiement terminé !" -ForegroundColor Green
Write-Host "Frontend: Vérifiez le portail Azure pour l'URL Static Web App" -ForegroundColor Cyan
Write-Host "Backend: https://$BackendUrl" -ForegroundColor Cyan