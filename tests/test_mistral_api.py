#!/usr/bin/env python3
"""
Suite de tests Playwright pour l'API Mistral AI
Teste la génération automatique de mots thématiques
"""

import os
import time
import json
from playwright.sync_api import sync_playwright

class TestConfig:
    """Configuration des tests Mistral"""
    # URL de l'application
    APP_URL = "http://localhost:3000"  # Vercel dev requis pour l'API

    # Dossier pour les screenshots
    SCREENSHOTS_DIR = "web/screenshots/tests/mistral"

    # Timeout pour les opérations
    TIMEOUT = 15000  # 15 secondes (API peut être lente)

    # Timeout pour les requêtes API
    API_TIMEOUT = 20000  # 20 secondes

def setup_test_env():
    """Prépare l'environnement de test"""
    os.makedirs(TestConfig.SCREENSHOTS_DIR, exist_ok=True)

    # Vérifier que le serveur est actif
    import urllib.request
    try:
        urllib.request.urlopen(TestConfig.APP_URL, timeout=5)
    except:
        print(f"❌ Serveur non actif sur {TestConfig.APP_URL}")
        print("   ⚠️  L'API Mistral nécessite Vercel Dev!")
        print("   Lancez: vercel dev")
        exit(1)

def test_mistral_api_direct(page):
    """Test 1: Appel direct à l'API Mistral"""
    print("\n📝 Test 1: Appel direct API /api/mistral")

    # Tester l'API directement
    response = page.request.post(
        f"{TestConfig.APP_URL}/api/mistral",
        data={
            "theme": "animaux",
            "count": 5
        },
        timeout=TestConfig.API_TIMEOUT
    )

    assert response.ok, f"API retourné {response.status}"

    data = response.json()
    print(f"   Réponse API: {json.dumps(data, ensure_ascii=False, indent=2)}")

    # Vérifications
    assert "words" in data, "Pas de champ 'words' dans la réponse"
    assert isinstance(data["words"], list), "'words' n'est pas une liste"
    assert len(data["words"]) > 0, "Liste de mots vide"
    assert data["theme"] == "animaux", f"Thème incorrect: {data['theme']}"
    assert data["model"] == "ministral-3b-latest", f"Modèle incorrect: {data['model']}"

    print(f"   ✅ API fonctionne: {len(data['words'])} mots générés")
    print(f"   Mots: {', '.join(data['words'][:5])}")

    return True

def test_mistral_ui_button_visibility(page):
    """Test 2: Visibilité du bouton Mistral AI dans l'interface"""
    print("\n📝 Test 2: Bouton 'Générer avec IA' visible")

    page.goto(TestConfig.APP_URL)
    page.wait_for_load_state('networkidle')

    # Vérifier que le bouton Mistral existe
    mistral_button = page.locator('#btn-magic')
    assert mistral_button.is_visible(), "Bouton Mistral AI non visible"

    button_text = mistral_button.inner_text()
    assert "Magique" in button_text or "Chat" in button_text, f"Texte bouton incorrect: {button_text}"

    print(f"   ✅ Bouton visible: '{button_text}'")

    page.screenshot(path=f"{TestConfig.SCREENSHOTS_DIR}/01-button-visibility.png")
    return True

def test_mistral_word_generation_simple(page):
    """Test 3: Génération de mots simple via l'UI"""
    print("\n📝 Test 3: Génération de mots via UI (thème: automne)")

    page.goto(TestConfig.APP_URL)
    page.wait_for_load_state('networkidle')

    # Entrer un thème
    page.locator('#theme').fill('automne')

    # Cliquer sur le bouton Mistral
    page.locator('#btn-magic').click()
    print("   Génération en cours...")

    # Attendre que le bouton soit à nouveau activé (signe que l'API a répondu)
    page.wait_for_function("document.querySelector('#btn-magic').disabled === false", timeout=TestConfig.API_TIMEOUT)
    time.sleep(1)

    # Récupérer les mots générés
    words_value = page.locator('#words').input_value()
    words = [w.strip() for w in words_value.split('\n') if w.strip()]

    assert len(words) > 0, "Aucun mot généré"
    print(f"   ✅ {len(words)} mots générés: {', '.join(words[:5])}")

    # Vérifier que les mots sont pertinents pour le thème
    # (test basique: au moins 3 mots)
    assert len(words) >= 3, f"Trop peu de mots générés: {len(words)}"

    page.screenshot(path=f"{TestConfig.SCREENSHOTS_DIR}/02-generation-simple.png")
    return True

