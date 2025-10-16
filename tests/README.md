# Tests Playwright - Fiches-Mots

Suite de tests de non-régression pour l'application Fiches Pédagogiques.

## Installation

```bash
# Installer Playwright
pip install playwright

# Installer les navigateurs
python -m playwright install chromium
```

## Exécution des Tests

### En local avec serveur simple

```bash
# Terminal 1: Démarrer le serveur
cd web
python3 -m http.server 8000

# Terminal 2: Lancer les tests
cd /Volumes/sidecar/src/fiches-mots
python tests/test_web_app.py
```

⚠️ Avec le serveur simple, les API ne fonctionnent pas. Les tests d'images seront sautés.

### En local avec Vercel Dev (recommandé)

```bash
# Terminal 1: Démarrer Vercel Dev
vercel dev
# Application sur http://localhost:3000

# Terminal 2: Modifier la config et lancer les tests
# Dans tests/test_web_app.py, changer:
# APP_URL = "http://localhost:3000"

python tests/test_web_app.py
```

✅ Avec Vercel Dev, toutes les API fonctionnent.

### En production

```bash
# Modifier la config
# APP_URL = "https://your-app.vercel.app"

python tests/test_web_app.py
```

## Tests Inclus

### 1. test_simple_words
Vérifie que les mots simples (sans caractères spéciaux) fonctionnent correctement.
- **Mots testés**: chat, chien, oiseau
- **Vérifie**: Création de 3 sections

### 2. test_words_with_spaces
Vérifie que les mots avec espaces génèrent des IDs HTML valides.
- **Mots testés**: petite voiture, grosse maison
- **Vérifie**: IDs sans espaces (`word-petite-voiture`)

### 3. test_words_with_apostrophes ⭐️
**TEST DE NON-RÉGRESSION CRITIQUE**

Vérifie que les apostrophes sont correctement encodées.
- **Mots testés**: l'oiseau, d'automne
- **Vérifie**: IDs sans apostrophes brutes (`word-l-oiseau`)
- **Bug corrigé**: Issue #1 - Apostrophes causaient des erreurs CSS

### 4. test_mixed_characters
Vérifie que les combinaisons complexes fonctionnent.
- **Mots testés**: feuille d'érable, château d'eau
- **Vérifie**: Espaces + apostrophes + accents

### 5. test_image_selection
Vérifie que la sélection d'images fonctionne.
- **Vérifie**: Clic sur une image, classe `.selected`
- **Note**: Sauté si API non disponibles

### 6. test_pagination
Vérifie que le bouton "Plus d'images" fonctionne.
- **Vérifie**: Clic sur pagination
- **Note**: Sauté si moins de 3 images

## Screenshots

Tous les tests génèrent des screenshots dans `web/screenshots/tests/`:
- `01-simple-words.png`
- `02-words-with-spaces.png`
- `03-words-with-apostrophes.png` ⭐️
- `04-mixed-characters.png`
- `05-image-selection.png`
- `06-pagination.png`
- `error-*.png` (en cas d'échec)

## Configuration

Éditer `TestConfig` dans `test_web_app.py`:

```python
class TestConfig:
    APP_URL = "http://localhost:8000"  # URL de l'app
    SCREENSHOTS_DIR = "web/screenshots/tests"
    TIMEOUT = 10000  # 10 secondes
```

## CI/CD

### GitHub Actions (exemple)

```yaml
name: Tests Playwright

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v3

      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'

      - name: Install dependencies
        run: |
          pip install playwright
          playwright install chromium

      - name: Start Vercel Dev
        run: |
          npm install -g vercel
          vercel dev --listen 3000 &
          sleep 10

      - name: Run tests
        run: python tests/test_web_app.py

      - name: Upload screenshots
        if: always()
        uses: actions/upload-artifact@v3
        with:
          name: test-screenshots
          path: web/screenshots/tests/
```

## Dépannage

### Erreur: "Serveur non actif"
- Vérifiez que le serveur tourne sur le bon port
- Changez `APP_URL` dans la config

### Tests sautés (SKIP)
- Normal avec serveur simple (pas d'API)
- Utilisez `vercel dev` pour tester les API

### Timeout
- Augmentez `TIMEOUT` dans la config
- Vérifiez votre connexion internet

## Maintenance

### Ajouter un nouveau test

```python
def test_my_feature(page):
    """Test X: Description"""
    print("\n📝 Test X: Ma fonctionnalité")

    page.goto(TestConfig.APP_URL)
    # ... votre test ...

    assert condition, "Message d'erreur"
    print("   ✅ Test réussi")

    page.screenshot(path=f"{TestConfig.SCREENSHOTS_DIR}/0X-my-feature.png")
    return True
```

Puis l'ajouter dans `run_all_tests()`:
```python
tests = [
    # ... tests existants ...
    ("Ma fonctionnalité", test_my_feature),
]
```

## Tests Mistral AI

Une suite dédiée de tests pour l'intégration Mistral AI est disponible dans `test_mistral_api.py`.

### Exécution des tests Mistral

```bash
# Démarrer Vercel Dev (OBLIGATOIRE pour l'API)
vercel dev

# Dans un autre terminal
python tests/test_mistral_api.py
```

⚠️ Les tests Mistral **nécessitent** Vercel Dev (pas de serveur simple).

### Tests Mistral inclus

1. **API directe** - Teste l'endpoint `/api/mistral`
2. **Bouton UI** - Vérifie la visibilité du bouton "Générer avec IA"
3. **Génération simple** - Génère des mots pour un thème
4. **Nombre custom** - Teste la génération avec un nombre spécifique de mots
5. **Workflow complet** - Génération + recherche d'images
6. **Gestion erreurs** - Vérifie le comportement avec thème vide
7. **Thèmes multiples** - Teste plusieurs générations successives
8. **Vérification modèle** - Confirme l'utilisation de `open-mistral-7b`

Screenshots sauvegardés dans `web/screenshots/tests/mistral/`.

## Historique

- **2025-10-16**: Création de la suite de tests
- **2025-10-16**: Ajout test critique apostrophes (régression issue #1)
- **2025-10-16**: Ajout suite de tests Mistral AI (8 tests)
