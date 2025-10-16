# Configuration des Clés API

## ⚠️ IMPORTANT - Sécurité

**NE COMMITTEZ JAMAIS vos clés API dans git!**

Le fichier `js/config.api.js` est ignoré par git (`.gitignore`) pour protéger vos clés.

## Installation

### 1. Copier le fichier de configuration exemple

```bash
cd web/js
cp config.api.example.js config.api.js
```

### 2. Obtenir vos clés API (gratuites)

#### Unsplash API
1. Créez un compte sur [Unsplash Developers](https://unsplash.com/developers)
2. Créez une nouvelle application
3. Copiez votre **Access Key**
4. Limite: 50 requêtes/heure (gratuit)

#### Pixabay API
1. Créez un compte sur [Pixabay](https://pixabay.com/api/docs/)
2. Copiez votre **API Key** depuis votre profil
3. Limite: 100 requêtes/heure (gratuit)

### 3. Configurer vos clés

Éditez `web/js/config.api.js` et remplacez les valeurs:

```javascript
const API_CONFIG = {
    unsplash: {
        accessKey: 'VOTRE_CLE_UNSPLASH_ICI'
    },
    pixabay: {
        apiKey: 'VOTRE_CLE_PIXABAY_ICI'
    }
};
```

### 4. Vérifier la configuration

Lancez le serveur:

```bash
cd web/
./start.sh
```

Ouvrez http://localhost:8000 dans votre navigateur.

Si les clés sont mal configurées, vous verrez une erreur dans la console du navigateur.

## Structure des fichiers

```
web/
├── js/
│   ├── config.api.example.js  ← Exemple (committé dans git)
│   └── config.api.js          ← VOS CLÉS (ignoré par git)
├── .gitignore                 ← Ignore config.api.js
└── CONFIGURATION.md           ← Ce fichier
```

## Résolution de problèmes

### Erreur: "Configuration API manquante"
→ Vous n'avez pas créé le fichier `config.api.js`
→ Solution: Copiez `config.api.example.js` vers `config.api.js`

### Erreur: "Clés API non configurées"
→ Vous avez laissé les valeurs par défaut (`YOUR_...`)
→ Solution: Remplacez par vos vraies clés API

### Erreur: "Unsplash API error: 401"
→ Votre clé Unsplash est invalide
→ Solution: Vérifiez votre clé sur https://unsplash.com/oauth/applications

### Erreur: "Pixabay API error: 400"
→ Votre clé Pixabay est invalide
→ Solution: Vérifiez votre clé sur https://pixabay.com/api/docs/
