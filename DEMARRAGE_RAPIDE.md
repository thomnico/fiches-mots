# ⚡ Démarrage Rapide - Fiches Pédagogiques

## 🚨 IMPORTANT : Utiliser le Bon Serveur

### ❌ NE PAS utiliser

```bash
# NE FONCTIONNE PAS avec les fonctions serverless
python3 -m http.server 8000
cd web && python3 -m http.server
```

**Problème** : Ce serveur simple ne peut pas exécuter les fonctions API serverless, donc **les images ne se chargeront pas**.

### ✅ À UTILISER

```bash
# Méthode correcte pour le développement local
vercel dev --listen 3000
```

**Avantage** : Lance les fonctions serverless localement avec les clés API sécurisées.

---

## 🚀 Instructions Complètes

### 1️⃣ Arrêter tout serveur existant

```bash
# Trouver les processus Python
ps aux | grep python | grep http.server

# Les tuer (remplacez PID par le numéro de processus)
kill PID
```

### 2️⃣ Lancer Vercel Dev

```bash
vercel dev --listen 3000
```

Attendez le message :
```
✅ Ready! Available at http://localhost:3000
```

### 3️⃣ Ouvrir l'Application

Ouvrez votre navigateur sur :
**http://localhost:3000**

---

## 🔍 Vérifier que ça Marche

### Test dans le Navigateur

1. Allez sur `http://localhost:3000`
2. Entrez un thème : **automne**
3. Entrez des mots : **feuille, champignon, citrouille**
4. Cliquez sur **🔍 Rechercher les images**
5. Les images devraient apparaître après quelques secondes

### Test via Terminal

```bash
# Tester Pixabay
curl "http://localhost:3000/api/pixabay?query=feuille&image_type=vector&per_page=3"

# Tester Unsplash
curl "http://localhost:3000/api/unsplash?query=feuille&per_page=3"
```

Si vous voyez du JSON avec des URLs d'images → **✅ Ça marche !**

---

## 🐛 Problèmes Courants

### "Cannot GET /api/pixabay"

**Cause** : Vous utilisez `python -m http.server` au lieu de `vercel dev`

**Solution** :
```bash
# 1. Tuer le serveur Python
ps aux | grep http.server
kill PID

# 2. Lancer Vercel Dev
vercel dev --listen 3000
```

### "API key not configured"

**Cause** : Le fichier `.env` n'existe pas ou est vide

**Solution** :
```bash
# Vérifier que .env existe
cat .env

# Devrait afficher:
# UNSPLASH_ACCESS_KEY=votre_clé_unsplash_ici
# PIXABAY_API_KEY=votre_clé_pixabay_ici
```

Si le fichier n'existe pas :
```bash
cp .env.example .env
# Puis éditez .env avec vos clés
```

### Port 3000 déjà utilisé

**Solution** :
```bash
# Tuer le processus sur le port 3000
lsof -ti:3000 | xargs kill -9

# Ou utiliser un autre port
vercel dev --listen 3001
```

### Les images ne se chargent toujours pas

**Vérifications** :

1. **Console du navigateur** (F12 → Console)
   - Cherchez les erreurs rouges
   - Vérifiez que les appels à `/api/pixabay` et `/api/unsplash` aboutissent

2. **Logs Vercel Dev**
   - Dans le terminal où tourne `vercel dev`
   - Vérifiez qu'il n'y a pas d'erreurs

3. **Vérifiez l'URL**
   - Assurez-vous d'être sur `localhost:3000` (pas 8000)

---

## 📖 Documentation Complète

- [DEVELOPMENT.md](./DEVELOPMENT.md) - Guide développement complet
- [README_DEPLOIEMENT_VERCEL.md](./README_DEPLOIEMENT_VERCEL.md) - Déploiement production

---

## 🎯 Résumé en 3 Commandes

```bash
# 1. Aller dans le dossier du projet
cd /Volumes/sidecar/src/fiches-mots

# 2. Lancer le serveur Vercel
vercel dev --listen 3000

# 3. Ouvrir le navigateur
open http://localhost:3000
```

C'est tout ! 🎉
