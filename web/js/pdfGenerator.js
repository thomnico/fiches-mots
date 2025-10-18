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
            // Créer le document PDF
            const { jsPDF } = window.jspdf;
            this.doc = new jsPDF({
                orientation: 'landscape',  // Format paysage pour plus d'espace
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

                // Ligne de séparation verticale entre les 2 fiches (si 2 fiches sur la page)
                if (pageWords.length === 2) {
                    const cfg = CONFIG.pdf;
                    const pageWidth = this.doc.internal.pageSize.getWidth();
                    const pageHeight = this.doc.internal.pageSize.getHeight();
                    const margin = cfg.margin;

                    this.doc.setDrawColor(200, 200, 200); // Gris clair
                    this.doc.setLineWidth(1);
                    this.doc.setLineDash([5, 3]); // Ligne pointillée
                    this.doc.line(
                        pageWidth / 2,
                        margin,
                        pageWidth / 2,
                        pageHeight - margin
                    );
                    this.doc.setLineDash([]); // Réinitialiser le style de ligne
                }

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
     * Dessine une fiche pour un mot sur la page
     * EN PAYSAGE: Layout côte à côte (2 colonnes)
     * @param {string} word - Le mot à afficher
     * @param {string} imageUrl - URL de l'image
     * @param {number} position - Position sur la page (0 = gauche, 1 = droite)
     */
    async drawWordFiche(word, imageUrl, position) {
        const cfg = CONFIG.pdf;
        const margin = cfg.margin;

        // EN PAYSAGE: 2 fiches côte à côte (position 0 = gauche, 1 = droite)
        const pageWidth = this.doc.internal.pageSize.getWidth();

        // Largeur disponible pour chaque fiche (moitié de la page)
        const ficheWidth = (pageWidth - 3 * margin) / 2; // 3 marges: gauche, milieu, droite

        // Position X de la fiche (gauche ou droite)
        const ficheX = position === 0
            ? margin  // Fiche gauche
            : margin * 2 + ficheWidth; // Fiche droite

        // Centre horizontal de la fiche
        const xCenter = ficheX + ficheWidth / 2;

        // Position Y initiale (haut de la page)
        const topMargin = margin;

        // ZONE IMAGE: hauteur fixe réservée pour l'image
        const imageZoneHeight = cfg.imageMaxHeight * 1.69; // Zone réservée pour l'image (hauteur max)

        // POSITIONS FIXES pour les mots (toujours à la même hauteur)
        const textStartY = topMargin + imageZoneHeight + cfg.spacing;
        const capitalY = textStartY;
        const scriptY = capitalY + 40;
        const cursiveY = scriptY + 70;

        // 1. Image (si disponible) - centrée dans la zone réservée
        if (imageUrl && imageUrl !== 'none') {
            try {
                // Télécharger l'image en Data URL
                const dataUrl = await imageSearcher.downloadImageAsDataURL(imageUrl);

                // Créer une image temporaire pour obtenir les dimensions
                const img = await this.loadImage(dataUrl);
                const imgWidth = img.width;
                const imgHeight = img.height;

                // Calculer les dimensions de l'image en respectant les proportions
                // En paysage côte à côte, adapter la largeur max à la largeur de la fiche
                const maxImageWidth = ficheWidth * 1.35; // 135% de la largeur de la fiche (+30% supplémentaires = +69% vs original 80%)
                const maxImageHeight = cfg.imageMaxHeight * 1.69; // +69% total en hauteur (1.3 * 1.3 = 1.69)

                const aspect = imgWidth / imgHeight;
                let width, height;

                if (aspect > maxImageWidth / maxImageHeight) {
                    width = Math.min(maxImageWidth, cfg.imageMaxWidth);
                    height = width / aspect;
                } else {
                    height = Math.min(maxImageHeight, cfg.imageMaxHeight);
                    width = height * aspect;
                }

                // Centrer l'image horizontalement dans la fiche
                const imgX = xCenter - width / 2;

                // Centrer l'image verticalement dans la zone réservée
                const imgY = topMargin + (imageZoneHeight - height) / 2;

                // Bordure noire autour de l'image (2pt)
                this.doc.setDrawColor(0, 0, 0);
                this.doc.setLineWidth(2);
                this.doc.rect(imgX - 5.67, imgY - 5.67, width + 11.34, height + 11.34);

                // Dessiner l'image
                this.doc.addImage(dataUrl, 'JPEG', imgX, imgY, width, height);

            } catch (error) {
                console.error(`Erreur chargement image pour "${word}":`, error);
                // Continuer sans l'image (les mots restent à la même position)
            }
        }

        // 2. Mot en CAPITALES (OpenDyslexic Bold, 32pt) - Position FIXE
        this.doc.setFont('OpenDyslexic-Bold', 'normal');
        this.doc.setFontSize(cfg.fontSize.capital);
        this.doc.setTextColor(0, 0, 0);
        this.doc.text(word.toUpperCase(), xCenter, capitalY, { align: 'center' });

        // 3. Mot en script (OpenDyslexic, 36pt) - Position FIXE
        this.doc.setFont('OpenDyslexic', 'normal');
        this.doc.setFontSize(cfg.fontSize.script);
        this.doc.text(word.toLowerCase(), xCenter, scriptY, { align: 'center' });

        // 4. Mot en cursif (Écolier, 64pt - TRÈS GRAND) - Position FIXE
        // La police Écolier ne supporte pas Œ/œ, on les remplace par OE/oe
        const cursiveWord = word.toLowerCase()
            .replace(/œ/g, 'oe')
            .replace(/Œ/g, 'oe'); // Déjà en lowercase, mais par sécurité
        this.doc.setFont('Ecolier', 'normal');
        this.doc.setFontSize(cfg.fontSize.cursive);
        this.doc.text(cursiveWord, xCenter, cursiveY, { align: 'center' });
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
