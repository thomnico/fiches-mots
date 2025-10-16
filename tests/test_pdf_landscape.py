#!/usr/bin/env python3
"""
Test de debug pour la génération PDF en paysage
"""

import os
import time
from playwright.sync_api import sync_playwright

APP_URL = "http://localhost:3000"

def test_pdf_generation():
    """Test debug génération PDF paysage"""
    print("🔍 Test debug - Génération PDF paysage")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        # Capturer les erreurs console
        page.on("console", lambda msg: print(f"   [{msg.type.upper()}] {msg.text}"))
        page.on("pageerror", lambda err: print(f"   [ERROR] {err}"))

        # Aller sur la page
        page.goto(APP_URL)
        page.wait_for_load_state('networkidle')

        print("\n1️⃣ Entrer des mots de test")
        page.locator('#words').fill('chat\nchien\noiseau')

        print("\n2️⃣ Cliquer sur 'Rechercher les images'")
        page.locator('#btn-search').click()

        # Attendre les sections
        print("\n3️⃣ Attendre les images...")
        page.wait_for_selector('.word-section', timeout=15000)
        time.sleep(3)

        sections = page.locator('.word-section').count()
        print(f"   ✅ {sections} sections créées")

        # Sélectionner les premières images
        print("\n4️⃣ Sélectionner les images...")
        for i in range(min(sections, 3)):
            images = page.locator(f'.word-section').nth(i).locator('.image-option')
            if images.count() > 0:
                images.first.click()
                time.sleep(0.5)

        print("\n5️⃣ Cliquer sur 'Générer le PDF'")
        page.locator('#btn-generate').click()

        # Attendre la génération
        print("\n6️⃣ Génération en cours...")
        time.sleep(5)

        print("\n7️⃣ Vérifier s'il y a des erreurs...")

        # Screenshot
        os.makedirs("web/screenshots/debug", exist_ok=True)
        page.screenshot(path="web/screenshots/debug/pdf-generation.png")
        print("\n📸 Screenshot: web/screenshots/debug/pdf-generation.png")

        input("\n⏸️  Appuyez sur Entrée pour fermer...")
        browser.close()

if __name__ == "__main__":
    test_pdf_generation()
