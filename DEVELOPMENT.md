# 💻 Développement Local

## 🚀 Démarrage Rapide

### 1. Clonez le projet

```bash
git clone https://github.com/VOTRE_USERNAME/fiches-mots.git
cd fiches-mots
```

### 2. Configurez les clés API

Le fichier `.env` est déjà créé avec vos clés. Vérifiez qu'il contient :

```bash
cat .env
```

Devrait afficher :
```
UNSPLASH_ACCESS_KEY=votre_clé_unsplash_ici
PIXABAY_API_KEY=votre_clé_pixabay_ici
```

### 3. Installez Vercel CLI

```bash
npm install -g vercel
```

### 4. Lancez le serveur de développement

```bash
npm run dev
```

Ou directement :
```bash
vercel dev
```

L'application sera disponible sur : **http://localhost:3000**

## 🔧 Comment ça marche ?

### Architecture

```
┌─────────────────┐
│  Navigateur     │
│  localhost:3000 │
└────────┬────────┘
         │
         │ GET /api/pixabay?query=feuille
         ▼
┌─────────────────┐
│  Vercel Dev     │  ← Lit .env pour les clés API
│  (Local)        │
└────────┬────────┘
         │
         │ Appel API avec clé sécurisée
         ▼
┌─────────────────┐
│  Pixabay /      │
│  Unsplash       │
└─────────────────┘
```

### Fichiers importants

- `api/pixabay.js` - Fonction serverless pour Pixabay
- `api/unsplash.js` - Fonction serverless pour Unsplash
- `web/js/imageSearch.serverless.js` - Client qui appelle /api/*
- `.env` - Variables d'environnement locales (git-ignoré)

## 📝 Commandes Utiles

```bash
# Développement local
npm run dev                  # Lance vercel dev

# Tests
python3 test_pagination.py   # Test de pagination

# Déploiement
npm run deploy               # Preview deployment
npm run deploy:prod          # Production deployment
```

## 🔍 Déboguer les API

### Tester l'endpoint Pixabay

```bash
curl "http://localhost:3000/api/pixabay?query=feuille&image_type=vector&per_page=3"
```

### Tester l'endpoint Unsplash

```bash
curl "http://localhost:3000/api/unsplash?query=feuille&per_page=3"
```

## 🐛 Problèmes Courants

### "API key not configured"

**Cause** : Le fichier `.env` n'existe pas ou est mal configuré.

**Solution** :
```bash
# Vérifiez que .env existe
ls -la .env

# Vérifiez son contenu
cat .env

# Si nécessaire, recréez-le
cp .env.example .env
nano .env  # Ajoutez vos clés
```

### "Port 3000 already in use"

**Cause** : Un autre processus utilise le port 3000.

**Solution** :
```bash
# Trouvez et tuez le processus
lsof -ti:3000 | xargs kill -9

# Ou utilisez un autre port
vercel dev --listen 3001
```

### Images ne se chargent pas

**Vérifications** :
1. Vérifiez que `vercel dev` tourne
2. Ouvrez la console du navigateur (F12)
3. Vérifiez les erreurs réseau
4. Testez les endpoints avec curl (voir ci-dessus)

## 🔄 Workflow de Développement

1. **Modifiez le code** (JavaScript, CSS, HTML)
2. **Rechargez le navigateur** (Ctrl+R)
3. **Vercel Dev recharge automatiquement** les fonctions serverless
4. **Testez vos modifications**
5. **Committez** :
   ```bash
   git add .
   git commit -m "Description des changements"
   ```
6. **Déployez** (optionnel) :
   ```bash
   npm run deploy
   ```

## 📦 Structure du Projet

```
fiches-mots/
├── api/                      # Backend serverless
│   ├── pixabay.js
│   └── unsplash.js
├── web/                      # Frontend
│   ├── index.html
│   ├── css/
│   │   └── style.css
│   ├── js/
│   │   ├── config.js
│   │   ├── imageSearch.serverless.js  ← Utilisé
│   │   ├── imageSearch.js             ← Ancien (clés exposées)
│   │   ├── pdfGenerator.js
│   │   └── app.js
│   └── fonts/
├── .env                      # Clés API (git-ignoré)
├── .env.example              # Template
├── vercel.json               # Config Vercel
└── package.json              # Scripts npm
```

## 🚀 Prêt à Déployer ?

Voir [README_DEPLOIEMENT_VERCEL.md](./README_DEPLOIEMENT_VERCEL.md)

---

Happy coding! 🎨
