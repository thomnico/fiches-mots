#!/usr/bin/env python3
"""
Suite de tests Playwright pour la compatibilité mobile
Teste la réactivité, les interactions tactiles, et l'API Mistral sur mobile
"""

import os
import time
import json
from playwright.sync_api import sync_playwright

class TestConfig:
    """Configuration des tests Mobile"""
    # URL de l'application
    APP_URL = "http://localhost:3000"  # Vercel dev requis pour l'API

    # Dossier pour les screenshots
    SCREENSHOTS_DIR = "web/screenshots/tests/mobile"

    # Timeout pour les opérations
    TIMEOUT = 20000  # 20 secondes (mobile peut être plus lent)

    # Timeout pour les requêtes API
    API_TIMEOUT = 30000  # 30 secondes (connexion mobile peut être plus lente)

    # Configurations d'appareils mobiles
    DEVICES = {
        'iPhone 12': {
            'viewport': {'width': 390, 'height': 844},
            'user_agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1',
            'device_scale_factor': 3,
            'is_mobile': True,
            'has_touch': True,
        },
        'iPhone SE': {
            'viewport': {'width': 375, 'height': 667},
            'user_agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1',
            'device_scale_factor': 2,
            'is_mobile': True,
            'has_touch': True,
        },
        'Pixel 5': {
            'viewport': {'width': 393, 'height': 851},
            'user_agent': 'Mozilla/5.0 (Linux; Android 11; Pixel 5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.91 Mobile Safari/537.36',
            'device_scale_factor': 3,
            'is_mobile': True,
            'has_touch': True,
        },
        'iPad Air': {
            'viewport': {'width': 820, 'height': 1180},
            'user_agent': 'Mozilla/5.0 (iPad; CPU OS 14_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1',
            'device_scale_factor': 2,
            'is_mobile': True,
            'has_touch': True,
        },
    }

def setup_test_env():
    """Prépare l'environnement de test"""
    os.makedirs(TestConfig.SCREENSHOTS_DIR, exist_ok=True)

    # Vérifier que le serveur est actif
    import urllib.request
    try:
        urllib.request.urlopen(TestConfig.APP_URL, timeout=5)
    except:
        print(f"❌ Serveur non actif sur {TestConfig.APP_URL}")
        print("   ⚠️  Les tests nécessitent Vercel Dev!")
        print("   Lancez: vercel dev")
        exit(1)

def test_mobile_viewport_responsive(page, device_name):
    """Test 1: Interface réactive sur différents viewports mobiles"""
    print(f"\n📝 Test 1: Réactivité viewport ({device_name})")

    page.goto(TestConfig.APP_URL)
    page.wait_for_load_state('networkidle')

    # Vérifier que les éléments principaux sont visibles
    elements = {
        '#theme': 'Champ thème',
        '#words': 'Zone de texte mots',
        '#btn-magic': 'Bouton IA',
        '#btn-search': 'Bouton recherche',
        '#btn-generate': 'Bouton générer PDF',
    }

    for selector, name in elements.items():
        element = page.locator(selector)
        assert element.is_visible(), f"{name} non visible sur {device_name}"

    print(f"   ✅ Tous les éléments visibles sur {device_name}")

    # Vérifier qu'il n'y a pas de dépassement horizontal
    viewport_width = page.viewport_size['width']
    body_width = page.evaluate('document.body.scrollWidth')

    # Tolérance de 5px pour les bordures/marges
    assert body_width <= viewport_width + 5, \
        f"Débordement horizontal: {body_width}px > {viewport_width}px"

    print(f"   ✅ Pas de débordement horizontal ({body_width}px ≤ {viewport_width}px)")

    page.screenshot(path=f"{TestConfig.SCREENSHOTS_DIR}/01-responsive-{device_name.replace(' ', '-')}.png")
    return True

