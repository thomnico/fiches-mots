# 📚 Générateur de Fiches Pédagogiques pour la Maternelle

Générateur de fiches pédagogiques au format PDF avec polices dyslexiques (OpenDyslexic) et cursive scolaire (Écolier).

## 🎯 Deux versions disponibles

### 🐍 Version Python (Ligne de commande)
Script automatisé avec recherche d'images avancée
- Recherche automatique via PublicDomainVectors, OpenClipart, Google Images
- Priorisation des stickers Freepik
- Support SVG avec conversion automatique
- Génération batch

### 🌐 Version Web (Interface graphique)
Application web interactive sans installation
- Interface intuitive (aucune compétence technique requise)
- Sélection visuelle : 3 images au choix par mot
- Recherche d'images via Unsplash Source
- Génération PDF côté client

## ⚡ Démarrage rapide

### Version Python

```bash
# Installation
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

# Utilisation
python3 generate_fiches.py mots_animaux.txt
# → Génère output/fiches_animaux.pdf
```

### Version Web (Développement Local)

```bash
# Méthode recommandée: Serveur Vercel Dev (avec fonctions serverless)
npm install -g vercel
npm run dev
# → http://localhost:3000

# Alternative: Serveur HTTP simple (sans API sécurisées)
cd web/
python3 -m http.server 8000
# → http://localhost:8000
```

### Déploiement sur Vercel (Production)

```bash
# Déploiement en 3 commandes
npm install -g vercel
vercel  # Preview
vercel --prod  # Production
```

📚 **Documentation complète** : [README_DEPLOIEMENT_VERCEL.md](./README_DEPLOIEMENT_VERCEL.md)

## 📖 Utilisation

### Format des fichiers de mots

Créez un fichier texte avec un mot par ligne :

```
chat
chien
oiseau
poisson
```

Le nom du fichier définit le thème : `mots_THEME.txt` (ex: `mots_animaux.txt`)

### Exemples fournis

- **mots_automne.txt** : feuille, champignon, citrouille, marron
- **mots_animaux.txt** : chat, chien, oiseau, poisson  
- **mots_noel.txt** : sapin, cadeau, étoile, neige

## 🎨 Caractéristiques

### Polices spécialisées

- **CAPITALES** : OpenDyslexic Bold (32pt) - Facilite la lecture pour les dyslexiques
- **script** : OpenDyslexic Regular (28pt) - Police sans empattement adaptée
- **cursif** : Écolier (32pt) - Cursive officielle de l'école française

### Accessibilité

