# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

```xml
<?xml version="1.0" encoding="UTF-8"?>
<project>
  <metadata>
    <name>fiches-mots</name>
    <description>Générateur automatique de fiches pédagogiques PDF pour la maternelle française</description>
    <language>Python</language>
    <version>1.0.0</version>
  </metadata>

  <critical_rules priority="MAXIMUM">
    <rule id="no_simplification">
      ⚠️ NEVER PROPOSE SIMPLIFICATIONS OR WORKAROUNDS
      - Always implement the full requested solution, no matter the complexity
      - Never suggest "easier" alternatives without explicit user request
      - Take note of user's specific requirements and NEVER deviate
      - If a solution requires complex implementation (e.g., font conversion, API integration), DO IT
    </rule>
    <rule id="font_requirements">
      🔤 FONT REQUIREMENTS ARE STRICT
      - CAPITALS and Script MUST use dyslexic-friendly fonts (OpenDyslexic)
      - Cursive MUST use Écolier font (French school cursive)
      - If OTF fonts don't work with ReportLab, convert them using FontForge
      - NEVER substitute with standard fonts without explicit permission
    </rule>
    <rule id="image_search">
      🎨 IMAGE SEARCH PRIORITY
      - First priority: OpenClipart (naive vector drawings for children)
      - Second: Wikimedia Commons (with preference for illustrations/drawings)
      - Never skip image search steps
      - Always filter for child-appropriate, educational content
    </rule>
    <rule id="mobile_responsive">
      📱 RESPONSIVE DESIGN REQUIREMENT
      - Application MUST be fully responsive and work correctly on mobile devices
      - Desktop-first approach, but must adapt gracefully to mobile
      - Test on various screen sizes (phones, tablets, desktop)
      - Touch interactions must be optimized for mobile usage
      - UI elements must be properly sized for touch screens
      - All features must work seamlessly on mobile browsers
    </rule>
  </critical_rules>

  <overview>
    <purpose>
      Créer des fiches éducatives illustrées pour l'apprentissage des mots en maternelle.
      Chaque fiche contient : une image, le mot en CAPITALES, en script, et en cursif.
      Format : 2 mots par page A4.
    </purpose>
    <target_audience>Enseignants de maternelle française</target_audience>
  </overview>

  <architecture>
    <structure>
      <file path="generate_fiches.py" type="script">
        <description>Script principal autonome pour générer les PDFs</description>
        <classes>
          <class name="ImageSearcher">
            <responsibility>Recherche et téléchargement d'images depuis Wikimedia Commons</responsibility>
            <methods>
              <method name="search_wikimedia">Recherche une image pour un mot donné</method>
              <method name="download_image">Télécharge et convertit l'image en RGB</method>
            </methods>
          </class>
          <class name="FichePDFGenerator">
            <responsibility>Génération des fiches PDF avec ReportLab</responsibility>
            <methods>
              <method name="setup_fonts">Configure les polices (CAPITALES, script, cursif)</method>
              <method name="draw_word_fiche">Dessine une fiche pour un mot (image + 3 styles)</method>
              <method name="generate">Orchestre la génération complète du PDF</method>
            </methods>
          </class>
        </classes>
        <dependencies>
          <library>reportlab - Génération PDF</library>
          <library>requests - Téléchargement HTTP</library>
          <library>beautifulsoup4 - Parsing HTML pour recherche d'images</library>
          <library>Pillow - Traitement d'images</library>
        </dependencies>
      </file>

      <file path="mots_automne.txt" type="data">
        <description>Liste de mots exemple sur le thème de l'automne</description>
        <format>Un mot par ligne, encodage UTF-8</format>
      </file>

      <directory path="fonts/">
        <description>Polices TrueType optionnelles pour améliorer le rendu</description>
        <files>
          <file>cursive.ttf - Police manuscrite/cursive</file>
          <file>script.ttf - Police script/scripte</file>
        </files>
      </directory>

      <directory path="output/">
        <description>Dossier de sortie pour les PDFs générés</description>
      </directory>
    </structure>

    <key_concepts>
      <concept name="Recherche d'images sans API">
        <explanation>
          Utilise le scraping HTML de Wikimedia Commons pour éviter les tokens API.
          Méthode gratuite et sans authentification.
        </explanation>
      </concept>

      <concept name="Layout PDF">
        <explanation>
          Format A4 (21 x 29.7 cm) avec 2 mots par page.
          Chaque fiche : Image (8x6cm) + 3 lignes de texte (CAPITALES 28pt, script 24pt, cursif 22pt).
        </explanation>
      </concept>

      <concept name="Polices par défaut">
        <explanation>
          Sans polices personnalisées : Helvetica-Bold (capitales), Helvetica (script), Times-Italic (cursif).
          Amélioration possible en ajoutant des .ttf dans fonts/.
        </explanation>
      </concept>
    </key_concepts>
  </architecture>

  <commands>
    <installation>
      <command>
        <name>install_dependencies</name>
        <usage>pip install -r requirements.txt</usage>
        <description>Installe toutes les dépendances Python nécessaires</description>
      </command>
    </installation>

    <development>
      <command>
        <name>generate_default</name>
        <usage>python generate_fiches.py</usage>
        <description>Génère un PDF avec la liste par défaut (mots_automne.txt)</description>
        <output>output/fiches_maternelle.pdf</output>
      </command>

      <command>
        <name>generate_custom_words</name>
        <usage>python generate_fiches.py [fichier_mots.txt]</usage>
        <description>Génère un PDF avec une liste de mots personnalisée</description>
        <example>python generate_fiches.py mots_animaux.txt</example>
      </command>

      <command>
        <name>generate_custom_output</name>
        <usage>python generate_fiches.py [fichier_mots.txt] [sortie.pdf]</usage>
        <description>Génère un PDF avec entrée et sortie personnalisées</description>
        <example>python generate_fiches.py mots_animaux.txt output/animaux.pdf</example>
      </command>
    </development>

    <testing>
      <browser>Firefox (Playwright)</browser>
      <note>Tous les tests Playwright utilisent Firefox (déjà installé)</note>
      <command>
        <name>run_playwright_tests</name>
        <usage>python tests/test_mistral_api.py</usage>
        <description>Lance les tests Playwright pour l'intégration Mistral AI</description>
        <coverage>8 tests: API directe, UI, génération, workflow, erreurs, modèle</coverage>
      </command>
      <command>
        <name>run_mobile_tests</name>
        <usage>python tests/test_mobile.py</usage>
        <description>Lance les tests Playwright pour la compatibilité mobile</description>
        <coverage>Tests de réactivité, interactions tactiles, API Mistral sur mobile</coverage>
      </command>
      <command>
        <name>run_pdf_tests</name>
        <usage>python tests/test_pdf_generation.py</usage>
        <description>Lance les tests Playwright pour la génération PDF (desktop et mobile)</description>
        <coverage>3 tests × 3 plateformes (Desktop, iPhone 12, Pixel 5): workflow complet, création blob, fallback téléchargement</coverage>
        <features>
          <feature>Timeouts adaptés pour réseau lent (60-90s)</feature>
          <feature>Retry automatique (3 tentatives avec délai 2s)</feature>
          <feature>Skip intelligent si problème réseau persistant</feature>
          <feature>Screenshots de debug automatiques</feature>
        </features>
      </command>
    </testing>

    <deployment>
      <platform>Vercel</platform>
      <workflow>
        <step number="1">Commit et push les changements vers GitHub</step>
        <step number="2">Vercel détecte automatiquement les changements sur main</step>
        <step number="3">Déploiement automatique en production</step>
        <step number="4">TOUJOURS nettoyer les anciens déploiements (> 1h)</step>
      </workflow>
      <note priority="HIGH">
        ⚠️ PAS BESOIN de 'vercel --prod' - Vercel prend le code directement depuis GitHub!
        Le déploiement est automatique dès le push sur la branche main.
      </note>
      <note priority="CRITICAL">
        🧹 NETTOYAGE AUTOMATIQUE REQUIS
        - Après chaque déploiement, TOUJOURS supprimer les déploiements de plus d'1 heure
        - Garder UNIQUEMENT le déploiement le plus récent
        - Utiliser 'vercel ls' pour lister puis 'vercel rm' pour chaque ancien déploiement
        - Cela évite l'accumulation de déploiements inutiles
      </note>
      <commands>
        <command>
          <name>push_to_deploy</name>
          <usage>git add . &amp;&amp; git commit -m "message" &amp;&amp; git push</usage>
          <description>Push vers GitHub déclenche le déploiement Vercel automatique</description>
        </command>
        <command>
          <name>list_deployments</name>
          <usage>vercel ls</usage>
          <description>Liste tous les déploiements Vercel</description>
        </command>
        <command>
          <name>remove_old_deployments</name>
          <usage>vercel ls | grep -E "[0-9]+h|[0-9]+d" | awk '{print $2}' | xargs -I {} vercel rm {} --yes</usage>
          <description>Supprime automatiquement tous les déploiements de plus d'1 heure</description>
          <note>Cette commande doit être exécutée après chaque push réussi</note>
        </command>
        <command>
          <name>remove_deployment</name>
          <usage>vercel rm [deployment-url] --yes</usage>
          <description>Supprime un déploiement spécifique</description>
        </command>
        <command>
          <name>complete_deploy_workflow</name>
          <usage>git push &amp;&amp; sleep 10 &amp;&amp; vercel ls | tail -n +3 | head -n -1 | tail -n +2 | awk '{print $2}' | xargs -I {} vercel rm {} --yes</usage>
          <description>Workflow complet: push + attendre + nettoyer anciens déploiements</description>
          <note>Garde uniquement le déploiement le plus récent</note>
        </command>
      </commands>
    </deployment>
  </commands>

  <workflow>
    <typical_usage>
      <step number="1">Créer un fichier texte avec des mots (un par ligne)</step>
      <step number="2">Exécuter : python generate_fiches.py mon_fichier.txt</step>
      <step number="3">Le script recherche automatiquement les images sur Wikimedia</step>
      <step number="4">Génération du PDF dans output/ avec 2 mots par page</step>
      <step number="5">Vérifier le PDF généré</step>
    </typical_usage>

    <adding_words>
      <instruction>Éditer le fichier .txt ou créer un nouveau fichier</instruction>
      <format>Un mot par ligne, encodage UTF-8, sans caractères spéciaux</format>
      <themes_examples>
        <theme name="automne">feuille, champignon, citrouille, marron</theme>
        <theme name="animaux">chat, chien, oiseau, poisson</theme>
        <theme name="couleurs">rouge, bleu, jaune, vert</theme>
      </themes_examples>
    </adding_words>

    <adding_fonts>
      <instruction>Télécharger des polices .ttf libres et les placer dans fonts/</instruction>
      <required_files>
        <file>fonts/cursive.ttf - Pour le style cursif/manuscrit</file>
        <file>fonts/script.ttf - Pour le style script</file>
      </required_files>
      <recommendations>
        <font type="cursive">Écolier, Cursive Standard</font>
        <font type="script">Sassoon, OpenDyslexic, Andika</font>
      </recommendations>
    </adding_fonts>
  </workflow>

  <troubleshooting>
    <issue type="no_image_found">
      <symptom>Message "Aucune image trouvée pour '[mot]'"</symptom>
      <solutions>
        <solution>Vérifier l'orthographe du mot</solution>
        <solution>Essayer un synonyme plus courant</solution>
        <solution>Rechercher manuellement sur commons.wikimedia.org</solution>
        <solution>Le script continue sans image si non trouvée</solution>
      </solutions>
    </issue>

    <issue type="connection_error">
      <symptom>Erreur de téléchargement d'image</symptom>
      <solutions>
        <solution>Vérifier la connexion internet</solution>
        <solution>Réessayer (Wikimedia peut être temporairement indisponible)</solution>
      </solutions>
    </issue>

    <issue type="font_rendering">
      <symptom>Polices par défaut peu adaptées</symptom>
      <solutions>
        <solution>Installer des polices .ttf personnalisées dans fonts/</solution>
        <solution>Nommer les fichiers : cursive.ttf et script.ttf</solution>
      </solutions>
    </issue>

    <issue type="pdf_generation_mobile" priority="FIXED">
      <symptom>✅ CORRIGÉ: Le PDF ne s'affichait pas dans le browser et ne se créait pas sur mobile</symptom>
      <root_cause>
        - window.open() bloqué par les popup blockers sur mobile
        - URL.revokeObjectURL() appelé trop rapidement (1s)
        - Absence de fallback si popup bloqué
      </root_cause>
      <solution_implemented>
        <change file="web/js/pdfGenerator.js">
          - Détection mobile: téléchargement direct sur mobile (plus fiable)
          - Détection desktop: window.open() avec fallback vers téléchargement si bloqué
          - Nouvelle méthode downloadPDF() compatible iOS/Android
          - Timeout URL.revokeObjectURL() prolongé à 10s pour connexions lentes
        </change>
      </solution_implemented>
      <testing>
        <test>tests/test_pdf_generation.py - 9 tests (3 tests × 3 plateformes)</test>
        <test>Vérification création blob, ouverture popup, fallback téléchargement</test>
        <test>Timeouts adaptés pour réseau lent avec retry automatique</test>
      </testing>
    </issue>

    <issue type="mistral_api_mobile" priority="MONITORED">
      <symptom>⚠️ L'appel à l'API Mistral peut être instable sur mobile avec connexion lente</symptom>
      <context>Peut nécessiter des timeouts plus longs et retry sur mobile</context>
      <solutions>
        <solution>✅ Timeouts augmentés (45s pour API Mistral)</solution>
        <solution>✅ Retry automatique (2 tentatives) implémenté dans mistralAI.js</solution>
        <solution>✅ Gestion d'erreurs réseau spécifique mobile</solution>
        <solution>Vérifier les CORS et les restrictions réseau mobile</solution>
      </solutions>
      <testing>
        <test>Utiliser tests/test_mobile.py pour reproduire et debugger le problème</test>
        <test>Tester avec émulation mobile dans les DevTools navigateur</test>
        <test>Tester sur de vrais appareils physiques (iOS et Android)</test>
      </testing>
    </issue>

    <issue type="network_timeout" priority="HANDLED">
      <symptom>Timeouts lors de la recherche d'images avec connexion lente</symptom>
      <solutions>
        <solution>✅ Tous les tests implémentent retry automatique (3 tentatives)</solution>
        <solution>✅ Timeouts adaptés: 60s opérations PDF, 90s recherche images</solution>
        <solution>✅ Skip intelligent si problème réseau persistant (ne fait pas échouer la suite)</solution>
        <solution>✅ Messages informatifs pour diagnostiquer les problèmes réseau</solution>
      </solutions>
    </issue>
  </troubleshooting>

  <technical_notes>
    <note type="image_search">
      <title>Méthode de recherche gratuite</title>
      <details>
        Scraping HTML de Wikimedia Commons via BeautifulSoup.
        Pas d'API token requis, mais délai de 1s entre requêtes pour respecter les serveurs.
      </details>
    </note>

    <note type="image_processing">
      <title>Conversion d'images</title>
      <details>
        Toutes les images sont converties en RGB pour compatibilité PDF.
        Support de RGBA, LA, P avec fond blanc si nécessaire.
        Ratio d'aspect préservé lors de l'insertion.
      </details>
    </note>

    <note type="pdf_layout">
      <title>Dimensions des éléments</title>
      <details>
        Page A4 : 21 x 29.7 cm
        Marges : 2 cm
        Image : 8 x 6 cm (ajustée selon ratio)
        Ligne de séparation entre les 2 mots : trait gris (0.8, 0.8, 0.8)
      </details>
    </note>
  </technical_notes>

  <extensions_ideas>
    <idea>Ajouter support pour thèmes prédéfinis (animaux, couleurs, etc.)</idea>
    <idea>Interface graphique simple (Tkinter) pour sélection de mots</idea>
    <idea>Export en plusieurs formats (PNG par fiche, etc.)</idea>
    <idea>Personnalisation des couleurs et mise en page</idea>
    <idea>Cache local des images téléchargées</idea>
    <idea>Support pour phrases courtes (pas seulement mots isolés)</idea>
  </extensions_ideas>

  <educational_context>
    <target_age>3-6 ans (maternelle française : PS, MS, GS)</target_age>
    <pedagogical_objective>
      Apprentissage de la reconnaissance et de l'écriture des mots.
      Association mot-image pour faciliter la mémorisation.
      Familiarisation avec les trois styles d'écriture utilisés en France.
    </pedagogical_objective>
  </educational_context>
</project>
```
