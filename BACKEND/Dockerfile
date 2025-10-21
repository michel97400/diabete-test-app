# Backend Dockerfile optimisé pour Render
FROM python:3.11-slim

# Variables d'environnement pour Python
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Définir le répertoire de travail
WORKDIR /app

# Installer les dépendances système nécessaires
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copier tout le code source d'abord
COPY . .

# Installer les dépendances Python
RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Exposer le port (Render utilise la variable PORT)
EXPOSE $PORT

# Commande pour démarrer l'application
CMD uvicorn main:app --host 0.0.0.0 --port ${PORT:-8000}
