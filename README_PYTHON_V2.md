# 🐍 Script Python v2 - Pixabay & Unsplash

## 🆕 Nouvelle Version Alignée sur le Web

Le script `generate_fiches_v2.py` est maintenant **100% aligné** avec la version JavaScript :

- ✅ **Mêmes APIs** : Pixabay (vecteurs prioritaires) + Unsplash (fallback)
- ✅ **Mêmes tailles de police** : Capital 32pt, Script 36pt, Cursif 64pt
- ✅ **Même logique de recherche** : Mot seul pour variété, gestion des mots ambigus
- ✅ **Mêmes dimensions d'images** : 7cm × 5cm maximum
- ✅ **Même espacement** : Identique au rendu JavaScript

## 📊 Comparaison des Versions

| Caractéristique | generate_fiches.py (v1) | generate_fiches_v2.py (v2) |
|----------------|-------------------------|----------------------------|
| **Sources d'images** | PublicDomainVectors, OpenClipart, Google Images | Pixabay API + Unsplash API |
| **Type d'images** | SVG convertis, scraping web | Vecteurs PNG + Photos HD |
| **Qualité** | Variable (scraping) | Excellente (APIs officielles) |
| **Fiabilité** | Moyenne (dépend du scraping) | Haute (APIs stables) |
| **Vitesse** | Lente (scraping + conversions) | Rapide (APIs directes) |
| **Police Capital** | 32pt | 32pt ✅ |
| **Police Script** | 28pt | 36pt ✅ (+30%) |
| **Police Cursif** | 32pt | 64pt ✅ (+100%) |
| **Alignement JS** | Non | Oui ✅ |
| **Clés API requises** | Non | Oui (variables d'env) |

## 🚀 Utilisation

### Installation

Les dépendances sont les mêmes que la v1 :

```bash
source venv/bin/activate
pip install -r requirements.txt
```

### Configuration des Clés API

#### Option 1 : Variables d'environnement (recommandé)

```bash
export PIXABAY_API_KEY="votre_clé_pixabay_ici"
export UNSPLASH_ACCESS_KEY="votre_clé_unsplash_ici"
```

Ou ajoutez-les dans votre `.bashrc`/`.zshrc` :

```bash
echo 'export PIXABAY_API_KEY="votre_clé_pixabay_ici"' >> ~/.zshrc
echo 'export UNSPLASH_ACCESS_KEY="votre_clé_unsplash_ici"' >> ~/.zshrc
source ~/.zshrc
```

#### Option 2 : Clés codées en dur (par défaut)

Les clés sont déjà incluses dans le script par défaut. **Pas besoin de configuration !**

### Génération de Fiches

```bash
# Utiliser la v2 (recommandé)
python3 generate_fiches_v2.py mots_automne.txt

# Spécifier le fichier de sortie
python3 generate_fiches_v2.py mots_automne.txt output/mes_fiches.pdf

# Utiliser l'ancienne v1 (si besoin)
python3 generate_fiches.py mots_automne.txt
```

## ✨ Fonctionnalités v2

### 1. Recherche Pixabay Optimisée

```python
# Priorité 1: Vecteurs (mot seul)
→ feuille → 20 vecteurs

# Priorité 2: Vecteurs (mot + thème)
→ feuille automne → 15 vecteurs

# Priorité 3: Illustrations
→ feuille illustrations → 10 images
```

### 2. Fallback Unsplash

Si Pixabay ne trouve pas assez d'images :
```python
→ "feuille livre enfants illustration" sur Unsplash
→ Photos HD orientées paysage
```

### 3. Gestion des Mots Ambigus

Comme dans la version JavaScript :

```python
if word == "marron" and theme == "automne":
    search_word = "châtaigne marron"  # Pas la couleur !
```

### 4. Tailles de Police Augmentées

```python
CAPITAL: 32pt  # Identique
script:  36pt  # +30% vs ancienne version (28pt)
cursif:  64pt  # +100% vs ancienne version (32pt) 🎯
```

## 📈 Avantages de la v2

### Par rapport à la v1 (Python)

✅ **Plus rapide** : APIs directes vs scraping web
✅ **Plus fiable** : Pas de breakage si les sites changent
✅ **Meilleure qualité** : Images vectorielles Pixabay
✅ **Aligné sur JS** : Rendu identique web et Python
✅ **Moins de dépendances** : Pas besoin de cairosvg pour SVG

### Par rapport à la version Web

✅ **Génération en masse** : Traiter plusieurs fichiers
✅ **Automation** : Intégrer dans des scripts
✅ **Offline après téléchargement** : Les images sont dans le PDF
✅ **Pas de navigateur requis**

## 🎓 Exemples d'Utilisation

### Générer toutes les fiches de thèmes

```bash
for file in mots_*.txt; do
    python3 generate_fiches_v2.py "$file"
done
```

### Générer avec un thème spécifique

```bash
python3 generate_fiches_v2.py mots_noel.txt output/fiches_noel_2024.pdf
```

### Utiliser avec des clés API personnalisées

```bash
PIXABAY_API_KEY="votre_cle" \
UNSPLASH_ACCESS_KEY="votre_cle" \
python3 generate_fiches_v2.py mots_animaux.txt
```

## 🔐 Sécurité des Clés API

**Note** : Les clés API incluses dans le script sont destinées à un usage éducatif personnel.

Pour un usage en production :
1. Obtenez vos propres clés sur [Pixabay](https://pixabay.com/api/docs/) et [Unsplash](https://unsplash.com/developers)
2. Configurez-les via variables d'environnement
3. Ne les commitez **jamais** dans git

## 📝 Exemple de Sortie

```bash
$ python3 generate_fiches_v2.py mots_automne.txt

============================================================
Générateur de Fiches Pédagogiques v2 (Pixabay + Unsplash)
============================================================

📖 Chargement: mots_automne.txt
✅ 4 mots: feuille, champignon, citrouille, marron
🔑 Pixabay API: ✅
🔑 Unsplash API: ✅

📄 Génération du PDF: output/fiches_automne.pdf
📝 4 mots à traiter
🎨 Thème: automne

✅ Police CAPITALES chargée: fonts/capital.ttf
✅ Police script chargée: fonts/script.ttf
✅ Police cursive chargée: fonts/cursive.ttf

--- Page 1 ---
🔍 Recherche d'images pour: feuille
   ✅ Pixabay vecteurs: 20 images trouvées
   ✅ 20 images disponibles, téléchargement de la première...
   ✅ Image téléchargée avec succès

[...]

✅ PDF généré avec succès: output/fiches_automne.pdf

============================================================
✅ Génération terminée!
============================================================
```

## 🤝 Migration de v1 à v2

### Changements Nécessaires

**Aucun !** Les deux versions coexistent :

- `generate_fiches.py` → Ancienne version (toujours fonctionnelle)
- `generate_fiches_v2.py` → Nouvelle version (recommandée)

### Recommandation

Utilisez **v2 par défaut** pour :
- ✅ Meilleure qualité d'images
- ✅ Plus de fiabilité
- ✅ Alignement avec la version web

Utilisez **v1** seulement si :
- ❌ Vous ne voulez pas utiliser d'API keys
- ❌ Vous préférez les sources de domaine public strict

## 📚 Documentation Complète

- [README.md](./README.md) - Documentation générale
- [DEVELOPMENT.md](./DEVELOPMENT.md) - Guide développement
- [requirements.txt](./requirements.txt) - Dépendances Python

---

**Profitez de la nouvelle version alignée avec le web !** 🎉
