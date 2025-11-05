/**
 * Module de génération de PDF
 * Utilise jsPDF pour créer les fiches pédagogiques
 */

class PDFGenerator {
    constructor() {
        this.doc = null;
        this.fonts = {
            capital: null,
            script: null,
            cursive: null
        };
    }

    /**
     * Charge les polices TTF depuis les fichiers
     * @returns {Promise<void>}
     */
    async loadFonts() {
        try {
            console.log('📦 Chargement des polices...');

            // Charger les fichiers TTF en base64 (chemins absolus depuis racine)
            const [capital, script, cursive] = await Promise.all([
                this.loadFontFile('/fonts/capital.ttf'),
                this.loadFontFile('/fonts/script.ttf'),
                this.loadFontFile('/fonts/cursive.ttf')
            ]);

            // Vérifier que les polices sont bien chargées
            if (!capital || !script || !cursive) {
                throw new Error('Une ou plusieurs polices sont vides');
            }

            this.fonts.capital = capital;
            this.fonts.script = script;
            this.fonts.cursive = cursive;

            console.log('✅ Polices chargées avec succès');
            console.log(`   - Capital: ${capital.length} bytes`);
            console.log(`   - Script: ${script.length} bytes`);
            console.log(`   - Cursive: ${cursive.length} bytes`);

        } catch (error) {
            console.error('❌ Erreur chargement des polices:', error);
            throw new Error(`Impossible de charger les polices: ${error.message}`);
        }
    }

    /**
     * Charge un fichier de police et le convertit en base64
     * @param {string} url - URL du fichier TTF
     * @returns {Promise<string>} - Police en base64
     */
    async loadFontFile(url) {
        console.log(`   Chargement: ${url}`);

        const response = await fetch(url);

        if (!response.ok) {
            throw new Error(`Échec chargement ${url}: ${response.status} ${response.statusText}`);
        }

        const blob = await response.blob();

        if (blob.size === 0) {
            throw new Error(`Fichier vide: ${url}`);
        }

        console.log(`   → Taille: ${blob.size} bytes`);

        return new Promise((resolve, reject) => {
            const reader = new FileReader();
            reader.onloadend = () => {
                // Extraire seulement la partie base64
                const base64 = reader.result.split(',')[1];

                if (!base64 || base64.length === 0) {
                    reject(new Error(`Base64 vide pour ${url}`));
                    return;
                }

                console.log(`   → Base64: ${base64.length} caractères`);
                resolve(base64);
            };
            reader.onerror = () => reject(new Error(`Erreur lecture ${url}`));
            reader.readAsDataURL(blob);
        });
    }

    /**
     * Génère le PDF avec les mots et images sélectionnés
     * @param {Array} words - Liste de mots avec leurs images
     * @param {string} theme - Thème du PDF
     * @param {Function} progressCallback - Callback pour la progression
     * @returns {Promise<void>}
     */
    async generatePDF(words, theme, progressCallback) {
        try {
            // Créer le document PDF en PORTRAIT (4 fiches A6 par page)
            const { jsPDF } = window.jspdf;
            this.doc = new jsPDF({
                orientation: 'portrait',  // Format portrait pour 4 fiches A6
                unit: 'pt',
                format: 'a4'
            });

            // Charger les polices si nécessaire
            if (!this.fonts.capital) {
                await this.loadFonts();
            }

            // Ajouter les polices personnalisées au document
            this.doc.addFileToVFS('OpenDyslexic-Bold.ttf', this.fonts.capital);
            this.doc.addFont('OpenDyslexic-Bold.ttf', 'OpenDyslexic-Bold', 'normal');

            this.doc.addFileToVFS('OpenDyslexic.ttf', this.fonts.script);
            this.doc.addFont('OpenDyslexic.ttf', 'OpenDyslexic', 'normal');

            this.doc.addFileToVFS('Ecolier.ttf', this.fonts.cursive);
            this.doc.addFont('Ecolier.ttf', 'Ecolier', 'normal');

            // Métadonnées du PDF
            this.doc.setProperties({
                title: 'Fiches Pédagogiques - Maternelle',
                subject: `Fiches éducatives - Thème: ${theme || 'général'}`,
                author: 'Générateur Fiches-Mots',
                keywords: 'éducation, maternelle, dyslexie, accessibilité',
                creator: 'FichesMots Web App'
            });

            // Générer les pages (4 mots par page A4 = 4 fiches A6)
            let pageCreated = false;
            for (let i = 0; i < words.length; i += 4) {
                if (pageCreated) {
                    this.doc.addPage();
                }

                progressCallback((i / words.length) * 100);

                // Dessiner les 4 mots de la page (4 fiches A6)
                const pageWords = words.slice(i, i + 4);

                for (let j = 0; j < pageWords.length; j++) {
                    await this.drawWordFiche(pageWords[j].word, pageWords[j].imageUrl, j);
                }

                // Dessiner les pointillés de séparation en croix (plus légers)
                const pageWidth = this.doc.internal.pageSize.getWidth();
                const pageHeight = this.doc.internal.pageSize.getHeight();
                const a6Width = pageWidth / 2;
                const a6Height = pageHeight / 2;

                this.doc.setDrawColor(200, 200, 200); // Gris très clair
                this.doc.setLineWidth(0.5); // Plus fin
                this.doc.setLineDash([2, 4]); // Pointillés plus espacés: 2pt trait, 4pt espace

                // Ligne verticale centrale
                this.doc.line(a6Width, 0, a6Width, pageHeight);

                // Ligne horizontale centrale
                this.doc.line(0, a6Height, pageWidth, a6Height);

                this.doc.setLineDash([]); // Réinitialiser le style de ligne

                pageCreated = true;
            }

            progressCallback(100);

            // Générer le PDF
            const filename = theme ? `fiches_${theme}.pdf` : 'fiches_maternelle.pdf';
            const pdfBlob = this.doc.output('blob');
            const pdfUrl = URL.createObjectURL(pdfBlob);

            // Stratégie multi-plateforme pour afficher/télécharger le PDF
            // 1. Essayer d'ouvrir dans un nouvel onglet (desktop)
            // 2. Si bloqué, déclencher un téléchargement (mobile, popup blockers)

            const isMobile = /iPhone|iPad|iPod|Android/i.test(navigator.userAgent);

            if (isMobile) {
                // Sur mobile: Téléchargement direct (plus fiable que window.open)
                console.log('📱 Mobile détecté - Téléchargement du PDF...');
                this.downloadPDF(pdfBlob, filename);
                console.log('✅ PDF téléchargé:', filename);
            } else {
                // Sur desktop: Essayer d'ouvrir dans un nouvel onglet
                console.log('🖥️  Desktop - Ouverture du PDF dans un nouvel onglet...');
                const newWindow = window.open(pdfUrl, '_blank');

                if (!newWindow || newWindow.closed || typeof newWindow.closed === 'undefined') {
                    // Popup bloqué - fallback vers téléchargement
                    console.log('⚠️  Popup bloqué - Fallback vers téléchargement');
                    this.downloadPDF(pdfBlob, filename);
                    console.log('✅ PDF téléchargé:', filename);
                } else {
                    console.log('✅ PDF ouvert dans un nouvel onglet:', filename);
                }
            }

            // Libérer l'URL après 10 secondes (plus sûr pour les connexions lentes)
            setTimeout(() => URL.revokeObjectURL(pdfUrl), 10000);

        } catch (error) {
            console.error('❌ Erreur génération PDF:', error);
            throw error;
        }
    }

