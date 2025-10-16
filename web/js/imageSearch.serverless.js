/**
 * Module de recherche d'images - VERSION SERVERLESS
 * Utilise les fonctions serverless Vercel pour cacher les clés API
 *
 * Cette version appelle /api/pixabay et /api/unsplash au lieu d'appeler
 * directement les APIs avec les clés exposées côté client.
 */

class ImageSearcher {
    constructor() {
        // Pas besoin de clés API côté client avec les fonctions serverless
        console.log('🔐 Mode serverless: les clés API sont sécurisées côté serveur');

        // Détecter si on est en dev local ou en production
        this.isDevelopment = window.location.hostname === 'localhost' ||
                            window.location.hostname === '127.0.0.1';

        // URLs des endpoints serverless
        this.pixabayEndpoint = this.isDevelopment
            ? 'http://localhost:3000/api/pixabay'  // Dev local avec vercel dev
            : '/api/pixabay';  // Production Vercel

        this.unsplashEndpoint = this.isDevelopment
            ? 'http://localhost:3000/api/unsplash'
            : '/api/unsplash';
    }

    /**
     * Recherche des images pour un mot donné
     * @param {string} word - Le mot à rechercher (en français)
     * @param {string} theme - Le thème optionnel (en français)
     * @returns {Promise<Array>} - Tableau d'URLs d'images
     */
    async searchImages(word, theme = '') {
        console.log(`🔍 Recherche d'images pour: ${word}${theme ? ` - Thème: ${theme}` : ''}`);

        try {
            // 1. Essayer Pixabay d'abord (meilleur pour illustrations/cliparts)
            const pixabayImages = await this.searchPixabayOptimized(word, theme);
            if (pixabayImages && pixabayImages.length > 0) {
                console.log(`✅ Pixabay: ${pixabayImages.length} images trouvées pour "${word}"`);

                if (pixabayImages.length >= CONFIG.imagesPerWord) {
                    return pixabayImages;
                }
            }

            console.log(`⚠️  Pas assez d'images Pixabay, essai Unsplash...`);

            // 2. Fallback Unsplash
            const unsplashImages = await this.searchUnsplashOptimized(word, theme);
            if (unsplashImages && unsplashImages.length > 0) {
                console.log(`✅ Unsplash: ${unsplashImages.length} images trouvées pour "${word}"`);

                if (unsplashImages.length >= CONFIG.imagesPerWord) {
                    return unsplashImages;
                }
            }

            // 3. Combiner les résultats si nécessaire
            const combinedImages = [...(pixabayImages || []), ...(unsplashImages || [])];
            if (combinedImages.length > 0) {
                console.log(`✅ Combiné: ${combinedImages.length} images de Pixabay + Unsplash`);
                return combinedImages;
            }

            console.log(`⚠️  Pas assez d'images, utilisation des placeholders`);
            return this.getPlaceholderImages(word);

        } catch (error) {
            console.error(`❌ Erreur lors de la recherche pour "${word}":`, error);
            return this.getPlaceholderImages(word);
        }
    }

