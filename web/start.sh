#!/bin/bash
# Script de démarrage du serveur web

echo "🚀 Démarrage du serveur web..."
echo ""
echo "📂 Dossier: $(pwd)"
echo "🌐 URL: http://localhost:8000"
echo ""
echo "📸 Utilise l'API Unsplash pour des photos de haute qualité"
echo "🔍 Les images correspondent aux mots recherchés (chat, chien, etc.)"
echo ""
echo "Ouvrez votre navigateur à l'adresse ci-dessus"
echo "Appuyez sur Ctrl+C pour arrêter le serveur"
echo ""
echo "---"
echo ""

# Utiliser le serveur HTTP simple de Python (pas besoin de proxy avec Unsplash API)
python3 -m http.server 8000