def test_mistral_word_count_custom(page):
    """Test 4: Génération avec nombre de mots personnalisé"""
    print("\n📝 Test 4: Génération avec 15 mots")

    page.goto(TestConfig.APP_URL)
    page.wait_for_load_state('networkidle')

    # Vérifier si le champ count existe
    count_field = page.locator('#word-count')
    if not count_field.is_visible():
        print("   ⚠️  Champ 'word-count' non trouvé (skip)")
        return None

    # Configurer
    page.locator('#theme').fill('couleurs')
    count_field.fill('15')

    # Générer
    page.locator('#btn-magic').click()
    page.wait_for_function("document.querySelector('#btn-magic').disabled === false", timeout=TestConfig.API_TIMEOUT)
    time.sleep(1)

    # Vérifier
    words_value = page.locator('#words').input_value()
    words = [w.strip() for w in words_value.split('\n') if w.strip()]

    # Tolérance: entre 10 et 20 mots (l'IA peut varier légèrement)
    assert 10 <= len(words) <= 20, f"Nombre de mots hors range: {len(words)}"
    print(f"   ✅ {len(words)} mots générés (attendu ~15)")

    page.screenshot(path=f"{TestConfig.SCREENSHOTS_DIR}/03-custom-count.png")
    return True

def test_mistral_then_search_images(page):
    """Test 5: Génération de mots + recherche d'images (workflow complet)"""
    print("\n📝 Test 5: Workflow complet (Mistral → Recherche images)")

    page.goto(TestConfig.APP_URL)
    page.wait_for_load_state('networkidle')

    # Étape 1: Générer les mots avec Mistral
    page.locator('#theme').fill('fruits')
    page.locator('#btn-magic').click()

    print("   Étape 1/2: Génération de mots...")
    page.wait_for_function("document.querySelector('#btn-magic').disabled === false", timeout=TestConfig.API_TIMEOUT)
    time.sleep(1)

    words_value = page.locator('#words').input_value()
    words = [w.strip() for w in words_value.split('\n') if w.strip()]
    print(f"   ✅ {len(words)} mots générés")

    # Étape 2: Rechercher les images
    print("   Étape 2/2: Recherche d'images...")
    page.locator('#btn-search').click()

    # Attendre que toutes les sections soient créées
    # Les sections sont créées progressivement, donc on attend plus longtemps
    page.wait_for_selector('.word-section', timeout=TestConfig.TIMEOUT)

    # Attendre que le nombre de sections corresponde au nombre de mots
    # Avec un timeout généreux car la recherche d'images peut être lente
    page.wait_for_function(
        f"document.querySelectorAll('.word-section').length === {len(words)}",
        timeout=30000  # 30 secondes pour toutes les images
    )

    sections = page.locator('.word-section').count()
    print(f"   ✅ {sections} sections créées avec images")

    page.screenshot(path=f"{TestConfig.SCREENSHOTS_DIR}/04-full-workflow.png")
    return True

def test_mistral_error_no_theme(page):
    """Test 6: Gestion d'erreur - pas de thème"""
    print("\n📝 Test 6: Erreur si thème vide")

    page.goto(TestConfig.APP_URL)
    page.wait_for_load_state('networkidle')

    # Vider le champ thème
    page.locator('#theme').fill('')

    # Essayer de générer
    page.locator('#btn-magic').click()

    # Attendre une alerte ou un message d'erreur
    time.sleep(2)

    # Le textarea ne devrait PAS être rempli
    words_value = page.locator('#words').input_value()

    # Soit vide, soit contient un message d'erreur, mais pas une liste de mots
    if words_value:
        assert "erreur" in words_value.lower() or len(words_value) < 50, \
            "Le champ contient des mots alors que le thème est vide"

    print("   ✅ Erreur gérée correctement")

    page.screenshot(path=f"{TestConfig.SCREENSHOTS_DIR}/05-error-no-theme.png")
    return True

def test_mistral_multiple_themes(page):
    """Test 7: Générer plusieurs thèmes successivement"""
    print("\n📝 Test 7: Générations multiples (3 thèmes)")

    page.goto(TestConfig.APP_URL)
    page.wait_for_load_state('networkidle')

    themes = ['animaux', 'véhicules', 'météo']

    for i, theme in enumerate(themes, 1):
        print(f"   Thème {i}/3: {theme}")

        page.locator('#theme').fill(theme)
        page.locator('#btn-magic').click()

        page.wait_for_function("document.querySelector('#btn-magic').disabled === false", timeout=TestConfig.API_TIMEOUT)
        time.sleep(1)

        words_value = page.locator('#words').input_value()
        words = [w.strip() for w in words_value.split('\n') if w.strip()]

        assert len(words) >= 3, f"Trop peu de mots pour {theme}: {len(words)}"
        print(f"      ✅ {len(words)} mots: {', '.join(words[:3])}...")

        time.sleep(1)  # Pause entre les requêtes

    page.screenshot(path=f"{TestConfig.SCREENSHOTS_DIR}/06-multiple-themes.png")
    return True

