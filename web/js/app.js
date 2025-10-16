/**
 * Application principale
 * Gère l'interaction utilisateur et l'orchestration des modules
 */

class App {
    constructor() {
        this.theme = '';
        this.words = [];
        this.imagesData = {}; // { word: [url1, url2, url3] }
        this.selectedImages = {}; // { word: selectedUrl }

        this.initializeElements();
        this.attachEventListeners();
    }

    /**
     * Initialise les références aux éléments DOM
     */
    initializeElements() {
        // Sections
        this.stepInput = document.getElementById('step-input');
        this.stepSelection = document.getElementById('step-selection');
        this.stepGenerate = document.getElementById('step-generate');

        // Champs de formulaire
        this.themeInput = document.getElementById('theme');
        this.wordsInput = document.getElementById('words');

        // Boutons
        this.btnSearch = document.getElementById('btn-search');
        this.btnBack = document.getElementById('btn-back');
        this.btnGenerate = document.getElementById('btn-generate');

        // Conteneurs
        this.imageSelectionContainer = document.getElementById('image-selection-container');
        this.progressBar = document.getElementById('progress-bar');
        this.progressText = document.getElementById('progress-text');
        this.errorMessage = document.getElementById('error-message');
    }

    /**
     * Attache les écouteurs d'événements
     */
    attachEventListeners() {
        this.btnSearch.addEventListener('click', () => this.handleSearch());
        this.btnBack.addEventListener('click', () => this.handleBack());
        this.btnGenerate.addEventListener('click', () => this.handleGenerate());

        // Délégation d'événements pour les boutons "Plus d'images" (créés dynamiquement)
        this.imageSelectionContainer.addEventListener('click', (e) => {
            if (e.target.classList.contains('btn-more-images')) {
                const word = e.target.dataset.word;
                this.handleMoreImages(word);
            }
        });
    }

    /**
     * Affiche une section et cache les autres
     */
    showStep(step) {
        document.querySelectorAll('.step').forEach(s => s.classList.remove('active'));
        step.classList.add('active');
    }

    /**
     * Affiche un message d'erreur
     */
    showError(message) {
        this.errorMessage.textContent = message;
        this.errorMessage.classList.add('show');
        setTimeout(() => {
            this.errorMessage.classList.remove('show');
        }, 5000);
    }

    /**
     * Gère la recherche d'images
     */
    async handleSearch() {
        try {
            // Récupérer et valider les entrées
            this.theme = this.themeInput.value.trim();
            const wordsText = this.wordsInput.value.trim();

            if (!wordsText) {
                this.showError('⚠️ Veuillez entrer au moins un mot');
                return;
            }

            // Parser les mots (un par ligne)
            this.words = wordsText.split('\n')
                .map(w => w.trim())
                .filter(w => w.length > 0);

            if (this.words.length === 0) {
                this.showError('⚠️ Veuillez entrer au moins un mot valide');
                return;
            }

            console.log(`📝 Recherche pour ${this.words.length} mot(s)${this.theme ? ` avec thème "${this.theme}"` : ''}`);

            // Désactiver le bouton pendant la recherche
            this.btnSearch.disabled = true;
            this.btnSearch.textContent = '⏳ Recherche en cours...';

            // Passer à l'étape de sélection
            this.showStep(this.stepSelection);

            // Lancer la recherche d'images pour tous les mots
            await this.searchAllImages();

            // Réactiver le bouton
            this.btnSearch.disabled = false;
            this.btnSearch.textContent = '🔍 Rechercher les images';

        } catch (error) {
            console.error('Erreur lors de la recherche:', error);
            this.showError('❌ Erreur lors de la recherche d\'images');
            this.btnSearch.disabled = false;
            this.btnSearch.textContent = '🔍 Rechercher les images';
        }
    }

    /**
     * Recherche les images pour tous les mots
     */
    async searchAllImages() {
        this.imageSelectionContainer.innerHTML = '';
        this.imagesData = {};
        this.selectedImages = {};

        for (const word of this.words) {
            // Créer la section pour ce mot
            const wordSection = this.createWordSection(word);
            this.imageSelectionContainer.appendChild(wordSection);

            // Lancer la recherche d'images
            try {
                const images = await imageSearcher.searchImages(word, this.theme);
                this.imagesData[word] = images;

                // Afficher les images
                this.displayImagesForWord(word, images, wordSection);

            } catch (error) {
                console.error(`Erreur recherche images pour "${word}":`, error);
                this.displayImagesForWord(word, [], wordSection);
            }
        }
    }

