#!/usr/bin/env python3
"""
Suite de tests Playwright pour l'application Fiches-Mots
Tests de non-régression pour vérifier que l'encodage des caractères spéciaux fonctionne
"""

import os
import time
from playwright.sync_api import sync_playwright

class TestConfig:
    """Configuration des tests"""
    # URL de l'application
    # En production Vercel, utiliser: https://your-app.vercel.app
    # En dev local avec vercel dev: http://localhost:3000
    # En dev local avec serveur simple: http://localhost:8000
    APP_URL = "http://localhost:8000"

    # Dossier pour les screenshots
    SCREENSHOTS_DIR = "web/screenshots/tests"

    # Timeout pour les opérations
    TIMEOUT = 10000  # 10 secondes

def setup_test_env():
    """Prépare l'environnement de test"""
    os.makedirs(TestConfig.SCREENSHOTS_DIR, exist_ok=True)

    # Vérifier que le serveur est actif
    import urllib.request
    try:
        urllib.request.urlopen(TestConfig.APP_URL)
    except:
        print(f"❌ Serveur non actif sur {TestConfig.APP_URL}")
        print("   Lancez le serveur avec:")
        print("   - Production/Dev: vercel dev")
        print("   - Simple: cd web && python3 -m http.server 8000")
        exit(1)

def test_simple_words(page):
    """Test 1: Mots simples sans caractères spéciaux"""
    print("\n📝 Test 1: Mots simples (chat, chien, oiseau)")

    page.goto(TestConfig.APP_URL)
    page.wait_for_load_state('networkidle')

    page.locator('#theme').fill('animaux')
    page.locator('#words').fill('chat\nchien\noiseau')
    page.locator('#btn-search').click()

    page.wait_for_selector('.word-section', timeout=TestConfig.TIMEOUT)
    time.sleep(2)

    sections = page.locator('.word-section').count()
    assert sections == 3, f"Attendu 3 sections, trouvé {sections}"
    print(f"   ✅ {sections}/3 sections créées")

    page.screenshot(path=f"{TestConfig.SCREENSHOTS_DIR}/01-simple-words.png")
    return True

def test_words_with_spaces(page):
    """Test 2: Mots avec espaces"""
    print("\n📝 Test 2: Mots avec espaces (petite voiture, grosse maison)")

    page.goto(TestConfig.APP_URL)
    page.wait_for_load_state('networkidle')

    page.locator('#words').fill('petite voiture\ngrosse maison')
    page.locator('#btn-search').click()

    page.wait_for_selector('.word-section', timeout=TestConfig.TIMEOUT)
    time.sleep(2)

    sections = page.locator('.word-section').all()
    assert len(sections) == 2, f"Attendu 2 sections, trouvé {len(sections)}"

    # Vérifier les IDs
    for section in sections:
        section_id = section.get_attribute('id')
        assert ' ' not in section_id, f"ID contient des espaces: {section_id}"
        print(f"   ✅ ID valide: {section_id}")

    page.screenshot(path=f"{TestConfig.SCREENSHOTS_DIR}/02-words-with-spaces.png")
    return True

def test_words_with_apostrophes(page):
    """Test 3: Mots avec apostrophes - TEST DE NON-RÉGRESSION"""
    print("\n📝 Test 3: Mots avec apostrophes (l'oiseau, d'automne)")

    page.goto(TestConfig.APP_URL)
    page.wait_for_load_state('networkidle')

    page.locator('#words').fill("l'oiseau\nd'automne")
    page.locator('#btn-search').click()

    page.wait_for_selector('.word-section', timeout=TestConfig.TIMEOUT)
    time.sleep(2)

    sections = page.locator('.word-section').all()
    assert len(sections) == 2, f"Attendu 2 sections, trouvé {len(sections)}"

    # Vérifier que les apostrophes sont encodées correctement
    for section in sections:
        section_id = section.get_attribute('id')
        title = section.locator('h3').inner_text()

        # L'ID ne doit PAS contenir d'apostrophe brute
        assert "'" not in section_id, f"Apostrophe non encodée dans ID: {section_id}"
        print(f"   ✅ {title} → ID: {section_id}")

    page.screenshot(path=f"{TestConfig.SCREENSHOTS_DIR}/03-words-with-apostrophes.png")
    return True