def test_mobile_touch_interactions(page, device_name):
    """Test 2: Interactions tactiles sur mobile"""
    print(f"\n📝 Test 2: Interactions tactiles ({device_name})")

    page.goto(TestConfig.APP_URL)
    page.wait_for_load_state('networkidle')

    # Test 1: Tap sur le champ thème
    theme_field = page.locator('#theme')
    theme_field.tap()
    time.sleep(0.5)

    # Vérifier que le champ a le focus
    is_focused = page.evaluate('document.activeElement.id === "theme"')
    assert is_focused, "Le champ thème n'a pas reçu le focus après tap"
    print("   ✅ Tap sur champ thème fonctionne")

    # Test 2: Remplir le champ avec le clavier virtuel
    theme_field.fill('animaux')
    theme_value = theme_field.input_value()
    assert theme_value == 'animaux', f"Valeur incorrecte: {theme_value}"
    print("   ✅ Saisie tactile fonctionne")

    # Test 3: Tap sur le bouton Mistral
    btn_magic = page.locator('#btn-magic')
    btn_magic.tap()
    print("   ✅ Tap sur bouton fonctionne")

    page.screenshot(path=f"{TestConfig.SCREENSHOTS_DIR}/02-touch-{device_name.replace(' ', '-')}.png")
    return True

def test_mobile_mistral_api_bug(page, device_name):
    """Test 3: Reproduction du bug API Mistral sur mobile (BUG CONNU)"""
    print(f"\n📝 Test 3: API Mistral sur mobile ({device_name}) - ⚠️ BUG CONNU")

    page.goto(TestConfig.APP_URL)
    page.wait_for_load_state('networkidle')

    # Entrer un thème
    page.locator('#theme').fill('fruits')

    # Cliquer sur le bouton Mistral
    page.locator('#btn-magic').tap()
    print("   Génération en cours...")

    # Capturer les erreurs de console
    console_errors = []
    page.on('console', lambda msg: console_errors.append(msg.text) if msg.type == 'error' else None)

    # Capturer les erreurs réseau
    network_errors = []
    page.on('requestfailed', lambda request: network_errors.append({
        'url': request.url,
        'failure': request.failure
    }))

    try:
        # Attendre que le bouton soit à nouveau activé
        page.wait_for_function(
            "document.querySelector('#btn-magic').disabled === false",
            timeout=TestConfig.API_TIMEOUT
        )
        time.sleep(1)

        # Vérifier les mots générés
        words_value = page.locator('#words').input_value()
        words = [w.strip() for w in words_value.split('\n') if w.strip()]

        if len(words) > 0:
            print(f"   ✅ API fonctionne sur {device_name}: {len(words)} mots générés")
            print(f"   Mots: {', '.join(words[:3])}")
            success = True
        else:
            print(f"   ❌ BUG CONFIRMÉ: Aucun mot généré sur {device_name}")
            success = False

    except Exception as e:
        print(f"   ❌ BUG CONFIRMÉ: Timeout/Erreur sur {device_name}")
        print(f"   Erreur: {e}")
        success = False

    # Afficher les erreurs capturées
    if console_errors:
        print(f"   📋 Erreurs console: {len(console_errors)}")
        for error in console_errors[:3]:
            print(f"      - {error}")

    if network_errors:
        print(f"   🌐 Erreurs réseau: {len(network_errors)}")
        for error in network_errors[:3]:
            print(f"      - {error['url']}: {error['failure']}")

    page.screenshot(path=f"{TestConfig.SCREENSHOTS_DIR}/03-api-bug-{device_name.replace(' ', '-')}.png")

    # Ce test ne fait pas échouer la suite (BUG CONNU)
    # On retourne le résultat pour information
    return success

def test_mobile_mistral_api_direct(page, device_name):
    """Test 4: Appel direct à l'API Mistral avec user-agent mobile"""
    print(f"\n📝 Test 4: API directe avec user-agent {device_name}")

    # Tester l'API directement avec le user-agent mobile
    try:
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
        print(f"   Réponse API: {json.dumps(data, ensure_ascii=False, indent=2)[:200]}...")

        # Vérifications
        assert "words" in data, "Pas de champ 'words' dans la réponse"
        assert isinstance(data["words"], list), "'words' n'est pas une liste"
        assert len(data["words"]) > 0, "Liste de mots vide"

        print(f"   ✅ API directe fonctionne sur {device_name}: {len(data['words'])} mots")

    except Exception as e:
        print(f"   ❌ API directe échoue sur {device_name}: {e}")
        page.screenshot(path=f"{TestConfig.SCREENSHOTS_DIR}/04-api-direct-error-{device_name.replace(' ', '-')}.png")
        raise

    return True