    /**
     * Recherche optimisée sur Pixabay via fonction serverless
     */
    async searchPixabayOptimized(word, theme) {
        try {
            // Gestion des mots ambigus
            let searchWord = word;
            if (word.toLowerCase() === 'marron' && theme && theme.toLowerCase() === 'automne') {
                searchWord = 'châtaigne marron';
                console.log(`🌰 Mot ambigu détecté: "marron" → "châtaigne marron" (contexte automne)`);
            }

            console.log(`🎨 Recherche Pixabay VECTEURS (FR) pour: "${searchWord}"`);

            // 1. Recherche le mot SEUL (plus de variété)
            const wordOnlyUrl = `${this.pixabayEndpoint}?query=${encodeURIComponent(searchWord)}&image_type=vector&per_page=20&lang=fr`;

            const wordResponse = await fetch(wordOnlyUrl);
            if (wordResponse.ok) {
                const wordData = await wordResponse.json();
                const wordImages = wordData.hits ? wordData.hits.map(hit => hit.webformatURL) : [];
                console.log(`📌 Mot seul (FR): ${wordImages.length} vecteurs trouvés`);

                if (wordImages.length >= CONFIG.imagesPerWord) {
                    return wordImages;
                }

                // 2. Compléter avec recherche thématique si besoin
                if (theme && wordImages.length < CONFIG.imagesPerWord) {
                    const themedUrl = `${this.pixabayEndpoint}?query=${encodeURIComponent(word + ' ' + theme)}&image_type=vector&per_page=20&lang=fr`;

                    const themedResponse = await fetch(themedUrl);
                    if (themedResponse.ok) {
                        const themedData = await themedResponse.json();
                        const themedImages = themedData.hits ? themedData.hits.map(hit => hit.webformatURL) : [];

                        // Combiner et dédupliquer
                        const combined = [...new Set([...wordImages, ...themedImages])];
                        console.log(`📌 Avec thème: ${combined.length} vecteurs au total`);

                        if (combined.length >= CONFIG.imagesPerWord) {
                            return combined;
                        }
                    }
                }

                // 3. Fallback vers illustrations si pas assez de vecteurs
                if (wordImages.length < CONFIG.imagesPerWord) {
                    const illustrationUrl = `${this.pixabayEndpoint}?query=${encodeURIComponent(searchWord)}&image_type=illustration&per_page=20&lang=fr`;

                    const illustrationResponse = await fetch(illustrationUrl);
                    if (illustrationResponse.ok) {
                        const illustrationData = await illustrationResponse.json();
                        const illustrationImages = illustrationData.hits ? illustrationData.hits.map(hit => hit.webformatURL) : [];

                        const combined = [...new Set([...wordImages, ...illustrationImages])];
                        console.log(`📌 Avec illustrations: ${combined.length} images au total`);
                        return combined;
                    }
                }

                return wordImages;
            }

            return [];

        } catch (error) {
            console.error('❌ Erreur Pixabay:', error);
            return [];
        }
    }

    /**
     * Recherche optimisée sur Unsplash via fonction serverless
     */
    async searchUnsplashOptimized(word, theme) {
        try {
            const query = theme
                ? `${word} ${theme} livre enfants illustration`
                : `${word} livre enfants illustration`;

            console.log(`📸 Recherche Unsplash (FR) pour: "${query}"`);

            const url = `${this.unsplashEndpoint}?query=${encodeURIComponent(query)}&per_page=20&orientation=landscape`;

            const response = await fetch(url);
            if (response.ok) {
                const data = await response.json();
                const images = data.results ? data.results.map(result => result.urls.regular) : [];
                console.log(`📌 Unsplash: ${images.length} photos trouvées`);

                if (images.length >= CONFIG.imagesPerWord) {
                    return images;
                }

                // Fallback sans "illustration"
                if (images.length < CONFIG.imagesPerWord) {
                    const fallbackQuery = theme ? `${word} ${theme}` : word;
                    const fallbackUrl = `${this.unsplashEndpoint}?query=${encodeURIComponent(fallbackQuery)}&per_page=20&orientation=landscape`;

                    const fallbackResponse = await fetch(fallbackUrl);
                    if (fallbackResponse.ok) {
                        const fallbackData = await fallbackResponse.json();
                        const fallbackImages = fallbackData.results ? fallbackData.results.map(result => result.urls.regular) : [];

                        const combined = [...new Set([...images, ...fallbackImages])];
                        console.log(`📌 Unsplash fallback: ${combined.length} photos au total`);
                        return combined;
                    }
                }

                return images;
            }

            return [];

        } catch (error) {
            console.error('❌ Erreur Unsplash:', error);
            return [];
        }
    }

    /**
     * Images placeholder en cas d'échec
     */
    getPlaceholderImages(word) {
        console.log(`📦 Utilisation des placeholders pour "${word}"`);
        return [
            `https://via.placeholder.com/400x300/4A90E2/FFFFFF?text=${encodeURIComponent(word)}+1`,
            `https://via.placeholder.com/400x300/7B68EE/FFFFFF?text=${encodeURIComponent(word)}+2`,
            `https://via.placeholder.com/400x300/52C41A/FFFFFF?text=${encodeURIComponent(word)}+3`
        ];
    }

    /**
     * Télécharge une image en Data URL pour l'inclure dans le PDF
     */
    async downloadImageAsDataURL(imageUrl) {
        try {
            const response = await fetch(imageUrl);
            const blob = await response.blob();

            return new Promise((resolve, reject) => {
                const reader = new FileReader();
                reader.onloadend = () => resolve(reader.result);
                reader.onerror = reject;
                reader.readAsDataURL(blob);
            });
        } catch (error) {
            console.error('Erreur téléchargement image:', error);
            throw error;
        }
    }
}

// Instance globale
const imageSearcher = new ImageSearcher();
