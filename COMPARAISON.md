# Comparaison des versions Python et Web

Ce projet propose deux versions du générateur de fiches pédagogiques : une version **Python** (ligne de commande) et une version **Web** (interface graphique).

## 📊 Tableau comparatif

| Critère | Version Python | Version Web |
|---------|---------------|-------------|
| **Installation** | Python 3 + pip | Aucune (navigateur) |
| **Interface** | Ligne de commande | Interface graphique |
| **Utilisation** | Technique | Grand public |
| **Sélection images** | Automatique (1ère trouvée) | Interactive (3 choix) |
| **Sources images** | PublicDomainVectors, OpenClipart, Google | Unsplash API |
| **Polices** | ✅ OpenDyslexic + Écolier | ✅ OpenDyslexic + Écolier |
| **Format PDF** | ✅ Identique A4 | ✅ Identique A4 |
| **Accessibilité** | ✅ Contrastes, bordures | ✅ Contrastes, bordures |
| **Thèmes** | ✅ Support complet | ✅ Support complet |
| **Traductions** | FR → EN automatique | FR → EN automatique |
| **Offline** | ✅ (après install) | ❌ (besoin internet) |
| **Batch processing** | ✅ Facile | ⚠️ Limité |
| **Déploiement** | N/A | GitHub Pages, Netlify |

## 🎯 Quand utiliser quelle version ?

### Version Python (`generate_fiches.py`)

**Utiliser si :**
- Vous êtes à l'aise avec la ligne de commande
- Vous devez générer beaucoup de fiches (automatisation)
- Vous voulez un contrôle précis sur la recherche d'images
- Vous préférez travailler hors ligne
- Vous voulez intégrer dans un workflow automatisé

**Exemple d'utilisation :**
```bash
python3 generate_fiches.py mots_automne.txt output/fiches_automne.pdf
```

### Version Web (`web/index.html`)

**Utiliser si :**
- Vous préférez une interface graphique
- Vous voulez choisir visuellement les images
- Vous devez partager l'outil avec des non-techniques (enseignants, parents)
- Vous voulez un résultat immédiat sans installation
- Vous générez quelques fiches occasionnellement

**Exemple d'utilisation :**
1. Ouvrir `web/index.html` dans un navigateur
2. Saisir le thème et les mots
3. Choisir les images
4. Télécharger le PDF

## 🔄 Workflow hybride recommandé

### Pour les enseignants
1. **Découverte** : Utiliser la version Web pour tester
2. **Production** : Basculer sur Python pour générer en masse

### Pour les développeurs
1. **Prototype** : Version Web pour valider les images
2. **Automatisation** : Version Python pour intégration

## 📁 Structure du projet

```
fiches-mots/
├── generate_fiches.py      # Version Python
├── requirements.txt         # Dépendances Python
├── fonts/                   # Polices partagées
│   ├── capital.ttf
│   ├── script.ttf
│   └── cursive.ttf
├── mots_*.txt              # Fichiers de mots (exemples)
├── output/                  # PDFs générés par Python
├── web/                     # Version Web
│   ├── index.html
│   ├── css/style.css
│   ├── js/
│   │   ├── app.js
│   │   ├── config.js
│   │   ├── imageSearch.js
│   │   └── pdfGenerator.js
│   ├── fonts/              # Polices (copie)
│   └── start.sh            # Script de démarrage
└── CLAUDE.md               # Instructions du projet

```

## 🚀 Démarrage rapide

### Python
```bash
# Installation
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Utilisation
python3 generate_fiches.py mots_automne.txt
```

### Web
```bash
# Démarrage serveur local
cd web/
./start.sh

# Ou simplement ouvrir index.html dans un navigateur
```

## 🎨 Fonctionnalités communes

Les deux versions partagent :
- ✅ Mêmes polices (OpenDyslexic + Écolier)
- ✅ Même mise en page (2 mots/page A4)
- ✅ Mêmes tailles de police (32pt capitals, 28pt script, 32pt cursive)
- ✅ Mêmes bordures et espacements
- ✅ Support des thèmes contextuels
- ✅ Traductions FR/EN automatiques
- ✅ Images enfantines (clipart/cartoon/sticker)
- ✅ Accessibilité (dyslexie, contraste WCAG AAA)

## 💡 Évolutions possibles

### Version Python
- [ ] Interface graphique Tkinter
- [ ] Mode serveur web (Flask/FastAPI)
- [ ] API REST pour intégration
- [ ] Export multi-format (DOCX, PNG)

### Version Web
- [ ] Mode hors ligne (PWA avec cache)
- [ ] Drag & drop pour réorganiser les mots
- [ ] Prévisualisation PDF en ligne
- [ ] Historique des fiches générées
- [ ] Partage de configurations

## 📝 Notes techniques

### Recherche d'images

**Python :**
- Scraping HTML (PublicDomainVectors, OpenClipart)
- Recherche Google Images via regex
- Priorité aux stickers Freepik

**Web :**
- API Unsplash (gratuite, sans CORS)
- Fallback sur placeholders
- Conversion Data URL pour PDF

### Génération PDF

**Python :**
- ReportLab (natif)
- Polices TTF via TTFont
- Support SVG via cairosvg

**Web :**
- jsPDF (JavaScript)
- Polices TTF en base64
- Images en Data URL

## 🤝 Contribution

Pour contribuer à l'une ou l'autre version, consultez :
- Python : Code dans `generate_fiches.py`
- Web : Code dans `web/js/`

Les deux versions utilisent les mêmes configurations de traduction et de thèmes (voir `CONFIG` dans chaque fichier).

---

**Choisissez la version qui correspond le mieux à vos besoins !** 🎯
