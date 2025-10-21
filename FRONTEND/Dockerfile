# Multi-stage build pour optimiser la production
FROM node:22-alpine AS builder

# Définir le répertoire de travail
WORKDIR /app

# Copier les fichiers de dépendances
COPY package*.json ./

# Installer les dépendances
RUN npm ci --only=production

# Copier le code source
COPY . .

# Build de production
RUN npm run build

# Stage 2: Serveur de production avec Nginx
FROM nginx:alpine

# Copier les fichiers buildés depuis le stage précédent
COPY --from=builder /app/dist /usr/share/nginx/html

# Copier la configuration Nginx pour SPA
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Exposer le port 80
EXPOSE 80

# Démarrer Nginx
CMD ["nginx", "-g", "daemon off;"]