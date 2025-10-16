# 📚 Générateur de Fiches Pédagogiques - Projet Complet

Générateur de fiches pédagogiques pour la maternelle française avec support des polices dyslexiques et accessibilité optimale.

## 🎯 Vue d'ensemble

Ce projet propose **deux versions** complémentaires pour générer des fiches pédagogiques au format PDF :

1. **Version Python** (`generate_fiches.py`) - Ligne de commande, automatisation
2. **Version Web** (`web/`) - Interface graphique interactive

Les deux versions utilisent les mêmes polices (OpenDyslexic + Écolier) et génèrent des PDFs identiques.

## 📋 Table des matières

- [Installation](#installation)
- [Utilisation rapide](#utilisation-rapide)
- [Version Python](#version-python)
- [Version Web](#version-web)
- [Tests](#tests)
- [Structure du projet](#structure-du-projet)
- [Documentation](#documentation)

## 🚀 Installation

### Prérequis
- Python 3.8+ (pour version Python et tests)
- Navigateur web moderne (Chrome, Firefox, Safari, Edge)

### Installation complète

```bash
# Cloner ou télécharger le projet
cd fiches-mots/

# Créer l'environnement virtuel Python
python3 -m venv venv
source venv/bin/activate  # Sur Windows: venv\Scripts\activate

# Installer les dépendances
pip install -r requirements.txt

# Optionnel: Installer Playwright pour les tests web
pip install playwright
playwright install chromium
```

## ⚡ Utilisation rapide

### Version Python (Ligne de commande)

```bash
# Activer l'environnement virtuel
source venv/bin/activate

# Générer des fiches avec les mots d'exemple
python3 generate_fiches.py mots_automne.txt

# Le PDF sera créé dans output/fiches_automne.pdf
```

### Version Web (Interface graphique)

```bash
# Démarrer le serveur local
cd web/
./start.sh

# Ouvrir dans votre navigateur
# http://localhost:8000
```

Ou simplement double-cliquer sur `web/index.html`

## 🐍 Version Python

### Caractéristiques

- ✅ Recherche automatique d'images (PublicDomainVectors, OpenClipart, Google Images)
- ✅ Génération batch (plusieurs fichiers)
- ✅ Support SVG avec conversion automatique
- ✅ Priorisation des stickers Freepik
- ✅ Scriptable et automatisable

### Utilisation détaillée

```bash
# Syntaxe de base
python3 generate_fiches.py <fichier_mots> [fichier_sortie]

# Exemples
python3 generate_fiches.py mots_automne.txt
python3 generate_fiches.py mots_animaux.txt output/mes_fiches.pdf
python3 generate_fiches.py mots_noel.txt
```

### Format des fichiers de mots

Créez un fichier texte avec un mot par ligne :

```
# mots_animaux.txt
chat
chien
oiseau
poisson
```

Le thème est détecté automatiquement depuis le nom du fichier (`mots_THEME.txt`).

### Exemples fournis

- `mots_automne.txt` - feuille, champignon, citrouille, marron
- `mots_animaux.txt` - chat, chien, oiseau, poisson
- `mots_noel.txt` - sapin, cadeau, étoile, neige

## 🌐 Version Web

### Caractéristiques

- ✅ Interface intuitive (aucune connaissance technique requise)
- ✅ Sélection visuelle d'images (3 choix par mot)
- ✅ Prévisualisation en temps réel
- ✅ Recherche d'images via Pixabay API
- ✅ Génération PDF côté client (pas de serveur nécessaire)
- ✅ Responsive (mobile, tablette, desktop)

### Workflow utilisateur

1. **Étape 1** : Entrer le thème (optionnel) et les mots
2. **Étape 2** : L'app recherche 3 images pour chaque mot
3. **Étape 3** : Cliquer sur l'image préférée pour chaque mot
4. **Étape 4** : Générer et télécharger le PDF

### Déploiement

La version web est 100% statique et peut être hébergée gratuitement :

**GitHub Pages :**
```bash
# Pousser le dossier web/ sur GitHub
# Activer GitHub Pages dans Settings
# URL: https://username.github.io/repo-name/
```

**Netlify / Vercel :**
1. Créer un compte gratuit
2. Déployer le dossier `web/`
3. URL personnalisée en quelques secondes

## 🧪 Tests

### Tests automatisés avec Playwright

```bash
# Installer Playwright (si pas déjà fait)
pip install playwright
playwright install chromium

# Lancer les tests
python3 test_web.py

# Les captures d'écran seront dans web/screenshots/
```

Les tests vérifient :
- ✅ Chargement de la page
- ✅ Formulaire de saisie
- ✅ Recherche d'images
- ✅ Sélection d'images
- ✅ Génération PDF

### Tests manuels

**Version Python :**
```bash
python3 generate_fiches.py mots_animaux.txt
# Ouvrir output/fiches_animaux.pdf
```

**Version Web :**
```bash
cd web/
./start.sh
# Tester dans le navigateur
```

## 📁 Structure du projet

```
fiches-mots/
│
├── 🐍 VERSION PYTHON
│   ├── generate_fiches.py          # Script principal (570 lignes)
│   ├── requirements.txt             # Dépendances Python
│   ├── mots_automne.txt            # Exemple: thème automne
│   ├── mots_animaux.txt            # Exemple: thème animaux
│   ├── mots_noel.txt               # Exemple: thème Noël
│   └── output/                      # PDFs générés
│       ├── fiches_automne.pdf
│       ├── fiches_animaux.pdf
│       └── fiches_noel.pdf
│
├── 🌐 VERSION WEB
│   └── web/
│       ├── index.html               # Page principale
│       ├── start.sh                 # Script de démarrage
│       ├── README.md                # Documentation web
│       ├── css/
│       │   └── style.css           # Styles (5.7 Ko)
│       ├── js/
│       │   ├── config.js           # Configuration (2.0 Ko)
│       │   ├── imageSearch.js      # Recherche images (5.9 Ko)
│       │   ├── pdfGenerator.js     # Génération PDF (7.8 Ko)
│       │   └── app.js              # App principale (9.9 Ko)
│       ├── fonts/                   # Polices (192 Ko)
│       │   ├── capital.ttf
│       │   ├── script.ttf
│       │   └── cursive.ttf
│       └── screenshots/             # Captures de test
│
├── 🔤 POLICES PARTAGÉES
│   └── fonts/
│       ├── capital.ttf              # OpenDyslexic Bold (70 Ko)
│       ├── script.ttf               # OpenDyslexic Regular (71 Ko)
│       ├── cursive.ttf              # Écolier cursive (46 Ko)
│       └── README.md
│
├── 📝 DOCUMENTATION
│   ├── README.md                    # Ce fichier
│   ├── CLAUDE.md                    # Instructions projet
│   ├── COMPARAISON.md               # Python vs Web
│   ├── THEMES.md                    # Guide des thèmes
│   ├── ACCESSIBILITE.md             # Accessibilité
│   └── README_PROJET_COMPLET.md     # Documentation complète
│
└── 🧪 TESTS
    ├── test_web.py                  # Tests Playwright
    └── venv/                        # Environnement virtuel
```

## 📚 Documentation

### Fichiers de documentation

| Fichier | Description |
|---------|-------------|
| [README.md](README.md) | Documentation principale |
| [CLAUDE.md](CLAUDE.md) | Instructions et règles du projet |
| [COMPARAISON.md](COMPARAISON.md) | Comparaison Python vs Web |
| [THEMES.md](THEMES.md) | Guide des thèmes et exemples |
| [ACCESSIBILITE.md](ACCESSIBILITE.md) | Fonctionnalités d'accessibilité |
| [web/README.md](web/README.md) | Documentation version web |

### Guides d'utilisation

**Pour les enseignants :**
1. Démarrer avec la version Web (plus simple)
2. Créer quelques fiches de test
3. Si besoin de production en masse, passer à Python

**Pour les développeurs :**
1. Version Python pour scripts et automatisation
2. Version Web pour prototype et démonstration
3. Tests Playwright pour validation

**Pour les contributeurs :**
1. Lire [CLAUDE.md](CLAUDE.md) pour les règles du projet
2. Consulter [COMPARAISON.md](COMPARAISON.md) pour l'architecture
3. Tests obligatoires avant chaque contribution

## 🎨 Fonctionnalités

### Polices et typographie

- **CAPITALES** : OpenDyslexic Bold (32pt) - Dyslexie
- **script** : OpenDyslexic Regular (28pt) - Dyslexie
- **cursif** : Écolier (32pt) - Cursive scolaire française

### Accessibilité

- ✅ Contrastes WCAG AAA (noir pur sur blanc)
- ✅ Bordures noires (2pt) autour des images
- ✅ Espacement généreux (1.5cm entre éléments)
- ✅ Polices spécialisées dyslexie
- ✅ Tailles de police optimales (28-32pt)
- ✅ Mise en page claire (2 mots/page A4)

### Recherche d'images

**Version Python :**
1. PublicDomainVectors (domaine public, SVG)
2. OpenClipart (CC0, dessins vectoriels)
3. Google Images (via scraping, priorité Freepik)

**Version Web :**
1. Pixabay API (gratuit, illustrations)
2. Fallback sur placeholders

### Thèmes supportés

- Automne (feuille, champignon, citrouille, marron)
- Animaux (chat, chien, oiseau, poisson)
- Noël (sapin, cadeau, étoile, neige)
- Personnalisé (créez vos propres fichiers)

## 🔧 Configuration

### Ajouter des traductions

Dans `generate_fiches.py` (Python) ou `js/config.js` (Web) :

```javascript
wordTranslations: {
    'nouveaumot': 'translation',
    // ...
}
```

### Modifier le nombre d'images (Web uniquement)

Dans `js/config.js` :

```javascript
imagesPerWord: 3  // Nombre d'images proposées
```

### Personnaliser les polices

Remplacez les fichiers TTF dans `fonts/` par vos propres polices.

## 🐛 Résolution de problèmes

### Python: "Module not found"
```bash
source venv/bin/activate
pip install -r requirements.txt
```

### Python: "Aucune image trouvée"
- Vérifiez votre connexion internet
- Les sites de recherche peuvent parfois bloquer les requêtes

### Web: Les images ne se chargent pas
- Vérifiez votre connexion internet
- Pixabay API a une limite de 100 requêtes/heure
- L'app utilise des placeholders en fallback

### Web: Le PDF ne se génère pas
- Vérifiez que toutes les images sont sélectionnées
- Ouvrez la console navigateur (F12) pour voir les erreurs
- Réduisez le nombre de mots (max 20-30 recommandé)

### Tests Playwright: "Browser not found"
```bash
playwright install chromium
```

## 📊 Statistiques du projet

- **Lignes de code Python** : ~570
- **Lignes de code JavaScript** : ~500
- **Lignes de CSS** : ~350
- **Taille totale** : ~500 Ko (hors venv)
- **Polices** : 3 fichiers TTF (192 Ko)
- **Documentation** : 6 fichiers Markdown

## 🤝 Contribution

Les contributions sont bienvenues !

1. Fork le projet
2. Créer une branche (`git checkout -b feature/amelioration`)
3. Commit vos changements (`git commit -m 'Ajout fonctionnalité'`)
4. Push vers la branche (`git push origin feature/amelioration`)
5. Ouvrir une Pull Request

**Règles importantes** :
- Lire [CLAUDE.md](CLAUDE.md) avant de contribuer
- Ne jamais simplifier sans demander
- Tests obligatoires
- Documentation mise à jour

## 📄 Licence

Polices :
- OpenDyslexic : Open Font License (OFL)
- Écolier : Licence libre

Code :
- Projet éducatif open source

## 👏 Remerciements

- OpenDyslexic pour les polices dyslexiques
- Écolier pour la cursive scolaire française
- Freepik, OpenClipart, PublicDomainVectors pour les images
- Pixabay pour l'API gratuite

## 📞 Support

Pour des questions ou problèmes :
1. Consulter la documentation dans les fichiers MD
2. Vérifier les issues GitHub
3. Ouvrir une nouvelle issue si nécessaire

---

**Projet créé pour faciliter l'apprentissage en maternelle avec des outils accessibles et adaptés !** 🎓✨