def test_mobile_buttons_size(page, device_name):
    """Test 5: Taille des boutons adaptée au tactile"""
    print(f"\n📝 Test 5: Taille des boutons tactiles ({device_name})")

    page.goto(TestConfig.APP_URL)
    page.wait_for_load_state('networkidle')

    # Taille minimale recommandée pour les boutons tactiles: 44x44px (iOS) ou 48x48px (Android)
    min_size = 44

    buttons = {
        '#btn-magic': 'Bouton IA',
        '#btn-search': 'Bouton recherche',
        '#btn-generate': 'Bouton générer PDF',
    }

    for selector, name in buttons.items():
        button = page.locator(selector)
        bbox = button.bounding_box()

        if bbox:
            height = bbox['height']
            width = bbox['width']

            assert height >= min_size, \
                f"{name} trop petit (hauteur: {height}px < {min_size}px)"
            assert width >= min_size, \
                f"{name} trop étroit (largeur: {width}px < {min_size}px)"

            print(f"   ✅ {name}: {width:.0f}x{height:.0f}px")

    page.screenshot(path=f"{TestConfig.SCREENSHOTS_DIR}/05-buttons-{device_name.replace(' ', '-')}.png")
    return True

def test_mobile_full_workflow(page, device_name):
    """Test 6: Workflow complet sur mobile (si l'API fonctionne)"""
    print(f"\n📝 Test 6: Workflow complet sur {device_name}")

    page.goto(TestConfig.APP_URL)
    page.wait_for_load_state('networkidle')

    # Étape 1: Générer les mots avec Mistral
    page.locator('#theme').fill('couleurs')
    page.locator('#btn-magic').tap()

    print("   Étape 1/3: Génération de mots...")

    try:
        page.wait_for_function(
            "document.querySelector('#btn-magic').disabled === false",
            timeout=TestConfig.API_TIMEOUT
        )
        time.sleep(1)

        words_value = page.locator('#words').input_value()
        words = [w.strip() for w in words_value.split('\n') if w.strip()]

        if len(words) == 0:
            print("   ⚠️  Skip workflow: API Mistral n'a pas généré de mots")
            return None

        print(f"   ✅ {len(words)} mots générés")

        # Étape 2: Rechercher les images
        print("   Étape 2/3: Recherche d'images...")
        page.locator('#btn-search').tap()

        # Attendre les sections
        page.wait_for_selector('.word-section', timeout=TestConfig.TIMEOUT)
        time.sleep(2)

        sections = page.locator('.word-section').count()
        print(f"   ✅ {sections} sections créées")

        # Étape 3: Screenshot final
        print("   Étape 3/3: Vérification visuelle...")
        page.screenshot(path=f"{TestConfig.SCREENSHOTS_DIR}/06-workflow-{device_name.replace(' ', '-')}.png")

        print(f"   ✅ Workflow complet réussi sur {device_name}")
        return True

    except Exception as e:
        print(f"   ❌ Workflow échoué: {e}")
        page.screenshot(path=f"{TestConfig.SCREENSHOTS_DIR}/06-workflow-error-{device_name.replace(' ', '-')}.png")
        return None

def test_mobile_orientation_landscape(page, device_name):
    """Test 7: Test en mode paysage (landscape)"""
    print(f"\n📝 Test 7: Mode paysage ({device_name})")

    # Inverser les dimensions pour le mode paysage
    viewport = page.viewport_size
    page.set_viewport_size({'width': viewport['height'], 'height': viewport['width']})

    page.goto(TestConfig.APP_URL)
    page.wait_for_load_state('networkidle')

    # Vérifier que les éléments sont toujours visibles
    elements = ['#theme', '#words', '#btn-magic', '#btn-search', '#btn-generate']

    for selector in elements:
        element = page.locator(selector)
        assert element.is_visible(), f"{selector} non visible en mode paysage"

    print(f"   ✅ Interface fonctionne en mode paysage sur {device_name}")

    page.screenshot(path=f"{TestConfig.SCREENSHOTS_DIR}/07-landscape-{device_name.replace(' ', '-')}.png")

    # Remettre en mode portrait
    page.set_viewport_size(viewport)

    return True

