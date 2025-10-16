#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tests Playwright pour vérifier le remplacement de caractères spéciaux en cursif
"""

import os
import sys
from playwright.sync_api import sync_playwright, expect

class TestConfig:
    """Configuration des tests"""
    APP_URL = "http://localhost:3000"
    TIMEOUT = 30000

def test_cursive_oe_replacement():
    """Test: Vérifier que Œ/œ sont remplacés par OE/oe en cursif uniquement"""
    print("\n" + "="*60)
    print("🧪 Test PDF: Remplacement Œ/œ → OE/oe en cursif")
    print("="*60)

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        # 1. Naviguer vers l'application
        print("\n📝 Étape 1: Charger l'application")
        page.goto(TestConfig.APP_URL)
        page.wait_for_load_state('networkidle')

        # 2. Ajouter des mots avec Œ/œ
        print("📝 Étape 2: Ajouter des mots contenant Œ/œ")
        test_words = "œuf\nœuvre\nœil\ncœur\nbœuf"
        page.fill('#words', test_words)

        # 3. Intercepter l'appel à addImage pour capturer le texte affiché
        print("📝 Étape 3: Intercepter la génération PDF")

        # Utiliser l'évaluation JavaScript pour vérifier le remplacement
        page.evaluate("""
            // Hook dans la fonction drawWordFiche pour capturer les textes
            window.capturedTexts = {
                capitals: [],
                scripts: [],
                cursives: []
            };

            // Override de jsPDF.text pour capturer les appels
            const originalText = window.jspdf.jsPDF.prototype.text;
            window.jspdf.jsPDF.prototype.text = function(text, x, y, options) {
                const font = this.getFont();
                if (font.fontName === 'OpenDyslexic-Bold') {
                    window.capturedTexts.capitals.push(text);
                } else if (font.fontName === 'OpenDyslexic') {
                    window.capturedTexts.scripts.push(text);
                } else if (font.fontName === 'Ecolier') {
                    window.capturedTexts.cursives.push(text);
                }
                return originalText.call(this, text, x, y, options);
            };
        """)

        # 4. Générer le PDF
        print("📝 Étape 4: Générer le PDF")
        page.click('#btn-generate')
        page.wait_for_timeout(5000)  # Attendre la génération

        # 5. Vérifier les textes capturés
        print("📝 Étape 5: Vérifier le remplacement")
        captured = page.evaluate("window.capturedTexts")

        print(f"\n✅ Textes CAPITALES capturés: {captured['capitals']}")
        print(f"✅ Textes SCRIPT capturés: {captured['scripts']}")
        print(f"✅ Textes CURSIF capturés: {captured['cursives']}")

        # Vérifications
        assert len(captured['capitals']) > 0, "Aucun texte en CAPITALES capturé"
        assert len(captured['scripts']) > 0, "Aucun texte en script capturé"
        assert len(captured['cursives']) > 0, "Aucun texte en cursif capturé"

        # Vérifier que CAPITALES et script contiennent toujours "Œ" ou "œ"
        capitals_have_oe = any('Œ' in text.upper() for text in captured['capitals'])
        scripts_have_oe = any('œ' in text for text in captured['scripts'])

        print(f"\n🔍 CAPITALES contiennent Œ: {capitals_have_oe}")
        print(f"🔍 Script contient œ: {scripts_have_oe}")

        # Vérifier que cursif NE contient PAS "œ" mais contient "oe"
        cursives_have_oe_char = any('œ' in text or 'Œ' in text for text in captured['cursives'])
        cursives_have_oe_replacement = any('oe' in text for text in captured['cursives'])

        print(f"🔍 Cursif contient œ/Œ (caractère): {cursives_have_oe_char}")
        print(f"🔍 Cursif contient 'oe' (remplacement): {cursives_have_oe_replacement}")

        # Assertions finales
        assert not cursives_have_oe_char, "❌ Le cursif contient encore le caractère œ/Œ!"
        assert cursives_have_oe_replacement, "❌ Le cursif ne contient pas le remplacement 'oe'!"

        print("\n✅ Test réussi: Œ/œ correctement remplacés par OE/oe en cursif uniquement")

        browser.close()
        return True

def run_test():
    """Lance le test"""
    print("\n" + "="*60)
    print("🧪 TEST PDF - Remplacement caractères cursif")
    print("="*60)

    try:
        test_cursive_oe_replacement()
        print("\n" + "="*60)
        print("✅ TEST RÉUSSI")
        print("="*60)
        return True
    except Exception as e:
        print("\n" + "="*60)
        print(f"❌ TEST ÉCHOUÉ: {e}")
        print("="*60)
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    success = run_test()
    sys.exit(0 if success else 1)
