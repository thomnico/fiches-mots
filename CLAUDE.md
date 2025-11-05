# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

```xml
<?xml version="1.0" encoding="UTF-8"?>
<project>
  <metadata>
    <name>fiches-mots</name>
    <description>Générateur automatique de fiches pédagogiques PDF pour la maternelle française</description>
    <language>JavaScript</language>
    <version>2.0.0</version>
    <stack>Web App (HTML/CSS/JavaScript + Vercel Serverless)</stack>
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
      - Fonts are loaded via TTF files in /fonts/ directory
      - NEVER substitute with standard fonts without explicit permission
    </rule>
    <rule id="image_search">
      🎨 IMAGE SEARCH via Google Custom Search API
      - Uses serverless API endpoint /api/google-search
      - Returns child-appropriate, educational images
      - Fallback to "none" if no images found
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
    <rule id="pdf_layout">
      📄 PDF LAYOUT REQUIREMENTS
      - Format A6: 4 cards per A4 page (2×2 grid, portrait orientation)
      - Layout per card: Image at TOP, Text at BOTTOM
      - Text: 3 styles stacked (CAPITALS, script, cursive)
      - Black borders: A6 cards + image/text boxes
      - Light gray dotted cross separator
      - Reduced margins (14.17pt = 0.5cm)
      - Dynamic font sizing for long words
    </rule>
  </critical_rules>

  <overview>
    <purpose>
      Application web pour créer des fiches éducatives illustrées pour l'apprentissage des mots en maternelle.
      Chaque fiche contient : une image, le mot en CAPITALES, en script, et en cursif.
      Format : 4 fiches A6 par page A4 (2×2 grid).
    </purpose>
    <target_audience>Enseignants de maternelle française</target_audience>
  </overview>

  <architecture>
    <structure>
      <directory path="web/">
        <description>Application web frontend</description>
        <file path="index.html">Interface utilisateur principale</file>
        <file path="css/style.css">Styles responsive (mobile-first)</file>
        <directory path="js/">
          <file path="app.js">Orchestration de l'application</file>
          <file path="pdfGenerator.js">Génération PDF avec jsPDF</file>
          <file path="mistralAI.js">Génération de mots via API Mistral</file>
          <file path="imageSearch.serverless.js">Recherche d'images via API</file>
          <file path="config.js">Configuration et traductions</file>
        </directory>
      </directory>

      <directory path="api/">
        <description>Vercel Serverless Functions</description>
        <file path="google-search.js">Proxy API Google Custom Search</file>
        <file path="mistral.js">Proxy API Mistral AI</file>
      </directory>

      <directory path="fonts/">
        <description>Polices TrueType pour dyslexie</description>
        <file>capital.ttf - OpenDyslexic-Bold (CAPITALES)</file>
        <file>script.ttf - OpenDyslexic (script)</file>
        <file>cursive.ttf - Écolier (cursif français)</file>
      </directory>
    </structure>

    <key_concepts>
      <concept name="Serverless Architecture">
        <explanation>
          L'application utilise Vercel Serverless Functions pour les appels API.
          Les clés API sont stockées dans les variables d'environnement Vercel.
          Aucune clé API n'est exposée côté client.
        </explanation>
      </concept>

      <concept name="Layout PDF A6">
        <explanation>
          Format A4 (595.28 × 841.89 pts) avec 4 fiches A6 (2×2 grid, portrait).
          Chaque fiche A6 : Image en HAUT (yPosition + innerMargin/2), Texte en BAS (yPosition + a6Height - textBoxHeight - innerMargin/2).
          Système de coordonnées jsPDF : Y=0 en haut, augmente vers le bas.
        </explanation>
      </concept>

      <concept name="Polices Custom">
        <explanation>
          Les polices TTF sont chargées dynamiquement depuis /fonts/.
          Conversion en base64 via FileReader, puis ajout à jsPDF via addFileToVFS().
          Support des caractères français (é, è, ê, à, ç, œ).
        </explanation>
      </concept>

      <concept name="Génération IA">
        <explanation>
          Utilise Mistral AI via API serverless pour générer des listes de mots thématiques.
          Timeouts adaptés (45s), retry automatique (2 tentatives), gestion erreurs réseau.
          Exclusion automatique des mots déjà présents.
        </explanation>
      </concept>
    </key_concepts>
  </architecture>

  <commands>
    <development>
      <command>
        <name>start_dev_server</name>
        <usage>vercel dev --listen 3000</usage>
        <description>Démarre le serveur de développement Vercel avec support API serverless</description>
        <note priority="CRITICAL">OBLIGATOIRE pour tester l'API Mistral et la recherche d'images</note>
      </command>
    </development>

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
      </commands>
    </deployment>
  </commands>

  <workflow>
    <typical_usage>
      <step number="1">Ouvrir l'application web (localhost:3000 en dev)</step>
      <step number="2">Saisir un thème (optionnel) et des mots (un par ligne)</step>
      <step number="3">OU utiliser "Le Chat Magique" (Mistral AI) pour générer des mots</step>
      <step number="4">Cliquer sur "Rechercher les images"</step>
      <step number="5">Sélectionner une image pour chaque mot (3 propositions)</step>
      <step number="6">Cliquer sur "Générer le PDF"</step>
      <step number="7">Le PDF s'ouvre dans un nouvel onglet (desktop) ou se télécharge (mobile)</step>
    </typical_usage>

    <adding_words_via_ai>
      <instruction>Utiliser le bouton "🪄 Le Chat Magique"</instruction>
      <features>
        <feature>Génération de 5-20 mots sur un thème</feature>
        <feature>Exclusion automatique des mots déjà présents</feature>
        <feature>Retry automatique si erreur réseau</feature>
        <feature>Timeout adapté pour mobile (45s)</feature>
      </features>
    </adding_words_via_ai>
  </workflow>

  <troubleshooting>
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
    </issue>

    <issue type="pdf_layout_image_position" priority="FIXED">
      <symptom>✅ CORRIGÉ: Les images apparaissaient en dessous du texte au lieu d'être au-dessus</symptom>
      <root_cause>
        Calculs de coordonnées Y inversés dans jsPDF (Y=0 en haut, augmente vers le bas)
      </root_cause>
      <solution_implemented>
        <change file="web/js/pdfGenerator.js:257-262">
          - imageBoxY = yPosition + innerMargin / 2 (EN HAUT)
          - textBoxY = yPosition + a6Height - textBoxHeight - innerMargin / 2 (EN BAS)
        </change>
      </solution_implemented>
    </issue>

    <issue type="mistral_api_mobile" priority="MONITORED">
      <symptom>⚠️ L'appel à l'API Mistral peut être instable sur mobile avec connexion lente</symptom>
      <context>Peut nécessiter des timeouts plus longs et retry sur mobile</context>
      <solutions>
        <solution>✅ Timeouts augmentés (45s pour API Mistral)</solution>
        <solution>✅ Retry automatique (2 tentatives) implémenté dans mistralAI.js</solution>
        <solution>✅ Gestion d'erreurs réseau spécifique mobile</solution>
      </solutions>
    </issue>

    <issue type="api_serverless">
      <symptom>API ne fonctionne pas en développement</symptom>
      <solutions>
        <solution>✅ Utiliser 'vercel dev --listen 3000' au lieu de 'python -m http.server'</solution>
        <solution>Vérifier que les variables d'environnement sont configurées dans .env.local</solution>
        <solution>Redémarrer Vercel Dev si les variables changent</solution>
      </solutions>
    </issue>
  </troubleshooting>

  <technical_notes>
    <note type="image_search">
      <title>Recherche via Google Custom Search API</title>
      <details>
        Utilise l'API Google Custom Search via une fonction serverless.
        Filtre: images libres de droits, adaptées aux enfants.
        Fallback: "none" si aucune image trouvée.
      </details>
    </note>

    <note type="pdf_generation">
      <title>Génération PDF avec jsPDF</title>
      <details>
        Bibliothèque: jsPDF 2.5.1 (CDN)
        Format: A4 portrait (595.28 × 841.89 pts)
        Layout: 4 fiches A6 par page (2×2 grid)
        Polices: TTF custom chargées en base64
        Images: Converties en Data URLs via CORS proxy
      </details>
    </note>

    <note type="font_loading">
      <title>Chargement des polices TTF</title>
      <details>
        Les polices sont chargées via fetch() depuis /fonts/
        Conversion en base64 via FileReader
        Ajout à jsPDF via addFileToVFS() et addFont()
        Cache: les polices sont chargées une seule fois par session
      </details>
    </note>

    <note type="coordinate_system">
      <title>Système de coordonnées jsPDF</title>
      <details>
        Y=0 en HAUT de la page, augmente vers le BAS
        Donc pour placer du contenu en HAUT visuel: utiliser une PETITE valeur Y
        Pour placer du contenu en BAS visuel: utiliser une GRANDE valeur Y
      </details>
    </note>
  </technical_notes>

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
