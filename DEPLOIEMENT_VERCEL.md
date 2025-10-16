# 🚀 Déploiement sur Vercel

Ce guide explique comment déployer l'application "Fiches Pédagogiques" sur Vercel.

## Méthode 1 : Via le CLI Vercel (Recommandée)

### 1. Installer Vercel CLI

```bash
npm install -g vercel
```

### 2. Se connecter à Vercel

```bash
vercel login
```

### 3. Déployer l'application

Depuis la racine du projet :

```bash
vercel
```

Suivez les instructions :
- **Set up and deploy?** → Yes
- **Which scope?** → Sélectionnez votre compte
- **Link to existing project?** → No (première fois)
- **Project name?** → fiches-mots (ou le nom de votre choix)
- **Directory?** → `./` (racine)
- **Override settings?** → No

### 4. Déploiement en production

Pour déployer en production :

```bash
vercel --prod
```

## Méthode 2 : Via l'interface Vercel (GitHub)

### 1. Créer un dépôt GitHub

```bash
# Créer un nouveau dépôt sur GitHub, puis :
git remote add origin https://github.com/VOTRE_USERNAME/fiches-mots.git
git branch -M main
git push -u origin main
```

### 2. Connecter à Vercel

1. Allez sur [vercel.com](https://vercel.com)
2. Cliquez sur "New Project"
3. Importez votre dépôt GitHub
4. Configurez le projet :
   - **Framework Preset:** Other
   - **Root Directory:** `./`
   - **Build Command:** (laisser vide)
   - **Output Directory:** `web`

### 3. Variables d'environnement (IMPORTANT)

⚠️ **N'oubliez pas de configurer vos clés API dans l'interface Vercel :**

1. Dans les paramètres du projet → "Environment Variables"
2. Ajoutez :
   - `UNSPLASH_ACCESS_KEY` = votre clé Unsplash
   - `PIXABAY_API_KEY` = votre clé Pixabay

## Configuration du projet

Le fichier `vercel.json` à la racine configure :
- Les routes pour servir les fichiers depuis `/web`
- Les headers CORS pour les API externes
- Le build statique

## Structure attendue

```
fiches-mots/
├── vercel.json          # Configuration Vercel
├── web/                 # Dossier de l'application
│   ├── index.html
│   ├── css/
│   ├── js/
│   │   ├── config.api.js  # ⚠️ À configurer avec vos clés
│   │   └── ...
│   └── fonts/
└── ...
```

## ⚠️ Sécurité des clés API

**IMPORTANT :** Les clés API sont exposées côté client (application statique).

Options :
1. **Restriction d'URL** : Limitez vos clés API aux domaines Vercel uniquement
   - Unsplash : Paramètres → Domain whitelist
   - Pixabay : Pas de restriction nécessaire (clé publique)

2. **Rotation régulière** : Changez vos clés régulièrement

## Après le déploiement

Votre application sera disponible à :
- **Preview :** `https://fiches-mots-RANDOM.vercel.app`
- **Production :** `https://fiches-mots.vercel.app`

Vous pouvez également configurer un domaine personnalisé dans les paramètres Vercel.

## Mises à jour

Pour mettre à jour l'application :

```bash
git add .
git commit -m "Mise à jour"
git push origin main
```

Vercel redéploiera automatiquement ! 🎉

## Dépannage

### Erreur : API keys non configurées

Si vous voyez l'erreur "Configuration API manquante" :
1. Vérifiez que `web/js/config.api.js` existe
2. Vérifiez que les clés ne contiennent pas `YOUR_`

### Erreur CORS

Si les images ne chargent pas :
1. Vérifiez les headers CORS dans `vercel.json`
2. Vérifiez la console du navigateur pour les erreurs

## Support

Pour plus d'informations : https://vercel.com/docs
