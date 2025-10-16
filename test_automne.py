#!/usr/bin/env python3
"""
Test spécifique pour le thème AUTOMNE
Vérifie la variété des images proposées
"""

import os
import time
from playwright.sync_api import sync_playwright

def test_theme_automne():
    print("🍂 Test du thème AUTOMNE")
    print("=" * 60)

    project_root = os.getcwd()

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context(viewport={'width': 1400, 'height': 1000})
        page = context.new_page()

        try:
            # Naviguer vers l'application
            url = "http://localhost:8000/"
            print(f"📂 Ouverture de: {url}")
            page.goto(url)
            page.wait_for_load_state('networkidle')
            print("✅ Page chargée\n")

            # Remplir le formulaire avec le thème AUTOMNE
            print("📝 Remplissage du formulaire")
            theme_input = page.locator('#theme')
            theme_input.fill('automne')
            print("   ✓ Thème: automne")

            words_input = page.locator('#words')
            words_input.fill("feuille\nchampignon\ncitrouille\nmarron")
            print("   ✓ Mots: feuille, champignon, citrouille, marron\n")

            time.sleep(1)

            # Capturer les logs de la console
            console_logs = []
            def handle_console(msg):
                console_logs.append(f"   [{msg.type}] {msg.text}")
            page.on("console", handle_console)

            # Rechercher les images
            print("🔍 Recherche d'images...")
            search_button = page.locator('#btn-search')
            search_button.click()

            # Attendre le chargement
            page.wait_for_selector('.word-section', timeout=10000)
            page.wait_for_selector('.image-option img', timeout=20000)
            time.sleep(15)  # Attendre que Pixabay charge toutes les images

            print("✅ Images chargées\n")

            # Afficher les logs pertinents
            print("📋 Logs de recherche:")
            for log in console_logs:
                if 'Recherche' in log or 'trouvés' in log or 'Pixabay' in log:
                    print(log)

            print("\n" + "=" * 60)

            # Créer des screenshots pour inspection manuelle
            screenshots_dir = 'web/screenshots'
            os.makedirs(screenshots_dir, exist_ok=True)

            print("\n📸 Création des captures d'écran...")

            # Capture globale
            page.screenshot(path=f"{screenshots_dir}/automne-global.png")
            print("   ✓ automne-global.png")

            # Captures individuelles par mot
            word_sections = page.locator('.word-section').count()
            for i in range(min(word_sections, 4)):
                section = page.locator('.word-section').nth(i)
                word_title = section.locator('h3').inner_text()

                # Scroll vers la section
                section.scroll_into_view_if_needed()
                time.sleep(0.5)

                # Capture de la section
                section.screenshot(path=f"{screenshots_dir}/automne-{i+1}-{word_title.lower()}.png")
                print(f"   ✓ automne-{i+1}-{word_title.lower()}.png")

            print("\n" + "=" * 60)
            print("✅ Test terminé!")
            print(f"📸 Captures dans: {screenshots_dir}/")
            print("\nInspectez manuellement les images pour vérifier:")
            print("  1. La variété des images pour chaque mot")
            print("  2. La pertinence par rapport au thème automne")
            print("  3. La qualité des vecteurs Pixabay")

            # Garder le navigateur ouvert pour inspection
            print("\n⏸️  Navigateur reste ouvert pendant 10 secondes...")
            time.sleep(10)

        except Exception as e:
            print(f"\n❌ Erreur: {e}")
            raise
        finally:
            browser.close()
            print("🔒 Navigateur fermé")

if __name__ == '__main__':
    test_theme_automne()