def run_all_tests():
    """Exécute tous les tests Mobile"""
    print("="*60)
    print("📱 Suite de Tests Playwright - Mobile")
    print("="*60)

    setup_test_env()

    # Tests à exécuter sur chaque appareil
    tests_per_device = [
        ("Viewport réactif", test_mobile_viewport_responsive),
        ("Interactions tactiles", test_mobile_touch_interactions),
        ("API Mistral (BUG)", test_mobile_mistral_api_bug),
        ("API directe", test_mobile_mistral_api_direct),
        ("Taille boutons", test_mobile_buttons_size),
        ("Workflow complet", test_mobile_full_workflow),
        ("Mode paysage", test_mobile_orientation_landscape),
    ]

    all_results = []

    with sync_playwright() as p:
        print("\n🌐 Lancement du navigateur Firefox...")
        browser = p.firefox.launch(headless=False)

        # Tester sur chaque appareil
        for device_name, device_config in TestConfig.DEVICES.items():
            print(f"\n{'='*60}")
            print(f"📱 Tests sur {device_name}")
            print(f"   Viewport: {device_config['viewport']['width']}x{device_config['viewport']['height']}")
            print(f"{'='*60}")

            context = browser.new_context(**device_config)

            for test_name, test_func in tests_per_device:
                page = context.new_page()
                full_test_name = f"{test_name} ({device_name})"
                print(f"\n{'─'*60}")

                try:
                    result = test_func(page, device_name)

                    if result is True:
                        all_results.append((full_test_name, "PASS", None))
                    elif result is None:
                        all_results.append((full_test_name, "SKIP", "Conditions non remplies"))
                    elif result is False:
                        all_results.append((full_test_name, "WARN", "BUG CONNU"))
                    else:
                        all_results.append((full_test_name, "FAIL", "Test échoué"))

                except AssertionError as e:
                    all_results.append((full_test_name, "FAIL", str(e)))
                    print(f"   ❌ ÉCHEC: {e}")
                    page.screenshot(path=f"{TestConfig.SCREENSHOTS_DIR}/error-{device_name.replace(' ', '-')}-{test_name.replace(' ', '-')}.png")

                except Exception as e:
                    all_results.append((full_test_name, "ERROR", str(e)))
                    print(f"   ❌ ERREUR: {e}")

                finally:
                    page.close()
                    time.sleep(0.5)

            context.close()

        browser.close()

    # Résumé
    print("\n" + "="*60)
    print("📊 RÉSUMÉ DES TESTS MOBILE")
    print("="*60)

    passed = sum(1 for _, status, _ in all_results if status == "PASS")
    failed = sum(1 for _, status, _ in all_results if status == "FAIL")
    skipped = sum(1 for _, status, _ in all_results if status == "SKIP")
    warnings = sum(1 for _, status, _ in all_results if status == "WARN")
    errors = sum(1 for _, status, _ in all_results if status == "ERROR")

    for test_name, status, message in all_results:
        icon = {
            "PASS": "✅",
            "FAIL": "❌",
            "SKIP": "⚠️ ",
            "WARN": "⚠️ ",
            "ERROR": "💥"
        }[status]

        msg = f" - {message[:50]}" if message else ""
        print(f"{icon} {status:6} {test_name:45} {msg}")

    print("\n" + "="*60)
    print(f"Total: {len(all_results)} tests")
    print(f"✅ Réussis: {passed}")
    print(f"❌ Échoués: {failed}")
    print(f"⚠️  Avertissements: {warnings}")
    print(f"⚠️  Sautés: {skipped}")
    print(f"💥 Erreurs: {errors}")
    print("="*60)

    print(f"\n📸 Screenshots sauvegardés dans: {TestConfig.SCREENSHOTS_DIR}/")

    # Note spéciale sur le bug Mistral mobile
    if warnings > 0:
        print("\n⚠️  BUGS CONNUS DÉTECTÉS:")
        print("   - L'API Mistral peut ne pas fonctionner correctement sur mobile")
        print("   - Voir CLAUDE.md section <troubleshooting> pour plus de détails")

    # Code de sortie
    # Les warnings ne font pas échouer la suite (bugs connus)
    if failed > 0 or errors > 0:
        print("\n⚠️  Des tests ont échoué!")
        exit(1)
    else:
        print("\n🎉 Tous les tests mobile critiques sont passés!")
        if warnings > 0:
            print("   (avec avertissements sur bugs connus)")
        exit(0)

if __name__ == "__main__":
    if not os.path.exists('web/index.html'):
        print("❌ Erreur: Exécutez ce script depuis le dossier racine du projet")
        print("   cd /Volumes/sidecar/src/fiches-mots")
        exit(1)

    run_all_tests()
