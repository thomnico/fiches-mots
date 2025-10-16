# 🚀 Déploiement sur Vercel avec Fonctions Serverless

## 🔐 Architecture Sécurisée

L'application utilise des **fonctions serverless Vercel** pour protéger vos clés API :

```
┌─────────────────┐
│   Navigateur    │
│   (Frontend)    │
└────────┬────────┘
         │
         │ Appel: /api/pixabay?query=...
         ▼
┌─────────────────┐
│  Vercel Edge    │
│   (Fonctions    │
│   Serverless)   │
└────────┬────────┘
         │
         │ Clés API sécurisées (variables d'environnement)
         ▼
┌─────────────────┐
│  API Pixabay /  │
│  API Unsplash   │
└─────────────────┘
```

**Avantages** :
- ✅ Clés API jamais exposées au client
- ✅ Pas de limite CORS
- ✅ Contrôle total sur les requêtes
- ✅ Gratuit sur le plan Vercel Hobby

## 📁 Structure du Projet

```
fiches-mots/
├── api/                          # Fonctions serverless
│   ├── pixabay.js               # Proxy API Pixabay
│   └── unsplash.js              # Proxy API Unsplash
├── web/                         # Application frontend
│   ├── index.html
│   ├── js/
│   │   ├── imageSearch.serverless.js  # ← À utiliser pour Vercel
│   │   └── imageSearch.js             # ← Version dev locale (clés exposées)
│   └── ...
├── vercel.json                  # Configuration Vercel
└── .env.example                 # Template variables d'environnement
```

## 🚀 Étape 1 : Préparer le Déploiement

### 1.1 Modifier index.html

**IMPORTANT** : Changez la référence au fichier JavaScript pour utiliser la version serverless :

Éditez `web/index.html`, remplacez :
```html
<script src="js/imageSearch.js"></script>
```

Par :
```html
<script src="js/imageSearch.serverless.js"></script>
```

### 1.2 Installer Vercel CLI

```bash
npm install -g vercel
```

### 1.3 Se connecter à Vercel

```bash
vercel login
```

## 🔐 Étape 2 : Configurer les Variables d'Environnement

### Option A : Via le CLI (Dev Local)

1. Créez un fichier `.env` à la racine :
```bash
cp .env.example .env
```

2. Éditez `.env` avec vos vraies clés :
```bash
UNSPLASH_ACCESS_KEY=J52y_IWplzV6Wz6IsHpAr_TSkHEUTdQd8nvejL4X4PU
PIXABAY_API_KEY=52789824-40fb09218b750e39916fccc44
```

3. Testez localement avec `vercel dev` :
```bash
vercel dev
```
Ouvrez http://localhost:3000

### Option B : Via l'Interface Vercel (Production)

1. Allez sur [vercel.com](https://vercel.com)
2. Créez/ouvrez votre projet
3. Allez dans **Settings → Environment Variables**
4. Ajoutez :
   - **Name:** `UNSPLASH_ACCESS_KEY`
     **Value:** `J52y_IWplzV6Wz6IsHpAr_TSkHEUTdQd8nvejL4X4PU`
   - **Name:** `PIXABAY_API_KEY`
     **Value:** `52789824-40fb09218b750e39916fccc44`
5. Cochez **Production**, **Preview**, **Development**

## 📤 Étape 3 : Déployer

### Déploiement Preview (Test)

```bash
vercel
```

Cela crée un déploiement de test avec une URL unique :
`https://fiches-mots-abc123.vercel.app`

### Déploiement Production

Une fois que le test fonctionne :

```bash
vercel --prod
```

Votre app sera disponible sur :
`https://fiches-mots.vercel.app`

## 🔄 Méthode Alternative : GitHub Auto-Deploy

### 1. Pushez sur GitHub

```bash
git remote add origin https://github.com/VOTRE_USERNAME/fiches-mots.git
git push -u origin main
```

### 2. Connectez à Vercel

1. Allez sur [vercel.com/new](https://vercel.com/new)
2. Importez votre dépôt GitHub
3. Configurez :
   - **Framework Preset:** Other
   - **Root Directory:** `./`
   - **Build Command:** (laisser vide)
   - **Output Directory:** (laisser vide)

4. Ajoutez les variables d'environnement (voir Étape 2)

5. Cliquez **Deploy**

### 3. Auto-Deploy Activé

Chaque `git push` déclenchera automatiquement un nouveau déploiement ! 🎉

## ✅ Vérification Post-Déploiement

### 1. Testez les endpoints API

```bash
# Test Pixabay
curl "https://VOTRE-APP.vercel.app/api/pixabay?query=feuille&image_type=vector&per_page=3"

# Test Unsplash
curl "https://VOTRE-APP.vercel.app/api/unsplash?query=feuille&per_page=3"
```

Vous devriez recevoir du JSON avec des URLs d'images.

### 2. Testez l'application

1. Ouvrez `https://VOTRE-APP.vercel.app`
2. Entrez un thème : "automne"
3. Entrez des mots : "feuille, champignon, citrouille"
4. Cliquez "🔍 Rechercher les images"
5. Vérifiez que les images se chargent correctement

## 🛠️ Développement Local

### Avec fonctions serverless :

```bash
# 1. Créez .env avec vos clés
cp .env.example .env
nano .env

# 2. Lancez le serveur de dev Vercel
vercel dev

# 3. Ouvrez http://localhost:3000
```

### Sans fonctions serverless (mode classique) :

```bash
# Utilisez imageSearch.js au lieu de imageSearch.serverless.js
cd web
python3 -m http.server 8000
# Ouvrez http://localhost:8000
```

## 🔧 Dépannage

### Erreur : "API key not configured"

**Cause** : Les variables d'environnement ne sont pas définies dans Vercel.

**Solution** :
1. Vérifiez Settings → Environment Variables dans Vercel
2. Redéployez après avoir ajouté les variables

### Erreur : "Failed to fetch"

**Cause** : L'URL de l'endpoint est incorrecte.

**Solution** :
- En dev local : Vérifiez que `vercel dev` tourne sur le port 3000
- En production : Vérifiez que `imageSearch.serverless.js` est utilisé

### Images ne se chargent pas

**Cause** : Mauvaise référence au fichier JS.

**Solution** :
- Vérifiez que `index.html` charge `imageSearch.serverless.js`
- Vérifiez la console du navigateur pour les erreurs

## 📊 Limites Vercel (Plan Gratuit)

- ✅ 100 GB de bande passante par mois
- ✅ 100 heures de fonction serverless par mois
- ✅ Déploiements illimités

Pour une classe de maternelle → **largement suffisant** ! 🎯

## 🎓 Utilisation en Classe

Une fois déployé, partagez simplement l'URL avec vos collègues :
```
https://fiches-mots.vercel.app
```

Pas besoin d'installation, tout fonctionne dans le navigateur !

## 🔒 Sécurité des Clés API

Même avec les fonctions serverless, il est recommandé de :

### Pixabay
- Pas de restriction nécessaire (clé publique)

### Unsplash
1. Allez dans [Unsplash Developers](https://unsplash.com/oauth/applications)
2. Ouvrez votre application
3. Ajoutez votre domaine Vercel dans "Authorized JavaScript origins"

## 📚 Ressources

- [Documentation Vercel Serverless](https://vercel.com/docs/serverless-functions/introduction)
- [Variables d'environnement Vercel](https://vercel.com/docs/environment-variables)
- [API Pixabay](https://pixabay.com/api/docs/)
- [API Unsplash](https://unsplash.com/documentation)

---

Besoin d'aide ? Ouvrez une issue sur GitHub ! 🚀
