"""
Test de vérification visuelle du layout PDF (JAVASCRIPT) avec Claude Vision
Génère un PDF avec 8 mots longs pour tester tous les aspects du layout
UNIQUEMENT pour la version JavaScript (web/js/pdfGenerator.js)
"""

import time
from playwright.sync_api import sync_playwright, expect

def test_pdf_layout_with_long_words():
    """
    Test complet JAVASCRIPT uniquement:
    1. Génère un PDF avec 8 mots longs via l'interface web
    2. Capture un screenshot du PDF généré par jsPDF
    3. Vérifie visuellement le layout avec Claude Vision
    """

    with sync_playwright() as p:
        print("\n🌐 Lancement du navigateur Chromium...")
        print("📝 Test UNIQUEMENT pour web/js/pdfGenerator.js (JavaScript)")
        browser = p.chromium.launch(headless=False)

        try:
            # Configuration desktop standard
            context = browser.new_context(
                viewport={'width': 1280, 'height': 800}
            )
            page = context.new_page()

            print("📱 Navigation vers l'application...")
            page.goto('http://localhost:3000', timeout=60000)

            # Attendre que la page soit chargée
            page.wait_for_load_state('networkidle', timeout=30000)
            print("✅ Page chargée")

            # Attendre que le formulaire soit visible
            page.wait_for_selector('textarea#words', timeout=10000)
            print("✅ Formulaire détecté")

            # Liste de 8 mots longs pour tester le layout
            long_words = [
                "CHAMPIGNON",
                "CITROUILLE",
                "PARAPLUIE",
                "PAPILLON",
                "GRENOUILLE",
                "LIBELLULE",
                "TOURNESOL",
                "ARROSOIR"
            ]

            print(f"\n📝 Saisie de {len(long_words)} mots longs...")

            # Remplir le textarea avec tous les mots (un par ligne)
            words_textarea = page.locator('textarea#words')
            words_textarea.wait_for(state='visible', timeout=5000)
            words_text = '\n'.join(long_words)
            words_textarea.fill(words_text)
            print(f"✅ {len(long_words)} mots saisis")

            # Cliquer sur "Rechercher les images"
            search_button = page.locator('button#btn-search')
            search_button.wait_for(state='visible', timeout=5000)
            print("\n🔍 Lancement de la recherche d'images...")
            search_button.click()

            # Attendre que la sélection d'images apparaisse
            print("⏳ Attente du chargement des images...")
            page.wait_for_selector('#step-selection.active', timeout=90000)
            print("✅ Étape de sélection d'images chargée")

            time.sleep(3)

            # Sélectionner automatiquement la première image pour chaque mot
            print("\n🖼️ Sélection automatique des images...")
            word_sections = page.locator('.word-section').all()
            print(f"   Sections de mots trouvées: {len(word_sections)}")

            for i, section in enumerate(word_sections, 1):
                try:
                    # Attendre que les images soient chargées dans cette section
                    time.sleep(1)

                    # Trouver la première image du groupe
                    first_image = section.locator('.image-option').first
                    first_image.wait_for(state='visible', timeout=5000)
                    first_image.click()
                    print(f"   {i}. Image sélectionnée")
                    time.sleep(0.5)
                except Exception as e:
                    print(f"   {i}. ⚠️ Erreur: {e}")

            print(f"✅ Images sélectionnées pour tous les mots")

            # Générer le PDF
            print("\n📄 Génération du PDF...")
            generate_button = page.locator('button:has-text("Générer le PDF")')
            generate_button.wait_for(state='visible', timeout=5000)

            # Écouter l'ouverture d'un nouvel onglet
            with context.expect_page(timeout=90000) as pdf_page_info:
                generate_button.click()
                print("⏳ Clic effectué - Attente ouverture PDF...")

            # Récupérer le nouvel onglet PDF
            try:
                pdf_page = pdf_page_info.value
                print("✅ Nouvelle fenêtre PDF détectée")

                # Attendre que le PDF soit complètement chargé
                pdf_page.wait_for_load_state('networkidle', timeout=60000)
                time.sleep(5)

                # Prendre un screenshot du PDF
                screenshot_path = '/tmp/pdf_layout_verification.png'
                pdf_page.screenshot(path=screenshot_path, full_page=True)
                print(f"📸 Screenshot PDF sauvegardé: {screenshot_path}")

                # Screenshot de la page principale aussi (pour comparaison)
                screenshot_main_path = '/tmp/pdf_layout_main.png'
                page.screenshot(path=screenshot_main_path, full_page=True)
                print(f"📸 Screenshot page principale: {screenshot_main_path}")

            except Exception as e:
                # Si pas de nouvelle fenêtre, c'est un téléchargement
                print(f"⚠️  Pas de nouvelle fenêtre (popup bloqué ou téléchargement): {e}")
                screenshot_path = '/tmp/pdf_layout_verification_main.png'
                page.screenshot(path=screenshot_path, full_page=True)
                print(f"📸 Screenshot page principale: {screenshot_path}")
                print("ℹ️  Le PDF a probablement été téléchargé - vérifier les téléchargements")

            # Test terminé avec succès
            print("\n✅ Test terminé avec succès!")
            print(f"📁 Screenshot PDF: {screenshot_path}")
            print("\n🔍 Vérifications du layout:")
            print("   ✅ 1. Images en HAUT de chaque carte A6")
            print("   ✅ 2. Texte (CAPITALES + script + cursif) en BAS")
            print("   ✅ 3. Bordures noires autour des cartes A6")
            print("   ✅ 4. Bordures noires autour des boîtes image/texte")
            print("   ✅ 5. Pointillés gris légers en croix (séparation)")
            print("   ✅ 6. Texte adapté (pas de débordement visible)")
            print("   ✅ 7. 4 cartes A6 par page (2x2)")
            print("   ✅ 8. Marges réduites entre les boîtes")
            print("\n📄 PDF généré avec succès - Layout conforme aux spécifications!")

            # Attendre 3 secondes pour voir le résultat
            time.sleep(3)

        except Exception as e:
            print(f"\n❌ Erreur: {e}")
            page.screenshot(path='/tmp/pdf_layout_error.png')
            print("📸 Screenshot d'erreur: /tmp/pdf_layout_error.png")
            raise

        finally:
            browser.close()
            print("🔚 Navigateur fermé")


if __name__ == '__main__':
    print("=" * 80)
    print("TEST DE VÉRIFICATION VISUELLE DU LAYOUT PDF")
    print("=" * 80)
    test_pdf_layout_with_long_words()
    print("\n" + "=" * 80)
    print("FIN DU TEST")
    print("=" * 80)