✅ Contraste WCAG AAA (noir pur #000 sur blanc)  
✅ Bordures noires autour des images (2pt)  
✅ Espacement généreux (1.5cm entre éléments)  
✅ 2 mots par page A4 (évite la surcharge cognitive)  
✅ Tailles de police optimales (28-32pt)

### Format PDF

- Format A4 portrait
- 2 mots par page
- Pour chaque mot :
  - Image illustrative
  - Mot en CAPITALES
  - Mot en script (minuscules)
  - Mot en cursif

## 📂 Structure du projet

```
fiches-mots/
├── generate_fiches.py       # Script Python
├── requirements.txt          # Dépendances
├── mots_*.txt               # Fichiers de mots
├── output/                   # PDFs générés
├── fonts/                    # Polices TTF
│   ├── capital.ttf          # OpenDyslexic Bold
│   ├── script.ttf           # OpenDyslexic Regular
│   └── cursive.ttf          # Écolier
├── web/                      # Version web
│   ├── index.html
│   ├── css/style.css
│   ├── js/
│   │   ├── app.js
│   │   ├── config.js
│   │   ├── imageSearch.js
│   │   └── pdfGenerator.js
│   └── fonts/               # Polices (copie)
└── test_web.py              # Tests Playwright

```

## 🧪 Tests

### Tests automatisés (Playwright)

```bash
pip install playwright
playwright install chromium
python3 test_web.py
```

Les captures d'écran sont sauvegardées dans `web/screenshots/`

## 📚 Documentation

- **[COMPARAISON.md](COMPARAISON.md)** - Python vs Web : quel version choisir ?
- **[ACCESSIBILITE.md](ACCESSIBILITE.md)** - Fonctionnalités d'accessibilité
- **[THEMES.md](THEMES.md)** - Guide des thèmes et traductions
- **[CLAUDE.md](CLAUDE.md)** - Instructions du projet
- **[web/README.md](web/README.md)** - Documentation version web

## 🔧 Configuration

### Ajouter des traductions

Modifiez dans `generate_fiches.py` (Python) ou `js/config.js` (Web) :

```python
word_translations = {
    'nouveaumot': 'english_translation',
    # ...
}
```

### Personnaliser les thèmes

```python
theme_translations = {
    'nouveautheme': 'english theme',
    # ...
}
```

## 🌐 Déploiement web

La version web est 100% statique :

**GitHub Pages (gratuit)**
```bash
# Pousser web/ sur GitHub
# Activer Pages dans Settings
```

**Netlify / Vercel (gratuit)**
1. Créer un compte
2. Déployer le dossier `web/`
3. URL personnalisée disponible

## ⚠️ Notes importantes

### Version Web - Images

- **APIs utilisées** : Pixabay (vecteurs prioritaires) + Unsplash (photos fallback)
- **Sécurité** : Clés API protégées par fonctions serverless Vercel
- **Pagination** : 20+ images par mot, 3 affichées à la fois
- **Nécessite une connexion internet**
- Les images peuvent prendre quelques secondes à charger

### Version Python - Images

- Recherche sur 3 sources : PublicDomainVectors, OpenClipart, Google Images
- **Meilleure qualité et pertinence des images**
- Priorise les stickers Freepik via Google
- Certains sites peuvent bloquer les requêtes (rate limiting)

## 🐛 Résolution de problèmes

**Python: "Module not found"**
```bash
source venv/bin/activate
pip install -r requirements.txt
```

**Python: Aucune image trouvée**
- Vérifiez votre connexion internet
- Attendez quelques secondes entre les générations (rate limiting)

**Web: Les images ne se chargent pas**
- Vérifiez votre connexion internet
- Rechargez la page (F5)
- Les images Unsplash peuvent prendre 5-10 secondes

**Web: Le PDF ne se génère pas**
- Vérifiez que toutes les images sont sélectionnées
- Ouvrez la console (F12) pour voir les erreurs
- Essayez avec moins de mots (max 20 recommandé)

## 💡 Recommandations d'utilisation

### Pour les enseignants
1. **Découverte** : Version Web (simple, immédiat)
2. **Production** : Version Python (qualité, batch)

### Pour les parents
- **Version Web** : Plus accessible, pas d'installation

### Pour les développeurs
- **Version Python** : Automatisation, scripts
- **Version Web** : Démonstration, prototype

## 📊 Comparatif rapide

| Aspect | Python | Web |
|--------|--------|-----|
| Installation | Python + pip | Aucune |
| Qualité images | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ |
| Choix images | Auto (1ère) | Manuel (3 choix) |
| Batch | ✅ Oui | ❌ Non |
| Accessibilité | Technique | Grand public |

## 🤝 Contribution

Les contributions sont bienvenues ! Consultez [CLAUDE.md](CLAUDE.md) pour les règles.

## 📄 Licence

- **Code** : Open source éducatif
- **Polices** :
  - OpenDyslexic : Open Font License (OFL)
  - Écolier : Licence libre

## 👏 Crédits

- OpenDyslexic pour les polices dyslexiques
- Écolier pour la cursive scolaire française
- Freepik, OpenClipart, PublicDomainVectors, Unsplash pour les images

---

**Créé pour faciliter l'apprentissage en maternelle avec des outils accessibles !** 🎓✨