    /**
     * Crée la section HTML pour un mot
     */
    createWordSection(word) {
        const section = document.createElement('div');
        section.className = 'word-section';
        // Encoder le mot pour créer un ID valide (remplacer tous les caractères spéciaux)
        // D'abord remplacer les apostrophes (non encodées par encodeURIComponent)
        // puis encoder, puis remplacer %XX par des tirets
        const wordId = encodeURIComponent(word.replace(/'/g, '-'))
            .replace(/%[0-9A-F]{2}/g, '-');
        section.id = `word-${wordId}`;
        section.dataset.currentPage = '0';  // Pour la pagination

        section.innerHTML = `
            <h3>📝 ${word}</h3>
            <p>Sélectionnez une image parmi les propositions :</p>
            <div class="images-grid" id="images-${wordId}">
                ${this.createLoadingSpinners()}
            </div>
            <div class="pagination-buttons" style="display: none; margin-top: 15px; text-align: center;">
                <button class="btn-more-images" data-word="${word}">
                    ➡️ Voir plus d'images
                </button>
            </div>
        `;

        return section;
    }

    /**
     * Crée des spinners de chargement
     */
    createLoadingSpinners() {
        let html = '';
        for (let i = 0; i < CONFIG.imagesPerWord; i++) {
            html += `
                <div class="image-loading">
                    <div class="spinner"></div>
                </div>
            `;
        }
        return html;
    }

    /**
     * Affiche les images pour un mot (avec pagination)
     */
    displayImagesForWord(word, images, section) {
        const wordId = encodeURIComponent(word.replace(/'/g, '-')).replace(/%[0-9A-F]{2}/g, '-');
        const grid = section.querySelector(`#images-${wordId}`);

        if (images.length === 0) {
            grid.innerHTML = '<p style="color: #999;">Aucune image trouvée</p>';
            return;
        }

        // Stocker toutes les images dans la section pour la pagination
        section.dataset.allImages = JSON.stringify(images);

        // Afficher la première page (3 premières images)
        this.displayImagePage(word, section, 0);

        // Afficher le bouton "Plus d'images" s'il y a plus de 3 images
        const paginationButtons = section.querySelector('.pagination-buttons');
        if (images.length > CONFIG.imagesPerWord) {
            paginationButtons.style.display = 'block';
        }
    }

    /**
     * Affiche une page d'images (3 images)
     */
    displayImagePage(word, section, pageIndex) {
        const wordId = encodeURIComponent(word.replace(/'/g, '-')).replace(/%[0-9A-F]{2}/g, '-');
        const grid = section.querySelector(`#images-${wordId}`);
        const allImages = JSON.parse(section.dataset.allImages || '[]');

        // Calculer les indices de début et fin
        const startIndex = pageIndex * CONFIG.imagesPerWord;
        const endIndex = startIndex + CONFIG.imagesPerWord;
        const pageImages = allImages.slice(startIndex, endIndex);

        grid.innerHTML = '';

        pageImages.forEach((imageUrl, index) => {
            const imageOption = document.createElement('div');
            imageOption.className = 'image-option';
            imageOption.dataset.word = word;
            imageOption.dataset.url = imageUrl;

            imageOption.innerHTML = `
                <img src="${imageUrl}" alt="${word} ${startIndex + index + 1}"
                     onerror="this.src='https://via.placeholder.com/400x300/CCCCCC/666666?text=Image+non+disponible'">
                <div class="checkmark">✓</div>
            `;

            // Événement de sélection
            imageOption.addEventListener('click', () => {
                this.selectImage(word, imageUrl, imageOption);
            });

            // Sélectionner automatiquement la première image
            if (index === 0) {
                this.selectImage(word, imageUrl, imageOption);
            }

            grid.appendChild(imageOption);
        });

        // Mettre à jour le bouton selon s'il reste des images
        section.dataset.currentPage = pageIndex.toString();
        this.updateMoreImagesButton(word, section);
    }

    /**
     * Gère le clic sur "Plus d'images"
     */
    handleMoreImages(word) {
        const wordId = encodeURIComponent(word.replace(/'/g, '-')).replace(/%[0-9A-F]{2}/g, '-');
        const section = document.getElementById(`word-${wordId}`);
        const allImages = JSON.parse(section.dataset.allImages || '[]');
        const currentPage = parseInt(section.dataset.currentPage || '0');

        // Page suivante (循环)
        const nextPage = currentPage + 1;
        const maxPages = Math.ceil(allImages.length / CONFIG.imagesPerWord);

        // Si on arrive à la fin, revenir au début
        const newPage = nextPage >= maxPages ? 0 : nextPage;

        console.log(`➡️  "${word}": Page ${newPage + 1}/${maxPages}`);

        // Afficher la nouvelle page
        this.displayImagePage(word, section, newPage);
    }

    /**
     * Met à jour le bouton "Plus d'images"
     */
    updateMoreImagesButton(word, section) {
        const allImages = JSON.parse(section.dataset.allImages || '[]');
        const currentPage = parseInt(section.dataset.currentPage || '0');
        const maxPages = Math.ceil(allImages.length / CONFIG.imagesPerWord);

        const button = section.querySelector('.btn-more-images');
        if (button) {
            // Texte du bouton avec indication de la page
            const nextPage = currentPage + 1;
            if (nextPage >= maxPages) {
                button.textContent = `⬅️ Retour aux premières images`;
            } else {
                button.textContent = `➡️ Voir plus d'images (${nextPage + 1}/${maxPages})`;
            }
        }
    }

    /**
     * Sélectionne une image pour un mot
     */
    selectImage(word, imageUrl, imageElement) {
        // Désélectionner les autres images du même mot
        // Pour éviter les problèmes d'échappement, sélectionner toutes les options
        // et filtrer en JavaScript
        const allOptions = document.querySelectorAll('.image-option');
        allOptions.forEach(opt => {
            if (opt.dataset.word === word) {
                opt.classList.remove('selected');
            }
        });

        // Sélectionner cette image
        imageElement.classList.add('selected');
        this.selectedImages[word] = imageUrl;

        console.log(`✓ Image sélectionnée pour "${word}":`, imageUrl);
    }

    /**
     * Retour à l'étape précédente
     */
    handleBack() {
        this.showStep(this.stepInput);
    }

    /**
     * Génère le PDF
     */
    async handleGenerate() {
        try {
            // Vérifier que toutes les images sont sélectionnées
            const missingSelections = this.words.filter(w => !this.selectedImages[w]);
            if (missingSelections.length > 0) {
                this.showError(`⚠️ Veuillez sélectionner une image pour: ${missingSelections.join(', ')}`);
                return;
            }

            console.log('📄 Génération du PDF...');
            this.showStep(this.stepGenerate);

            // Préparer les données pour le PDF
            const pdfData = this.words.map(word => ({
                word: word,
                imageUrl: this.selectedImages[word]
            }));

            // Générer le PDF avec callback de progression
            await pdfGenerator.generatePDF(pdfData, this.theme, (progress) => {
                this.updateProgress(progress);
            });

            // Succès !
            this.progressText.textContent = '✅ PDF généré avec succès !';

            // Retourner à l'étape 1 après 2 secondes
            setTimeout(() => {
                this.showStep(this.stepInput);
                this.resetProgress();
            }, 2000);

        } catch (error) {
            console.error('Erreur génération PDF:', error);
            this.showError('❌ Erreur lors de la génération du PDF');
            this.showStep(this.stepSelection);
        }
    }

    /**
     * Met à jour la barre de progression
     */
    updateProgress(percentage) {
        this.progressBar.style.width = `${percentage}%`;

        if (percentage < 30) {
            this.progressText.textContent = 'Chargement des polices...';
        } else if (percentage < 70) {
            this.progressText.textContent = 'Téléchargement des images...';
        } else if (percentage < 100) {
            this.progressText.textContent = 'Génération du PDF...';
        } else {
            this.progressText.textContent = 'Finalisation...';
        }
    }

    /**
     * Réinitialise la progression
     */
    resetProgress() {
        this.progressBar.style.width = '0%';
        this.progressText.textContent = 'Préparation...';
    }
}

// Initialiser l'application au chargement de la page
document.addEventListener('DOMContentLoaded', () => {
    console.log('🚀 Application Fiches-Mots initialisée');
    const app = new App();
});
