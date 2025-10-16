#!/usr/bin/env python3
"""
Test de debug pour identifier le problème de génération Mistral
"""

import os
import time
from playwright.sync_api import sync_playwright

APP_URL = "http://localhost:3000"

def test_mistral_generation():
    """Test debug de la génération Mistral"""
    print("🔍 Test debug - Génération Mistral")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        # Activer la console
        page.on("console", lambda msg: print(f"   CONSOLE [{msg.type}]: {msg.text}"))
        page.on("pageerror", lambda err: print(f"   ERROR: {err}"))

        # Aller sur la page
        page.goto(APP_URL)
        page.wait_for_load_state('networkidle')

        print("\n1️⃣ Remplir le thème")
        page.locator('#theme').fill('test')

        print("\n2️⃣ Cliquer sur le Chat Magique")
        page.locator('#btn-magic').click()

        print("\n3️⃣ Attendre la réponse...")

        # Attendre max 30 secondes
        try:
            page.wait_for_function(
                "document.querySelector('#btn-magic').disabled === false",
                timeout=30000
            )
            print("   ✅ Bouton réactivé")
        except Exception as e:
            print(f"   ❌ Timeout: {e}")

        # Vérifier le contenu du textarea
        time.sleep(2)
        words_value = page.locator('#words').input_value()

        print(f"\n4️⃣ Contenu du textarea:")
        print(f"   Longueur: {len(words_value)} caractères")
        print(f"   Contenu: {repr(words_value[:200])}")

        if words_value:
            words = [w.strip() for w in words_value.split('\n') if w.strip()]
            print(f"   Mots générés: {len(words)}")
            print(f"   Liste: {words}")
        else:
            print("   ⚠️ VIDE !")

        # Screenshot
        os.makedirs("web/screenshots/debug", exist_ok=True)
        page.screenshot(path="web/screenshots/debug/mistral-debug.png")
        print("\n📸 Screenshot: web/screenshots/debug/mistral-debug.png")

        input("\n⏸️  Appuyez sur Entrée pour fermer...")
        browser.close()

if __name__ == "__main__":
    test_mistral_generation()
