#!/bin/bash

##
# Script de démarrage du serveur de développement
# Utilise Vercel Dev pour les fonctions serverless
##

echo "🚀 Démarrage du serveur de développement Fiches Pédagogiques"
echo "=================================================="
echo ""

# Vérifier que Vercel CLI est installé
if ! command -v vercel &> /dev/null; then
    echo "❌ Vercel CLI n'est pas installé!"
    echo ""
    echo "Installation:"
    echo "  npm install -g vercel"
    echo ""
    exit 1
fi

# Vérifier que le fichier .env existe
if [ ! -f .env ]; then
    echo "⚠️  Fichier .env non trouvé!"
    echo ""
    echo "Création depuis .env.example..."
    cp .env.example .env
    echo "✅ Fichier .env créé"
    echo ""
    echo "⚠️  ATTENTION: Éditez .env avec vos vraies clés API!"
    echo ""
    exit 1
fi

# Vérifier que les clés API sont configurées
if grep -q "YOUR_" .env; then
    echo "⚠️  Les clés API dans .env ne sont pas configurées!"
    echo ""
    echo "Éditez le fichier .env et remplacez les valeurs par défaut:"
    echo "  nano .env"
    echo ""
    exit 1
fi

# Tuer tout processus sur le port 3000
echo "🔍 Vérification du port 3000..."
if lsof -ti:3000 > /dev/null 2>&1; then
    echo "⚠️  Port 3000 déjà utilisé, libération..."
    lsof -ti:3000 | xargs kill -9
    sleep 1
    echo "✅ Port 3000 libéré"
fi

echo ""
echo "🎯 Lancement de Vercel Dev sur http://localhost:3000"
echo "=================================================="
echo ""
echo "📝 Pour arrêter le serveur: Ctrl+C"
echo ""

# Lancer Vercel Dev
exec vercel dev --listen 3000
