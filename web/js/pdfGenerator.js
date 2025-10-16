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

            // Charger les fichiers TTF en base64
            this.fonts.capital = await this.loadFontFile('../fonts/capital.ttf');
            this.fonts.script = await this.loadFontFile('../fonts/script.ttf');
            this.fonts.cursive = await this.loadFontFile('../fonts/cursive.ttf');

            console.log('✅ Polices chargées avec succès');

        } catch (error) {
            console.error('❌ Erreur chargement des polices:', error);
            throw new Error('Impossible de charger les polices');
        }
    }

    /**
     * Charge un fichier de police et le convertit en base64
     * @param {string} url - URL du fichier TTF
     * @returns {Promise<string>} - Police en base64
     */
    async loadFontFile(url) {
        const response = await fetch(url);
        const blob = await response.blob();

        return new Promise((resolve, reject) => {
            const reader = new FileReader();
            reader.onloadend = () => {
                // Extraire seulement la partie base64
                const base64 = reader.result.split(',')[1];
                resolve(base64);
            };
            reader.onerror = reject;
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
            // Créer le document PDF
            const { jsPDF } = window.jspdf;
            this.doc = new jsPDF({
                orientation: 'portrait',
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

            // Générer les pages (2 mots par page)
            let pageCreated = false;
            for (let i = 0; i < words.length; i += 2) {
                if (pageCreated) {
                    this.doc.addPage();
                }

                progressCallback((i / words.length) * 100);

                // Dessiner les 2 mots de la page
                const pageWords = words.slice(i, i + 2);

                for (let j = 0; j < pageWords.length; j++) {
                    await this.drawWordFiche(pageWords[j].word, pageWords[j].imageUrl, j);
                }

                pageCreated = true;
            }

            progressCallback(100);

            // Ouvrir le PDF dans un nouvel onglet au lieu de le télécharger
            const filename = theme ? `fiches_${theme}.pdf` : 'fiches_maternelle.pdf';

            // Générer le blob PDF
            const pdfBlob = this.doc.output('blob');
            const pdfUrl = URL.createObjectURL(pdfBlob);

            // Ouvrir dans un nouvel onglet
            window.open(pdfUrl, '_blank');

            console.log('✅ PDF généré et ouvert dans un nouvel onglet:', filename);

            // Libérer l'URL après un court délai
            setTimeout(() => URL.revokeObjectURL(pdfUrl), 1000);

        } catch (error) {
            console.error('❌ Erreur génération PDF:', error);
            throw error;
        }
    }

    /**
     * Dessine une fiche pour un mot sur la page
     * @param {string} word - Le mot à afficher
     * @param {string} imageUrl - URL de l'image
     * @param {number} position - Position sur la page (0 = haut, 1 = bas)
     */
    async drawWordFiche(word, imageUrl, position) {
        const cfg = CONFIG.pdf;
        const pageHeight = cfg.pageHeight;
        const margin = cfg.margin;
        const wordHeight = (pageHeight - 2 * margin) / 2;

        // Position Y de départ pour cette fiche
        let currentY = margin + (position * wordHeight);
        const xCenter = cfg.pageWidth / 2;

        // 1. Image (si disponible)
        if (imageUrl && imageUrl !== 'none') {
            try {
                // Télécharger l'image en Data URL
                const dataUrl = await imageSearcher.downloadImageAsDataURL(imageUrl);

                // Créer une image temporaire pour obtenir les dimensions
                const img = await this.loadImage(dataUrl);
                const imgWidth = img.width;
                const imgHeight = img.height;

                // Calculer les dimensions de l'image en respectant les proportions
                const aspect = imgWidth / imgHeight;
                let width, height;

                if (aspect > cfg.imageMaxWidth / cfg.imageMaxHeight) {
                    width = cfg.imageMaxWidth;
                    height = width / aspect;
                } else {
                    height = cfg.imageMaxHeight;
                    width = height * aspect;
                }

                const imgX = xCenter - width / 2;
                const imgY = currentY;

                // Bordure noire autour de l'image (2pt)
                this.doc.setDrawColor(0, 0, 0);
                this.doc.setLineWidth(2);
                this.doc.rect(imgX - 5.67, imgY - 5.67, width + 11.34, height + 11.34);

                // Dessiner l'image
                this.doc.addImage(dataUrl, 'JPEG', imgX, imgY, width, height);

                currentY = imgY + height + cfg.spacing;

            } catch (error) {
                console.error(`Erreur chargement image pour "${word}":`, error);
                // Continuer sans l'image
                currentY += cfg.spacing;
            }
        } else {
            currentY += cfg.spacing;
        }

        // 2. Mot en CAPITALES (OpenDyslexic Bold, 32pt)
        this.doc.setFont('OpenDyslexic-Bold', 'normal');
        this.doc.setFontSize(cfg.fontSize.capital);
        this.doc.setTextColor(0, 0, 0);
        this.doc.text(word.toUpperCase(), xCenter, currentY, { align: 'center' });
        currentY += 40;

        // 3. Mot en script (OpenDyslexic, 36pt)
        this.doc.setFont('OpenDyslexic', 'normal');
        this.doc.setFontSize(cfg.fontSize.script);
        this.doc.text(word.toLowerCase(), xCenter, currentY, { align: 'center' });
        currentY += 48;

        // 4. Mot en cursif (Écolier, 64pt - TRÈS GRAND)
        this.doc.setFont('Ecolier', 'normal');
        this.doc.setFontSize(cfg.fontSize.cursive);
        this.doc.text(word.toLowerCase(), xCenter, currentY, { align: 'center' });
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
}

// Instance globale
const pdfGenerator = new PDFGenerator();
