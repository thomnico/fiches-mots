#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tests unitaires pour vérifier le remplacement de Œ/œ en cursif
"""

import re

def test_cursive_replacement_logic():
    """Test unitaire: Logique de remplacement Œ/œ → OE/oe"""
    print("\n" + "="*60)
    print("🧪 Test Unitaire: Remplacement Œ/œ en cursif")
    print("="*60)

    # Mots de test avec Œ/œ
    test_cases = [
        ("œuf", "oeuf"),
        ("œuvre", "oeuvre"),
        ("œil", "oeil"),
        ("cœur", "coeur"),
        ("bœuf", "boeuf"),
        ("Œuvre", "oeuvre"),  # Avec majuscule
        ("ŒUVRE", "oeuvre"),  # Tout en majuscule
        ("sœur", "soeur"),
        ("nœud", "noeud"),
        ("vœu", "voeu"),
    ]

    print("\n📝 Cas de test:")
    all_passed = True

    for original, expected in test_cases:
        # Simuler la logique JavaScript:
        # word.toLowerCase().replace(/œ/g, 'oe').replace(/Œ/g, 'oe')
        cursive_word = original.lower()
        cursive_word = cursive_word.replace('œ', 'oe')
        cursive_word = cursive_word.replace('Œ', 'oe')

        passed = cursive_word == expected
        status = "✅" if passed else "❌"
        print(f"  {status} '{original}' → '{cursive_word}' (attendu: '{expected}')")

        if not passed:
            all_passed = False

    print("\n" + "="*60)
    if all_passed:
        print("✅ TOUS LES TESTS RÉUSSIS")
    else:
        print("❌ CERTAINS TESTS ONT ÉCHOUÉ")
    print("="*60)

    return all_passed

def verify_code_contains_replacement():
    """Vérifie que le code contient bien la logique de remplacement"""
    print("\n" + "="*60)
    print("🔍 Vérification du code source")
    print("="*60)

    import os
    pdf_generator_path = "web/js/pdfGenerator.js"

    if not os.path.exists(pdf_generator_path):
        print(f"❌ Fichier non trouvé: {pdf_generator_path}")
        return False

    with open(pdf_generator_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Vérifier la présence du remplacement
    has_oe_lower = ".replace(/œ/g, 'oe')" in content or '.replace(/œ/g, "oe")' in content
    has_oe_upper = ".replace(/Œ/g, 'oe')" in content or '.replace(/Œ/g, "oe")' in content
    has_cursive_word = "cursiveWord" in content

    print(f"  {'✅' if has_oe_lower else '❌'} Contient remplacement œ → oe")
    print(f"  {'✅' if has_oe_upper else '❌'} Contient remplacement Œ → oe")
    print(f"  {'✅' if has_cursive_word else '❌'} Utilise variable cursiveWord")

    all_checks = has_oe_lower and has_oe_upper and has_cursive_word

    print("\n" + "="*60)
    if all_checks:
        print("✅ CODE SOURCE VALIDE")
    else:
        print("❌ CODE SOURCE INCOMPLET")
    print("="*60)

    return all_checks

if __name__ == '__main__':
    import sys

    print("\n" + "="*60)
    print("🧪 SUITE DE TESTS - Cursif Œ/œ → OE/oe")
    print("="*60)

    test1_passed = test_cursive_replacement_logic()
    test2_passed = verify_code_contains_replacement()

    print("\n" + "="*60)
    print("📊 RÉSUMÉ")
    print("="*60)
    print(f"  {'✅' if test1_passed else '❌'} Tests unitaires logique")
    print(f"  {'✅' if test2_passed else '❌'} Vérification code source")
    print("="*60)

    all_passed = test1_passed and test2_passed

    if all_passed:
        print("🎉 TOUS LES TESTS SONT PASSÉS!")
    else:
        print("⚠️  CERTAINS TESTS ONT ÉCHOUÉ")

    sys.exit(0 if all_passed else 1)
