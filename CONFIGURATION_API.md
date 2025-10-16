# 🔐 Configuration Sécurisée des Clés API

## ⚠️ IMPORTANT : Sécurité des Clés

**NE JAMAIS** :
- ❌ Committer vos clés API dans Git
- ❌ Partager vos clés publiquement
- ❌ Mettre vos clés dans des fichiers .md, .js non ignorés

**TOUJOURS** :
- ✅ Utiliser des variables d'environnement (.env)
- ✅ Vérifier que .env est dans .gitignore
- ✅ Utiliser .env.example comme template

## 🚀 Configuration Initiale

### Étape 1 : Obtenir vos clés API

#### Pixabay
1. Créez un compte sur https://pixabay.com/accounts/register/
2. Allez sur https://pixabay.com/api/docs/
3. Copiez votre clé API

#### Unsplash
1. Créez un compte sur https://unsplash.com/join
2. Allez sur https://unsplash.com/oauth/applications
3. Créez une nouvelle application ("New Application")
4. Remplissez les informations :
   - **Application name** : Fiches Maternelle
   - **Description** : Générateur de fiches pédagogiques
5. Copiez votre **Access Key**

### Étape 2 : Configurer le fichier .env

```bash
# Copiez le template
cp .env.example .env

# Éditez avec vos clés
nano .env
```

Contenu du fichier `.env` :
```bash
PIXABAY_API_KEY=VOTRE_NOUVELLE_CLE_PIXABAY
UNSPLASH_ACCESS_KEY=VOTRE_NOUVELLE_CLE_UNSPLASH
```

### Étape 3 : Vérifier la configuration

```bash
# Vérifiez que .env n'est PAS dans git
git status

# .env ne doit PAS apparaître dans la liste
# Si il apparaît, c'est qu'il n'est pas dans .gitignore !
```

## 🐍 Utilisation avec Python

Le script `generate_fiches.py` charge automatiquement les clés depuis `.env` :

```python
self.pixabay_api_key = os.getenv('PIXABAY_API_KEY', '')
self.unsplash_access_key = os.getenv('UNSPLASH_ACCESS_KEY', '')
```

### Test rapide :

```bash
source venv/bin/activate
python3 generate_fiches.py mots_automne.txt
```

Si vous voyez :
```
🔑 Pixabay API: ✅
🔑 Unsplash API: ✅
```
C'est bon ! ✅

Si vous voyez :
```
🔑 Pixabay API: ❌
🔑 Unsplash API: ❌
```
Vérifiez votre fichier .env ⚠️

## 🌐 Utilisation avec Vercel (Web)

### Développement Local

```bash
# 1. Créez .env avec vos clés (voir Étape 2)
cp .env.example .env
nano .env

# 2. Lancez Vercel Dev
vercel dev

# 3. Testez sur http://localhost:3000
```

### Production Vercel

1. Allez sur https://vercel.com
2. Ouvrez votre projet
3. Allez dans **Settings → Environment Variables**
4. Ajoutez vos clés :
   - `PIXABAY_API_KEY` = votre nouvelle clé
   - `UNSPLASH_ACCESS_KEY` = votre nouvelle clé
5. Cochez **Production**, **Preview**, **Development**
6. Redéployez : `vercel --prod`

## 🔄 Rotation des Clés (Si Compromises)

Si vos clés ont été exposées publiquement :

### 1. Révoquer immédiatement

**Pixabay** :
- Allez sur https://pixabay.com/api/docs/
- Générez une nouvelle clé (l'ancienne sera invalidée)

**Unsplash** :
- Allez sur https://unsplash.com/oauth/applications
- Ouvrez votre app
- Cliquez "Regenerate Access Key"

### 2. Mettre à jour partout

**Fichier local .env** :
```bash
nano .env
# Remplacez par les nouvelles clés
```

**Vercel (si déployé)** :
1. Settings → Environment Variables
2. Supprimez les anciennes
3. Ajoutez les nouvelles
4. Redéployez : `vercel --prod`

### 3. Vérifier l'historique Git

```bash
# Chercher les anciennes clés dans l'historique
git log -S "ancienne_clé" --all --oneline
```

Si vous trouvez des commits, voir [SECURITE_GIT.md](./SECURITE_GIT.md)

## ✅ Checklist de Sécurité

Avant chaque commit :

- [ ] `.env` est dans .gitignore
- [ ] Aucune clé dans les fichiers .md
- [ ] Aucune clé dans les fichiers .js (sauf config.api.js qui est ignoré)
- [ ] Aucune clé dans les fichiers .py
- [ ] `git status` ne montre pas .env

Avant chaque déploiement :

- [ ] Variables d'environnement configurées sur Vercel
- [ ] Test local avec `vercel dev` fonctionne
- [ ] Aucune clé visible dans le code source public

## 📚 Ressources

- [Guide .env pour débutants](https://www.freecodecamp.org/news/how-to-use-environment-variables/)
- [Sécurité des clés API](https://www.freecodecamp.org/news/how-to-securely-store-api-keys-4ff3ea19ebda/)
- [Documentation Vercel Environment Variables](https://vercel.com/docs/environment-variables)

## 🆘 Aide

En cas de problème :

1. Vérifiez que .env existe : `ls -la .env`
2. Vérifiez le contenu : `cat .env`
3. Testez les clés manuellement :
   ```bash
   curl "https://pixabay.com/api/?key=VOTRE_CLE&q=test"
   curl -H "Authorization: Client-ID VOTRE_CLE" "https://api.unsplash.com/photos/random"
   ```

---

**Règle d'or** : Si vous avez un doute, NE COMMITEZ PAS ! 🔒
