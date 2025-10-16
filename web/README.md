# Générateur de Fiches Pédagogiques - Version Web

Interface web interactive pour générer des fiches pédagogiques pour la maternelle française.

## 🎨 Fonctionnalités

- **Interface intuitive** : Pas besoin de connaissances techniques
- **Recherche d'images automatique** : 3 propositions par mot
- **Sélection visuelle** : Choisissez l'image qui vous convient
- **Polices adaptées** :
  - CAPITALES : OpenDyslexic Bold (dyslexie)
  - script : OpenDyslexic Regular (dyslexie)
  - cursif : Écolier (cursive scolaire)
- **Génération PDF** : Téléchargement automatique
- **Accessibilité** : Contrastes élevés, bordures autour des images

## 🚀 Utilisation

### Démarrage rapide

1. Ouvrez `index.html` dans votre navigateur web
2. Entrez un thème (optionnel) : automne, animaux, noël...
3. Saisissez vos mots (un par ligne)
4. Cliquez sur "🔍 Rechercher les images"
5. Choisissez une image pour chaque mot parmi les 3 propositions
6. Cliquez sur "📄 Générer le PDF"
7. Le PDF se télécharge automatiquement !

### Exemple d'utilisation

```
Thème: automne

Mots:
feuille
champignon
citrouille
marron
```

Le système recherchera automatiquement 3 images pour chaque mot en contexte (avec le thème "automne").

## 📂 Structure du projet

```
web/
├── index.html           # Page principale
├── css/
│   └── style.css       # Styles de l'interface
├── js/
│   ├── config.js       # Configuration et traductions
│   ├── imageSearch.js  # Module de recherche d'images
│   ├── pdfGenerator.js # Génération des PDFs
│   └── app.js          # Application principale
└── fonts/
    ├── capital.ttf     # OpenDyslexic Bold
    ├── script.ttf      # OpenDyslexic Regular
    └── cursive.ttf     # Écolier cursive
```

## 🔧 Configuration avancée

### Modifier le nombre d'images proposées

Dans `js/config.js`, changez :
```javascript
imagesPerWord: 3  // Nombre d'images par mot
```

### Ajouter des traductions

Dans `js/config.js`, ajoutez vos traductions :
```javascript
wordTranslations: {
    'nouveaumot': 'translation',
    // ...
}
```

### API d'images

Par défaut, l'application utilise Unsplash (gratuit, sans inscription).

Pour production, obtenez une clé API gratuite sur :
- [Unsplash Developers](https://unsplash.com/developers)

Remplacez `client_id=demo` dans `imageSearch.js` par votre clé.

## 🌐 Déploiement

### GitHub Pages (gratuit)

1. Créez un repo GitHub
2. Uploadez le dossier `web/`
3. Activez GitHub Pages dans Settings
4. Votre app sera disponible à : `https://username.github.io/repo-name/`

### Netlify / Vercel (gratuit)

1. Créez un compte sur [Netlify](https://netlify.com) ou [Vercel](https://vercel.com)
2. Déployez le dossier `web/`
3. URL personnalisée disponible en quelques secondes

### Serveur local

```bash
# Python 3
cd web/
python3 -m http.server 8000

# Accès: http://localhost:8000
```

## 🎯 Comparaison avec la version Python

| Fonctionnalité | Python | Web |
|----------------|--------|-----|
| Installation | Python + pip | Aucune |
| Interface | Ligne de commande | Graphique |
| Sélection images | Automatique (1ère) | Interactive (3 choix) |
| Polices | ✅ Identiques | ✅ Identiques |
| Format PDF | ✅ | ✅ |
| Accessibilité | ✅ | ✅ |
| Thèmes | ✅ | ✅ |
| Utilisateurs | Techniques | Tous publics |

## 📝 Notes techniques

### Polices

Les polices TTF sont chargées dynamiquement et intégrées au PDF via jsPDF.

### Images

- Recherche via API Unsplash (gratuit)
- Conversion en Data URL pour intégration PDF
- Support CORS via proxy si nécessaire

### Compatibilité navigateurs

- ✅ Chrome 90+
- ✅ Firefox 88+
- ✅ Safari 14+
- ✅ Edge 90+

### Limitations

- Taille PDF limitée par la mémoire navigateur (~50 mots max recommandé)
- Recherche d'images nécessite une connexion internet
- CORS peut bloquer certaines images (utilise fallback)

## 🐛 Résolution de problèmes

### Les images ne se chargent pas

- Vérifiez votre connexion internet
- Certaines images peuvent être bloquées par CORS
- L'app utilise des placeholders en cas d'échec

### Le PDF ne se génère pas

- Vérifiez que toutes les images sont sélectionnées
- Ouvrez la console navigateur (F12) pour voir les erreurs
- Essayez avec moins de mots (max 20-30)

### Les polices n'apparaissent pas

- Vérifiez que les fichiers TTF sont dans `fonts/`
- Rechargez la page (Ctrl+F5)
- Testez avec un autre navigateur

## 📄 Licence

Même licence que le projet Python principal.

Polices :
- OpenDyslexic : Open Font License
- Écolier : Licence libre

## 🤝 Contribution

Pour améliorer l'application :
1. Ajoutez de nouveaux moteurs de recherche d'images
2. Améliorez l'interface utilisateur
3. Ajoutez des thèmes prédéfinis
4. Optimisez la génération PDF

---

**Version Web** - Basée sur le script Python `generate_fiches.py`
