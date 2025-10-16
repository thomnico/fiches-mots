# 🚀 Déploiement Rapide sur Vercel

## ⚡ Méthode la Plus Simple (5 minutes)

### 1️⃣ Modifiez `web/index.html`

Ligne ~60, changez :
```html
<script src="js/imageSearch.js"></script>
```
Par :
```html
<script src="js/imageSearch.serverless.js"></script>
```

### 2️⃣ Installez et déployez

```bash
npm install -g vercel
vercel login
vercel
```

### 3️⃣ Configurez les clés API

Sur [vercel.com](https://vercel.com), allez dans votre projet → **Settings → Environment Variables**

Ajoutez :
- `UNSPLASH_ACCESS_KEY` = `votre_clé_unsplash_ici`
- `PIXABAY_API_KEY` = `votre_clé_pixabay_ici`

### 4️⃣ Redéployez

```bash
vercel --prod
```

## ✅ C'est fait !

Votre app est sur : `https://fiches-mots.vercel.app`

---

**📘 Guide détaillé** : Voir [DEPLOIEMENT_VERCEL_SERVERLESS.md](./DEPLOIEMENT_VERCEL_SERVERLESS.md)