def test_mistral_api_model_verification(page):
    """Test 8: Vérifier que le bon modèle est utilisé"""
    print("\n📝 Test 8: Vérification du modèle (ministral-3b-latest)")

    response = page.request.post(
        f"{TestConfig.APP_URL}/api/mistral",
        data={
            "theme": "test",
            "count": 3
        },
        timeout=TestConfig.API_TIMEOUT
    )

    assert response.ok, f"API retourné {response.status}"
    data = response.json()

    # Vérifier le modèle
    assert "model" in data, "Pas de champ 'model' dans la réponse"
    assert data["model"] == "ministral-3b-latest", \
        f"Modèle incorrect: {data['model']} (attendu: ministral-3b-latest)"

    print(f"   ✅ Modèle correct: {data['model']}")
    print(f"   💰 Modèle économique confirmé (0.04€/1M tokens - 6x moins cher!)")

    return True

def run_all_tests():
    """Exécute tous les tests Mistral"""
    print("="*60)
    print("🪄 Suite de Tests Playwright - Mistral AI")
    print("="*60)

    setup_test_env()

    tests = [
        ("API directe", test_mistral_api_direct),
        ("Bouton UI visible", test_mistral_ui_button_visibility),
        ("Génération simple", test_mistral_word_generation_simple),
        ("Nombre de mots custom", test_mistral_word_count_custom),
        ("Workflow complet", test_mistral_then_search_images),
        ("Erreur thème vide", test_mistral_error_no_theme),
        ("Thèmes multiples", test_mistral_multiple_themes),
        ("Vérification modèle", test_mistral_api_model_verification),
    ]

    results = []

    with sync_playwright() as p:
        print("\n🌐 Lancement du navigateur...")
        browser = p.chromium.launch(headless=False)
        context = browser.new_context(viewport={'width': 1280, 'height': 800})

        for test_name, test_func in tests:
            page = context.new_page()
            print(f"\n{'─'*60}")

            try:
                result = test_func(page)
                if result is True:
                    results.append((test_name, "PASS", None))
                elif result is None:
                    results.append((test_name, "SKIP", "Conditions non remplies"))
                else:
                    results.append((test_name, "FAIL", "Test échoué"))

            except AssertionError as e:
                results.append((test_name, "FAIL", str(e)))
                print(f"   ❌ ÉCHEC: {e}")
                page.screenshot(path=f"{TestConfig.SCREENSHOTS_DIR}/error-{test_name.replace(' ', '-')}.png")

            except Exception as e:
                results.append((test_name, "ERROR", str(e)))
                print(f"   ❌ ERREUR: {e}")

            finally:
                page.close()
                time.sleep(1)

        browser.close()

    # Résumé
    print("\n" + "="*60)
    print("📊 RÉSUMÉ DES TESTS MISTRAL")
    print("="*60)

    passed = sum(1 for _, status, _ in results if status == "PASS")
    failed = sum(1 for _, status, _ in results if status == "FAIL")
    skipped = sum(1 for _, status, _ in results if status == "SKIP")
    errors = sum(1 for _, status, _ in results if status == "ERROR")

    for test_name, status, message in results:
        icon = {
            "PASS": "✅",
            "FAIL": "❌",
            "SKIP": "⚠️ ",
            "ERROR": "💥"
        }[status]

        msg = f" - {message}" if message else ""
        print(f"{icon} {status:6} {test_name:30} {msg}")

    print("\n" + "="*60)
    print(f"Total: {len(results)} tests")
    print(f"✅ Réussis: {passed}")
    print(f"❌ Échoués: {failed}")
    print(f"⚠️  Sautés: {skipped}")
    print(f"💥 Erreurs: {errors}")
    print("="*60)

    print(f"\n📸 Screenshots sauvegardés dans: {TestConfig.SCREENSHOTS_DIR}/")

    # Code de sortie
    if failed > 0 or errors > 0:
        print("\n⚠️  Des tests ont échoué!")
        exit(1)
    else:
        print("\n🎉 Tous les tests Mistral sont passés!")
        exit(0)

if __name__ == "__main__":
    if not os.path.exists('web/index.html'):
        print("❌ Erreur: Exécutez ce script depuis le dossier racine du projet")
        print("   cd /Volumes/sidecar/src/fiches-mots")
        exit(1)

    run_all_tests()