    /**
     * Dessine une fiche A6 avec cadre noir pour un mot
     * Layout: moitié haute = image dans boîte, moitié basse = 3 mots dans boîte
     * @param {string} word - Le mot à afficher
     * @param {string} imageUrl - URL de l'image
     * @param {number} position - Position sur la page (0-3: haut-gauche, haut-droite, bas-gauche, bas-droite)
     */
    async drawWordFiche(word, imageUrl, position) {
        const pageWidth = this.doc.internal.pageSize.getWidth();
        const pageHeight = this.doc.internal.pageSize.getHeight();

        // Dimensions A6 = A4 / 4
        const a6Width = pageWidth / 2;
        const a6Height = pageHeight / 2;

        // Positions des 4 fiches A6 sur la page A4
        const positions = [
            { x: 0, y: a6Height },           // Haut gauche
            { x: a6Width, y: a6Height },     // Haut droite
            { x: 0, y: 0 },                   // Bas gauche
            { x: a6Width, y: 0 }              // Bas droite
        ];

        const pos = positions[position];
        const xPosition = pos.x;
        const yPosition = pos.y;

        // Cadre noir autour de la fiche A6
        this.doc.setDrawColor(0, 0, 0);
        this.doc.setLineWidth(2);
        this.doc.rect(xPosition, yPosition, a6Width, a6Height);

        // Marges intérieures réduites pour les boîtes (0.5cm = 14.17pt)
        const innerMargin = 14.17;

        // Centre horizontal de la fiche
        const xCenter = xPosition + a6Width / 2;

        // Image en HAUT, texte en BAS
        // En jsPDF, Y=0 est en haut et augmente vers le bas
        // Pour un card qui commence à yPosition et s'étend sur a6Height:
        // - Top visuel = yPosition (bas Y) -> zone IMAGE
        // - Bottom visuel = yPosition + a6Height (haut Y) -> zone TEXTE

        const imageBoxHeight = (a6Height - innerMargin) / 2;
        const imageBoxY = yPosition + innerMargin / 2;  // EN HAUT (bas Y)
        const imageBoxWidth = a6Width - 2 * innerMargin;

        const textBoxHeight = (a6Height - innerMargin) / 2;
        const textBoxY = yPosition + a6Height - textBoxHeight - innerMargin / 2;  // EN BAS (haut Y)
        const textBoxWidth = a6Width - 2 * innerMargin;

        // === ZONE IMAGE (moitié haute) ===
        // Boîte pour l'image
        this.doc.setDrawColor(0, 0, 0);
        this.doc.setLineWidth(2);
        this.doc.rect(xPosition + innerMargin, imageBoxY, imageBoxWidth, imageBoxHeight);

        if (imageUrl && imageUrl !== 'none') {
            try {
                // Télécharger l'image en Data URL
                const dataUrl = await imageSearcher.downloadImageAsDataURL(imageUrl);

                // Créer une image temporaire pour obtenir les dimensions
                const img = await this.loadImage(dataUrl);
                const imgWidth = img.width;
                const imgHeight = img.height;

                // Dimensions maximales pour la zone image (avec marges internes)
                const maxImgWidth = imageBoxWidth - 2 * 14.17; // 14.17pt = 0.5cm
                const maxImgHeight = imageBoxHeight - 2 * 14.17;

                // Calculer les proportions
                const aspect = imgWidth / imgHeight;
                let width, height;

                if (aspect > maxImgWidth / maxImgHeight) {
                    width = maxImgWidth;
                    height = width / aspect;
                } else {
                    height = maxImgHeight;
                    width = height * aspect;
                }

                // Centrer l'image dans la zone
                const imgX = xCenter - width / 2;
                const imgY = imageBoxY + (imageBoxHeight - height) / 2;

                // Dessiner l'image
                this.doc.addImage(dataUrl, 'JPEG', imgX, imgY, width, height);

            } catch (error) {
                console.error(`Erreur chargement image pour "${word}":`, error);
            }
        }

        // === ZONE TEXTE (moitié basse) ===
        // Boîte pour les textes
        this.doc.setDrawColor(0, 0, 0);
        this.doc.setLineWidth(2);
        this.doc.rect(xPosition + innerMargin, textBoxY, textBoxWidth, textBoxHeight);

        // Rapprocher les textes du centre pour éviter le débordement du cursif
        // Zone de texte plus concentrée au centre (70% de la hauteur disponible)
        const textZoneHeight = textBoxHeight * 0.7;
        const textZoneOffset = (textBoxHeight - textZoneHeight) / 2;
        const textLineHeight = textZoneHeight / 3;

        // Fonction pour ajuster la taille de police si le texte dépasse
        const adjustFontSize = (text, font, maxSize, maxWidth) => {
            let size = maxSize;
            this.doc.setFont(font, 'normal');
            this.doc.setFontSize(size);

            // Réduire la taille si le texte dépasse
            while (this.doc.getTextWidth(text) > maxWidth && size > 10) {
                size -= 2;
                this.doc.setFontSize(size);
            }

            return size;
        };

        const maxTextWidth = textBoxWidth - 20; // Marge de sécurité

        // 1. Mot en CAPITALES (tiers supérieur de la zone concentrée)
        const yCapital = textBoxY + textZoneOffset + 2 * textLineHeight + textLineHeight / 2 - 8;
        adjustFontSize(word.toUpperCase(), 'OpenDyslexic-Bold', 24, maxTextWidth);
        this.doc.setTextColor(0, 0, 0);
        this.doc.text(word.toUpperCase(), xCenter, yCapital, { align: 'center', maxWidth: maxTextWidth });

        // 2. Mot en script (tiers central de la zone concentrée)
        const yScript = textBoxY + textZoneOffset + textLineHeight + textLineHeight / 2 - 10;
        adjustFontSize(word.toLowerCase(), 'OpenDyslexic', 28, maxTextWidth);
        this.doc.setTextColor(0, 0, 0);
        this.doc.text(word.toLowerCase(), xCenter, yScript, { align: 'center', maxWidth: maxTextWidth });

        // 3. Mot en cursif (tiers inférieur de la zone concentrée)
        const yCursive = textBoxY + textZoneOffset + textLineHeight / 2 - 5;
        const cursiveWord = word.toLowerCase()
            .replace(/œ/g, 'oe')
            .replace(/Œ/g, 'oe');
        adjustFontSize(cursiveWord, 'Ecolier', 48, maxTextWidth);
        this.doc.setTextColor(0, 0, 0);
        this.doc.text(cursiveWord, xCenter, yCursive, { align: 'center', maxWidth: maxTextWidth });
    }

    /**
     * Charge une image et retourne ses dimensions
     * @param {string} src - URL ou Data URL de l'image
     * @returns {Promise<HTMLImageElement>}
     */
    loadImage(src) {
        return new Promise((resolve, reject) => {
            const img = new Image();
            img.crossOrigin = 'Anonymous';
            img.onload = () => resolve(img);
            img.onerror = reject;
            img.src = src;
        });
    }

    /**
     * Télécharge le PDF via un lien temporaire
     * Compatible avec tous les navigateurs (desktop et mobile)
     * @param {Blob} blob - Le blob PDF
     * @param {string} filename - Nom du fichier
     */
    downloadPDF(blob, filename) {
        const link = document.createElement('a');
        link.href = URL.createObjectURL(blob);
        link.download = filename;

        // Ajouter temporairement au DOM pour compatibilité iOS
        document.body.appendChild(link);

        // Déclencher le téléchargement
        link.click();

        // Nettoyer
        setTimeout(() => {
            document.body.removeChild(link);
            URL.revokeObjectURL(link.href);
        }, 100);
    }
}

// Instance globale
const pdfGenerator = new PDFGenerator();
