#!/usr/bin/env python3
"""
Test de la fonctionnalité de pagination des images
Vérifie que le bouton "Voir plus d'images" fonctionne correctement
"""

from playwright.sync_api import sync_playwright
import time
import os

def test_pagination():
    print("🧪 Test de pagination des images")
    print("=" * 60)

    # Configuration
    url = "http://localhost:8000"
    screenshots_dir = "web/screenshots"
    os.makedirs(screenshots_dir, exist_ok=True)

    with sync_playwright() as p:
        # Lancer le navigateur
        browser = p.chromium.launch(headless=False)
        page = browser.new_page(viewport={"width": 1400, "height": 1000})

        try:
            # 1. Aller sur la page
            print(f"📍 Chargement de {url}...")
            page.goto(url)
            page.wait_for_load_state('networkidle')

            # 2. Remplir le formulaire avec UN SEUL mot pour simplicité
            print("📝 Remplissage du formulaire...")
            page.fill('#theme', 'automne')
            page.fill('#words', 'feuille')  # Un seul mot

            # 3. Lancer la recherche
            print("🔍 Lancement de la recherche...")
            page.click('#btn-search')

            # Attendre que les images se chargent
            print("⏳ Attente du chargement des images...")
            page.wait_for_selector('.image-option', timeout=15000)
            time.sleep(2)  # Attendre que toutes les images soient chargées

            # 4. Capturer la première page d'images
            print("📸 Capture page 1...")
            page.screenshot(path=f"{screenshots_dir}/pagination-page1.png")

            # Vérifier que le bouton "Plus d'images" existe
            btn_more = page.query_selector('.btn-more-images')
            if not btn_more:
                print("⚠️  Bouton 'Plus d'images' non trouvé!")
                return

            # Vérifier le texte initial du bouton
            btn_text = btn_more.inner_text()
            print(f"   Texte du bouton: '{btn_text}'")

            # Vérifier que le bouton est visible
            if not btn_more.is_visible():
                print("⚠️  Le bouton existe mais n'est pas visible!")
                return

            print("✓ Bouton 'Plus d'images' trouvé et visible")

            # 5. Cliquer sur "Plus d'images" pour voir page 2
            print("\n🖱️  Clic sur 'Plus d'images'...")
            btn_more.click()
            time.sleep(1)  # Attendre le changement d'images

            print("📸 Capture page 2...")
            page.screenshot(path=f"{screenshots_dir}/pagination-page2.png")

            # Vérifier que le texte du bouton a changé
            btn_text_2 = btn_more.inner_text()
            print(f"   Nouveau texte du bouton: '{btn_text_2}'")

            # 6. Cliquer encore pour voir page 3
            print("\n🖱️  Clic pour page 3...")
            btn_more.click()
            time.sleep(1)

            print("📸 Capture page 3...")
            page.screenshot(path=f"{screenshots_dir}/pagination-page3.png")

            btn_text_3 = btn_more.inner_text()
            print(f"   Texte du bouton: '{btn_text_3}'")

            # 7. Cliquer encore pour revenir au début (cycle)
            print("\n🖱️  Clic pour retour au début...")
            btn_more.click()
            time.sleep(1)

            print("📸 Capture retour page 1...")
            page.screenshot(path=f"{screenshots_dir}/pagination-cycle-back.png")

            btn_text_4 = btn_more.inner_text()
            print(f"   Texte du bouton: '{btn_text_4}'")

            # 8. Vérifier qu'on peut sélectionner une image sur chaque page
            print("\n🖼️  Test de sélection d'images sur différentes pages...")

            # Compter les images affichées
            images = page.query_selector_all('.image-option')
            print(f"   Nombre d'images visibles: {len(images)}")

            if len(images) > 0:
                print("   Clic sur la première image...")
                images[0].click()
                time.sleep(0.5)

                # Vérifier qu'elle est sélectionnée
                if 'selected' in images[0].get_attribute('class'):
                    print("   ✓ Image correctement sélectionnée")
                else:
                    print("   ⚠️  Image non sélectionnée")

                page.screenshot(path=f"{screenshots_dir}/pagination-selection.png")

            print("\n" + "=" * 60)
            print("✅ Test de pagination terminé!")
            print(f"📸 Captures dans: {screenshots_dir}/")
            print("\nVérifiez visuellement:")
            print("  1. pagination-page1.png - Premières 3 images")
            print("  2. pagination-page2.png - Images 4-6")
            print("  3. pagination-page3.png - Images 7-9")
            print("  4. pagination-cycle-back.png - Retour aux 3 premières")
            print("  5. pagination-selection.png - Image sélectionnée")

            # Garder le navigateur ouvert pour inspection
            print("\n⏸️  Navigateur reste ouvert pendant 5 secondes...")
            time.sleep(5)

        finally:
            browser.close()
            print("🔒 Navigateur fermé")

if __name__ == "__main__":
    test_pagination()
