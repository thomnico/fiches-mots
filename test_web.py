#!/usr/bin/env python3
"""
Script de test Playwright pour l'interface web du générateur de fiches
"""

import os
import time
from playwright.sync_api import sync_playwright

def test_web_interface():
    """Teste l'interface web avec Playwright"""

    print("🎭 Démarrage des tests Playwright")
    print("=" * 60)

    with sync_playwright() as p:
        # Lancer le navigateur
        print("🌐 Lancement du navigateur Chromium...")
        browser = p.chromium.launch(headless=False)  # headless=False pour voir le test
        context = browser.new_context(viewport={'width': 1280, 'height': 800})
        page = context.new_page()

        try:
            # Naviguer vers l'application
            # Utiliser HTTP au lieu de file:// pour que les APIs fonctionnent
            url = "http://localhost:8000/"
            print(f"📂 Ouverture de: {url}")
            page.goto(url)

            # Attendre que la page se charge
            page.wait_for_load_state('networkidle')
            print("✅ Page chargée")

            # Capture d'écran de l'état initial
            screenshots_dir = 'web/screenshots'
            os.makedirs(screenshots_dir, exist_ok=True)

            print("\n📸 Capture d'écran 1: État initial")
            page.screenshot(path=f"{screenshots_dir}/01-initial.png")

            # Test 1: Remplir le formulaire
            print("\n📝 Test 1: Remplissage du formulaire")

            # Entrer le thème
            theme_input = page.locator('#theme')
            theme_input.fill('animaux')
            print("   ✓ Thème saisi: animaux")

            # Entrer les mots (comme dans mots_animaux.txt)
            words_input = page.locator('#words')
            words_text = "chat\nchien\noiseau\npoisson"
            words_input.fill(words_text)
            print(f"   ✓ Mots saisis: {words_text.replace(chr(10), ', ')}")

            time.sleep(1)
            page.screenshot(path=f"{screenshots_dir}/02-formulaire-rempli.png")

            # Test 2: Cliquer sur recherche d'images
            print("\n🔍 Test 2: Recherche d'images")

            # Capturer les logs de la console
            console_logs = []
            def handle_console(msg):
                console_logs.append(f"   [{msg.type}] {msg.text}")
            page.on("console", handle_console)

            search_button = page.locator('#btn-search')
            search_button.click()
            print("   ✓ Bouton 'Rechercher' cliqué")

            # Attendre que les images se chargent
            print("   ⏳ Attente du chargement des sections...")
            page.wait_for_selector('.word-section', timeout=10000)

            # Attendre que les images soient visibles (pas juste les conteneurs)
            print("   ⏳ Attente du chargement des images (proxy CORS peut être lent)...")
            page.wait_for_selector('.image-option img', timeout=20000)

            # Attendre plus longtemps pour les proxies CORS
            print("   ⏳ Attente supplémentaire pour les proxies (30 sec)...")
            time.sleep(30)

            page.screenshot(path=f"{screenshots_dir}/03-images-chargees.png")
            print("   ✅ Images chargées")

            # Afficher les derniers logs
            print("\n   📋 Logs console (derniers 30):")
            for log in console_logs[-30:]:
                print(log)

            # Test 3: Vérifier le nombre de sections de mots
            word_sections = page.locator('.word-section').count()
            print(f"   ✓ {word_sections} sections de mots trouvées")

            # Test 4: Vérifier les images pour chaque mot
            print("\n🖼️ Test 3: Vérification des images")
            for i in range(word_sections):
                section = page.locator('.word-section').nth(i)
                word_title = section.locator('h3').inner_text()
                images_count = section.locator('.image-option').count()
                print(f"   ✓ {word_title}: {images_count} images proposées")

            # Test 5: Sélectionner une image différente pour le premier mot
            print("\n✅ Test 4: Sélection d'une image")
            first_word_section = page.locator('.word-section').first
            second_image = first_word_section.locator('.image-option').nth(1)
            second_image.click()
            print("   ✓ Deuxième image sélectionnée pour le premier mot")

            time.sleep(1)
            page.screenshot(path=f"{screenshots_dir}/04-image-selectionnee.png")

            # Test 6: Générer le PDF
            print("\n📄 Test 5: Génération du PDF")
            generate_button = page.locator('#btn-generate')
            generate_button.click()
            print("   ✓ Bouton 'Générer PDF' cliqué")

            # Attendre l'écran de génération
            page.wait_for_selector('#step-generate.active', timeout=5000)
            time.sleep(2)
            page.screenshot(path=f"{screenshots_dir}/05-generation-pdf.png")
            print("   ✅ Écran de génération affiché")

            # Attendre que la génération se termine
            # (Le PDF devrait se télécharger automatiquement)
            time.sleep(3)

            print("\n" + "=" * 60)
            print("✅ Tests terminés avec succès!")
            print(f"📸 Captures d'écran sauvegardées dans: {screenshots_dir}/")
            print("\nCaptures créées:")
            for i, name in enumerate([
                "01-initial.png - État initial de l'application",
                "02-formulaire-rempli.png - Formulaire avec thème et mots",
                "03-images-chargees.png - Images proposées pour chaque mot",
                "04-image-selectionnee.png - Sélection d'une image",
                "05-generation-pdf.png - Écran de génération PDF"
            ], 1):
                print(f"   {i}. {name}")

        except Exception as e:
            print(f"\n❌ Erreur durant les tests: {e}")
            page.screenshot(path=f"{screenshots_dir}/error.png")
            raise

        finally:
            # Laisser le navigateur ouvert quelques secondes pour voir le résultat
            print("\n⏸️  Navigateur ouvert pendant 5 secondes...")
            time.sleep(5)

            # Fermer le navigateur
            browser.close()
            print("🔒 Navigateur fermé")


if __name__ == "__main__":
    # Vérifier qu'on est dans le bon dossier
    if not os.path.exists('web/index.html'):
        print("❌ Erreur: Exécutez ce script depuis le dossier racine du projet")
        print("   cd /Volumes/sidecar/src/fiches-mots")
        exit(1)

    test_web_interface()