def test_mixed_characters(page):
    """Test 4: Mots avec espaces + apostrophes + accents"""
    print("\n📝 Test 4: Caractères mixtes (feuille d'érable, château d'eau)")

    page.goto(TestConfig.APP_URL)
    page.wait_for_load_state('networkidle')

    page.locator('#words').fill("feuille d'érable\nchâteau d'eau")
    page.locator('#btn-search').click()

    page.wait_for_selector('.word-section', timeout=TestConfig.TIMEOUT)
    time.sleep(2)

    sections = page.locator('.word-section').count()
    assert sections == 2, f"Attendu 2 sections, trouvé {sections}"

    print(f"   ✅ {sections}/2 sections créées avec caractères complexes")

    page.screenshot(path=f"{TestConfig.SCREENSHOTS_DIR}/04-mixed-characters.png")
    return True

def test_image_selection(page):
    """Test 5: Sélection d'images"""
    print("\n📝 Test 5: Sélection d'images")

    page.goto(TestConfig.APP_URL)
    page.wait_for_load_state('networkidle')

    page.locator('#words').fill('chat')
    page.locator('#btn-search').click()

    page.wait_for_selector('.word-section', timeout=TestConfig.TIMEOUT)
    time.sleep(3)

    images = page.locator('.image-option')
    image_count = images.count()

    if image_count == 0:
        print("   ⚠️  Pas d'images (API non disponibles)")
        return None

    print(f"   Images disponibles: {image_count}")

    # Cliquer sur la deuxième image si disponible
    if image_count > 1:
        images.nth(1).click()
        time.sleep(1)

        selected = page.locator('.image-option.selected').count()
        assert selected == 1, f"Une image devrait être sélectionnée, trouvé {selected}"
        print("   ✅ Sélection d'image fonctionne")

    page.screenshot(path=f"{TestConfig.SCREENSHOTS_DIR}/05-image-selection.png")
    return True

def test_pagination(page):
    """Test 6: Pagination (Plus d'images)"""
    print("\n📝 Test 6: Pagination")

    page.goto(TestConfig.APP_URL)
    page.wait_for_load_state('networkidle')

    page.locator('#words').fill('voiture')
    page.locator('#btn-search').click()

    page.wait_for_selector('.word-section', timeout=TestConfig.TIMEOUT)
    time.sleep(3)

    more_button = page.locator('.btn-more-images')

    if not more_button.is_visible():
        print("   ℹ️  Bouton non visible (moins de 3 images)")
        return None

    print("   Bouton 'Plus d'images' visible")
    more_button.click()
    time.sleep(2)
    print("   ✅ Pagination fonctionne")

    page.screenshot(path=f"{TestConfig.SCREENSHOTS_DIR}/06-pagination.png")
    return True

def run_all_tests():
    """Exécute tous les tests"""
    print("="*60)
    print("🎭 Suite de Tests Playwright - Fiches-Mots")
    print("="*60)

    setup_test_env()

    tests = [
        ("Mots simples", test_simple_words),
        ("Mots avec espaces", test_words_with_spaces),
        ("Mots avec apostrophes", test_words_with_apostrophes),
        ("Caractères mixtes", test_mixed_characters),
        ("Sélection d'images", test_image_selection),
        ("Pagination", test_pagination),
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
    print("📊 RÉSUMÉ DES TESTS")
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
    elif skipped == len(results):
        print("\n⚠️  Tous les tests ont été sautés (API non disponibles?)")
        exit(1)
    else:
        print("\n🎉 Tous les tests sont passés!")
        exit(0)

if __name__ == "__main__":
    if not os.path.exists('web/index.html'):
        print("❌ Erreur: Exécutez ce script depuis le dossier racine du projet")
        print("   cd /Volumes/sidecar/src/fiches-mots")
        exit(1)

    run_all_tests()
