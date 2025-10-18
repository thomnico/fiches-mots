#!/usr/bin/env python3
"""
Suite de tests Playwright pour la génération de PDF
Teste la génération sur desktop et mobile avec vérifications complètes
"""

import os
import time
import json
from playwright.sync_api import sync_playwright, expect

class TestConfig:
    """Configuration des tests PDF"""
    # URL de l'application
    APP_URL = "http://localhost:3000"

    # Dossier pour les screenshots
    SCREENSHOTS_DIR = "web/screenshots/tests/pdf"

    # Timeouts adaptés pour réseau lent
    TIMEOUT = 60000  # 60 secondes (génération PDF + réseau lent)
    IMAGE_SEARCH_TIMEOUT = 90000  # 90 secondes pour recherche d'images

    # Nombre de tentatives en cas d'échec réseau
    MAX_RETRIES = 3
    RETRY_DELAY = 2  # secondes entre les tentatives

    # Configurations d'appareils (Firefox ne supporte pas is_mobile/has_touch)
    DEVICES = {
        'Desktop': {
            'viewport': {'width': 1280, 'height': 800},
            'user_agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
        },
        'iPhone 12': {
            'viewport': {'width': 390, 'height': 844},
            'user_agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) AppleWebKit/605.1.15',
            'device_scale_factor': 3,
        },
        'Pixel 5': {
            'viewport': {'width': 393, 'height': 851},
            'user_agent': 'Mozilla/5.0 (Linux; Android 11; Pixel 5) AppleWebKit/537.36',
            'device_scale_factor': 3,
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
        print("   Lancez: vercel dev")
        exit(1)

def test_pdf_generation_workflow(page, device_name):
    """Test 1: Workflow complet jusqu'à la génération du PDF"""
    print(f"\n📝 Test 1: Génération PDF - Workflow complet ({device_name})")

    # Configurer les événements de console pour détecter les erreurs
    console_errors = []
    console_logs = []
    page.on('console', lambda msg: (
        console_errors.append(msg.text) if msg.type == 'error' else
        console_logs.append(msg.text) if 'PDF' in msg.text or 'pdf' in msg.text else None
    ))

    # Augmenter le timeout de navigation pour réseau lent
    page.set_default_timeout(TestConfig.TIMEOUT)

    page.goto(TestConfig.APP_URL, wait_until='domcontentloaded')  # Plus rapide que networkidle
    page.wait_for_load_state('domcontentloaded')

    # Étape 1: Entrer des mots simples (moins de mots = plus rapide)
    words = ['chat', 'chien']
    page.locator('#words').fill('\n'.join(words))
    print(f"   Étape 1/4: Mots saisis: {', '.join(words)}")

    # Étape 2: Rechercher les images avec retry
    print("   Étape 2/4: Recherche d'images...")
    for attempt in range(TestConfig.MAX_RETRIES):
        try:
            page.locator('#btn-search').click()
            page.wait_for_selector('.word-section', timeout=TestConfig.IMAGE_SEARCH_TIMEOUT)

            # Attendre que toutes les sections soient créées
            page.wait_for_function(
                f"document.querySelectorAll('.word-section').length === {len(words)}",
                timeout=TestConfig.IMAGE_SEARCH_TIMEOUT
            )
            time.sleep(3)  # Attendre que les images soient chargées
            print("   Étape 2/4: Images recherchées ✓")
            break
        except Exception as e:
            if attempt < TestConfig.MAX_RETRIES - 1:
                print(f"      ⚠️  Tentative {attempt + 1} échouée, retry...")
                time.sleep(TestConfig.RETRY_DELAY)
                page.reload()
                page.locator('#words').fill('\n'.join(words))
            else:
                raise Exception(f"Échec après {TestConfig.MAX_RETRIES} tentatives: {e}")

    # Vérifier que des images sont sélectionnées
    selected_images = page.locator('.image-option.selected').count()
    assert selected_images > 0, "Aucune image sélectionnée"
    print(f"   Étape 3/4: {selected_images} images sélectionnées ✓")

    # Étape 3: Générer le PDF
    print("   Étape 4/4: Génération du PDF...")

    # Écouter les nouveaux onglets/popups
    popup_opened = []
    def handle_popup(popup):
        popup_opened.append(popup)
        print(f"      → Popup/onglet ouvert: {popup.url[:100]}")

    page.context.on('page', handle_popup)

    # Écouter les téléchargements
    downloads = []
    def handle_download(download):
        downloads.append(download)
        print(f"      → Téléchargement déclenché: {download.suggested_filename}")

    page.on('download', handle_download)

    # Cliquer sur "Générer le PDF"
    page.locator('#btn-generate').click()

    # Attendre que la génération soit terminée
    # On attend soit un popup, soit un téléchargement, soit un message de succès
    try:
        page.wait_for_function(
            "document.querySelector('#progress-text')?.textContent?.includes('succès')",
            timeout=TestConfig.TIMEOUT
        )
        time.sleep(2)  # Laisser le temps pour le popup/téléchargement
        print("      → Message de succès affiché ✓")
    except:
        print("      ⚠️  Pas de message de succès détecté")

    # Vérifier les logs de console
    pdf_logs = [log for log in console_logs if 'PDF' in log or 'généré' in log]
    if pdf_logs:
        print("      → Logs PDF:")
        for log in pdf_logs[:5]:
            print(f"         {log}")

    # Vérifier les erreurs
    if console_errors:
        print(f"      ⚠️  Erreurs console: {len(console_errors)}")
        for error in console_errors[:3]:
            print(f"         {error}")

    # Résultats
    results = {
        'popup_opened': len(popup_opened) > 0,
        'download_triggered': len(downloads) > 0,
        'console_errors': len(console_errors),
        'pdf_logs': len(pdf_logs)
    }

    print(f"\n   📊 Résultats:")
    print(f"      • Popup ouvert: {'✓' if results['popup_opened'] else '✗'}")
    print(f"      • Téléchargement: {'✓' if results['download_triggered'] else '✗'}")
    print(f"      • Logs PDF: {results['pdf_logs']}")
    print(f"      • Erreurs: {results['console_errors']}")

    page.screenshot(path=f"{TestConfig.SCREENSHOTS_DIR}/01-workflow-{device_name.replace(' ', '-')}.png")

    # Le test réussit si au moins un des deux (popup ou téléchargement) s'est produit
    success = results['popup_opened'] or results['download_triggered']

    if not success:
        print(f"   ❌ ÉCHEC: Ni popup ni téléchargement détecté sur {device_name}")
        return False

    print(f"   ✅ PDF généré avec succès sur {device_name}")
    return True

def test_pdf_blob_creation(page, device_name):
    """Test 2: Vérifier que le blob PDF est créé correctement"""
    print(f"\n📝 Test 2: Vérification création blob PDF ({device_name})")

    page.set_default_timeout(TestConfig.TIMEOUT)
    page.goto(TestConfig.APP_URL, wait_until='domcontentloaded')

    # Entrer des mots et rechercher les images avec retry
    words = ['rouge']
    page.locator('#words').fill('\n'.join(words))

    for attempt in range(TestConfig.MAX_RETRIES):
        try:
            page.locator('#btn-search').click()
            page.wait_for_selector('.word-section', timeout=TestConfig.IMAGE_SEARCH_TIMEOUT)
            page.wait_for_function(
                f"document.querySelectorAll('.word-section').length === {len(words)}",
                timeout=TestConfig.IMAGE_SEARCH_TIMEOUT
            )
            time.sleep(3)
            break
        except Exception as e:
            if attempt < TestConfig.MAX_RETRIES - 1:
                print(f"      ⚠️  Tentative {attempt + 1} échouée, retry...")
                time.sleep(TestConfig.RETRY_DELAY)
                page.reload()
                page.locator('#words').fill('\n'.join(words))
            else:
                print(f"      ⚠️  Impossible de charger les images après {TestConfig.MAX_RETRIES} tentatives")
                print(f"      Skip test (problème réseau probable)")
                return None

    # Injecter un script pour capturer le blob PDF
    page.evaluate("""
        window.pdfBlobCaptured = null;
        window.pdfUrlCaptured = null;

        // Override window.open pour capturer l'URL
        const originalOpen = window.open;
        window.open = function(url, target) {
            console.log('window.open appelé avec:', url);
            window.pdfUrlCaptured = url;
            return originalOpen.call(this, url, target);
        };

        // Hook dans pdfGenerator pour capturer le blob
        if (window.pdfGenerator) {
            const originalGenerate = window.pdfGenerator.generatePDF;
            window.pdfGenerator.generatePDF = async function(...args) {
                const result = await originalGenerate.apply(this, args);
                if (this.doc) {
                    window.pdfBlobCaptured = this.doc.output('blob');
                    console.log('Blob PDF capturé:', window.pdfBlobCaptured.size, 'bytes');
                }
                return result;
            };
        }
    """)

    # Générer le PDF
    page.locator('#btn-generate').click()

    try:
        page.wait_for_function(
            "document.querySelector('#progress-text')?.textContent?.includes('succès')",
            timeout=TestConfig.TIMEOUT
        )
        time.sleep(2)
    except:
        pass

    # Vérifier que le blob a été capturé
    blob_info = page.evaluate("""
        ({
            blobCaptured: window.pdfBlobCaptured !== null,
            blobSize: window.pdfBlobCaptured ? window.pdfBlobCaptured.size : 0,
            blobType: window.pdfBlobCaptured ? window.pdfBlobCaptured.type : null,
            urlCaptured: window.pdfUrlCaptured !== null,
            urlValue: window.pdfUrlCaptured ? window.pdfUrlCaptured.substring(0, 50) : null
        })
    """)

    print(f"   Blob capturé: {blob_info['blobCaptured']}")
    print(f"   Taille blob: {blob_info['blobSize']} bytes")
    print(f"   Type blob: {blob_info['blobType']}")
    print(f"   URL capturée: {blob_info['urlCaptured']}")
    if blob_info['urlValue']:
        print(f"   URL début: {blob_info['urlValue']}...")

    page.screenshot(path=f"{TestConfig.SCREENSHOTS_DIR}/02-blob-{device_name.replace(' ', '-')}.png")

    # Vérifications
    assert blob_info['blobSize'] > 0, f"Blob vide ou non créé (taille: {blob_info['blobSize']})"
    assert blob_info['blobType'] == 'application/pdf', f"Type incorrect: {blob_info['blobType']}"

    print(f"   ✅ Blob PDF créé correctement ({blob_info['blobSize']} bytes)")
    return True

def test_pdf_download_fallback(page, device_name):
    """Test 3: Test du fallback de téléchargement si window.open échoue"""
    print(f"\n📝 Test 3: Fallback téléchargement ({device_name})")

    page.set_default_timeout(TestConfig.TIMEOUT)
    page.goto(TestConfig.APP_URL, wait_until='domcontentloaded')

    # Bloquer window.open pour forcer le fallback
    page.evaluate("""
        window.open = function(url, target) {
            console.log('window.open bloqué (simulation popup blocker)');
            return null;  // Simuler un blocage
        };
    """)

    # Entrer des mots et rechercher les images avec retry
    words = ['soleil']
    page.locator('#words').fill('\n'.join(words))

    for attempt in range(TestConfig.MAX_RETRIES):
        try:
            page.locator('#btn-search').click()
            page.wait_for_selector('.word-section', timeout=TestConfig.IMAGE_SEARCH_TIMEOUT)
            time.sleep(3)
            break
        except Exception as e:
            if attempt < TestConfig.MAX_RETRIES - 1:
                print(f"      ⚠️  Tentative {attempt + 1} échouée, retry...")
                time.sleep(TestConfig.RETRY_DELAY)
                page.reload()

                # Re-bloquer window.open après reload
                page.evaluate("""
                    window.open = function(url, target) {
                        console.log('window.open bloqué (simulation popup blocker)');
                        return null;
                    };
                """)
                page.locator('#words').fill('\n'.join(words))
            else:
                print(f"      ⚠️  Impossible de charger les images après {TestConfig.MAX_RETRIES} tentatives")
                print(f"      Skip test (problème réseau probable)")
                return None

    # Écouter les téléchargements
    downloads = []
    page.on('download', lambda d: downloads.append(d))

    # Générer le PDF
    page.locator('#btn-generate').click()

    try:
        page.wait_for_function(
            "document.querySelector('#progress-text')?.textContent?.includes('succès')",
            timeout=TestConfig.TIMEOUT
        )
        time.sleep(2)
    except:
        pass

    print(f"   Téléchargements déclenchés: {len(downloads)}")

    # Note: ce test peut échouer si le fallback n'est pas implémenté
    # C'est exactement ce qu'on veut détecter!

    page.screenshot(path=f"{TestConfig.SCREENSHOTS_DIR}/03-fallback-{device_name.replace(' ', '-')}.png")

    if len(downloads) > 0:
        print(f"   ✅ Fallback téléchargement fonctionne")
        return True
    else:
        print(f"   ⚠️  Fallback téléchargement non implémenté (PROBLÈME DÉTECTÉ)")
        return False

def run_all_tests():
    """Exécute tous les tests PDF"""
    print("="*60)
    print("📄 Suite de Tests Playwright - Génération PDF")
    print("="*60)

    setup_test_env()

    tests = [
        ("Workflow complet", test_pdf_generation_workflow),
        ("Création blob", test_pdf_blob_creation),
        ("Fallback téléchargement", test_pdf_download_fallback),
    ]

    all_results = []

    with sync_playwright() as p:
        print("\n🌐 Lancement du navigateur Firefox...")
        browser = p.firefox.launch(headless=False)

        # Tester sur chaque appareil
        for device_name, device_config in TestConfig.DEVICES.items():
            print(f"\n{'='*60}")
            print(f"📱 Tests sur {device_name}")
            print(f"{'='*60}")

            context = browser.new_context(**device_config)

            for test_name, test_func in tests:
                page = context.new_page()
                full_test_name = f"{test_name} ({device_name})"
                print(f"\n{'─'*60}")

                try:
                    result = test_func(page, device_name)

                    if result is True:
                        all_results.append((full_test_name, "PASS", None))
                    elif result is False:
                        all_results.append((full_test_name, "FAIL", "Test échoué"))
                    else:
                        all_results.append((full_test_name, "SKIP", "Conditions non remplies"))

                except AssertionError as e:
                    all_results.append((full_test_name, "FAIL", str(e)))
                    print(f"   ❌ ÉCHEC: {e}")
                    page.screenshot(path=f"{TestConfig.SCREENSHOTS_DIR}/error-{device_name.replace(' ', '-')}-{test_name.replace(' ', '-')}.png")

                except Exception as e:
                    all_results.append((full_test_name, "ERROR", str(e)))
                    print(f"   ❌ ERREUR: {e}")

                finally:
                    page.close()
                    time.sleep(1)

            context.close()

        browser.close()

    # Résumé
    print("\n" + "="*60)
    print("📊 RÉSUMÉ DES TESTS PDF")
    print("="*60)

    passed = sum(1 for _, status, _ in all_results if status == "PASS")
    failed = sum(1 for _, status, _ in all_results if status == "FAIL")
    skipped = sum(1 for _, status, _ in all_results if status == "SKIP")
    errors = sum(1 for _, status, _ in all_results if status == "ERROR")

    for test_name, status, message in all_results:
        icon = {
            "PASS": "✅",
            "FAIL": "❌",
            "SKIP": "⚠️ ",
            "ERROR": "💥"
        }[status]

        msg = f" - {message[:50]}" if message else ""
        print(f"{icon} {status:6} {test_name:50} {msg}")

    print("\n" + "="*60)
    print(f"Total: {len(all_results)} tests")
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
    else:
        print("\n🎉 Tous les tests PDF sont passés!")
        exit(0)

if __name__ == "__main__":
    if not os.path.exists('web/index.html'):
        print("❌ Erreur: Exécutez ce script depuis le dossier racine du projet")
        print("   cd /Volumes/sidecar/src/fiches-mots")
        exit(1)

    run_all_tests()
