/**
 * Module de recherche d'images
 * Utilise Google Images comme source principale
 */

class ImageSearcher {
    constructor() {
        // Clés API depuis la configuration (config.api.js)
        if (typeof API_CONFIG === 'undefined') {
            console.error('❌ ERREUR: config.api.js non chargé! Copiez config.api.example.js vers config.api.js et ajoutez vos clés API.');
            throw new Error('Configuration API manquante');
        }

        this.unsplashAccessKey = API_CONFIG.unsplash.accessKey;
        this.pixabayApiKey = API_CONFIG.pixabay.apiKey;

        // Vérifier que les clés ne sont pas les valeurs par défaut
        if (this.unsplashAccessKey.includes('YOUR_') || this.pixabayApiKey.includes('YOUR_')) {
            console.error('❌ ERREUR: Clés API non configurées! Éditez web/js/config.api.js avec vos vraies clés.');
            throw new Error('Clés API non configurées');
        }
    }

    /**
     * Recherche des images pour un mot donné
     * Priorité: Pixabay (illustrations) puis Unsplash (photos)
     * RECHERCHE EN FRANÇAIS pour de meilleurs résultats
     * @param {string} word - Le mot à rechercher (en français)
     * @param {string} theme - Le thème optionnel (en français)
     * @returns {Promise<Array>} - Tableau d'URLs d'images
     */
    async searchImages(word, theme = '') {
        console.log(`🔍 Recherche d'images pour: ${word}${theme ? ` - Thème: ${theme}` : ''}`);

        try {
            // NOUVEAU: Rechercher en FRANÇAIS directement
            // Les APIs Pixabay et Unsplash supportent le français!

            // 1. Essayer Pixabay d'abord (meilleur pour illustrations/cliparts)
            const pixabayImages = await this.searchPixabayOptimized(word, theme);
            if (pixabayImages && pixabayImages.length >= CONFIG.imagesPerWord) {
                console.log(`✅ Pixabay: ${pixabayImages.length} images trouvées pour "${word}"`);
                return pixabayImages.slice(0, CONFIG.imagesPerWord);
            }

            console.log(`⚠️  Pas assez d'images Pixabay, essai Unsplash...`);

            // 2. Fallback Unsplash
            const unsplashImages = await this.searchUnsplashOptimized(word, theme);
            if (unsplashImages && unsplashImages.length >= CONFIG.imagesPerWord) {
                console.log(`✅ Unsplash: ${unsplashImages.length} images trouvées pour "${word}"`);
                return unsplashImages.slice(0, CONFIG.imagesPerWord);
            }

            // 3. Combiner les résultats si on n'a pas assez
            const combinedImages = [...(pixabayImages || []), ...(unsplashImages || [])];
            if (combinedImages.length >= CONFIG.imagesPerWord) {
                console.log(`✅ Combiné: ${combinedImages.length} images de Pixabay + Unsplash`);
                return combinedImages.slice(0, CONFIG.imagesPerWord);
            }

            console.log(`⚠️  Pas assez d'images, utilisation des placeholders`);
            return this.getPlaceholderImages(word);

        } catch (error) {
            console.error(`❌ Erreur lors de la recherche pour "${word}":`, error);
            return this.getPlaceholderImages(word);
        }
    }

    /**
     * Recherche optimisée sur Pixabay (VECTEURS en priorité, puis illustrations)
     * RECHERCHE EN FRANÇAIS
     * @param {string} word - Le mot en français
     * @param {string} theme - Le thème en français
     * @returns {Promise<Array>} - URLs d'images
     */
    async searchPixabayOptimized(word, theme) {
        try {
            // Stratégie de recherche pour plus de variété:
            // 1. Chercher le mot seul (sans thème) pour avoir des images spécifiques
            // 2. Si pas assez, chercher avec le thème
            // 3. Mélanger pour avoir de la diversité

            // Gestion des mots ambigus (contexte maternelle)
            let searchWord = word;
            if (word.toLowerCase() === 'marron' && theme && theme.toLowerCase() === 'automne') {
                // "marron" en automne = châtaigne, pas la couleur!
                searchWord = 'châtaigne marron';
                console.log(`🌰 Mot ambigu détecté: "marron" → "châtaigne marron" (contexte automne)`);
            }

            console.log(`🎨 Recherche Pixabay VECTEURS (FR) pour: "${searchWord}"`);

            // 1. Recherche prioritaire: le mot SEUL en FRANÇAIS (plus spécifique et varié)
            const wordOnlyUrl = `https://pixabay.com/api/?key=${this.pixabayApiKey}&q=${encodeURIComponent(searchWord)}&image_type=vector&per_page=20&safesearch=true&lang=fr`;

            const wordResponse = await fetch(wordOnlyUrl);
            if (wordResponse.ok) {
                const wordData = await wordResponse.json();
                const wordImages = wordData.hits ? wordData.hits.map(hit => hit.webformatURL) : [];
                console.log(`📌 Mot seul (FR): ${wordImages.length} vecteurs trouvés`);

                // Si on a assez d'images avec juste le mot, c'est parfait
                if (wordImages.length >= CONFIG.imagesPerWord) {
                    console.log(`✅ Pixabay: ${wordImages.length} vecteurs variés pour "${word}"`);
                    return wordImages;
                }

                // 2. Si pas assez, essayer avec le thème pour compléter
                if (theme && wordImages.length < CONFIG.imagesPerWord) {
                    console.log(`⚠️  Pas assez d'images, recherche avec thème (FR): "${word} ${theme}"`);

                    const themedUrl = `https://pixabay.com/api/?key=${this.pixabayApiKey}&q=${encodeURIComponent(word + ' ' + theme)}&image_type=vector&per_page=20&safesearch=true&lang=fr`;

                    const themedResponse = await fetch(themedUrl);
                    if (themedResponse.ok) {
                        const themedData = await themedResponse.json();
                        const themedImages = themedData.hits ? themedData.hits.map(hit => hit.webformatURL) : [];
                        console.log(`🎨 Avec thème (FR): ${themedImages.length} vecteurs trouvés`);

                        // Combiner en alternant pour plus de variété
                        const combinedImages = this.interleaveArrays(wordImages, themedImages);
                        console.log(`✅ Pixabay: ${combinedImages.length} vecteurs combinés (variés)`);
                        return combinedImages;
                    }
                }

                // 3. Fallback: essayer les illustrations si vraiment pas assez de vecteurs
                if (wordImages.length < CONFIG.imagesPerWord) {
                    console.log(`⚠️  Pas assez de vecteurs, ajout d'illustrations (FR)...`);

                    const illustrationUrl = `https://pixabay.com/api/?key=${this.pixabayApiKey}&q=${encodeURIComponent(word)}&image_type=illustration&per_page=20&safesearch=true&lang=fr`;

                    const illustrationResponse = await fetch(illustrationUrl);
                    if (illustrationResponse.ok) {
                        const illustrationData = await illustrationResponse.json();
                        const illustrationImages = illustrationData.hits ? illustrationData.hits.map(hit => hit.webformatURL) : [];
                        console.log(`🖼️  Illustrations (FR): ${illustrationImages.length} trouvées`);

                        const combinedImages = [...wordImages, ...illustrationImages];
                        console.log(`✅ Pixabay: ${combinedImages.length} images (vecteurs + illustrations)`);
                        return combinedImages;
                    }
                }

                return wordImages;
            }

            console.log(`⚠️  Pixabay HTTP ${wordResponse.status}`);
            return [];
        } catch (error) {
            console.error('❌ Erreur Pixabay:', error);
            return [];
        }
    }

    /**
     * Entrelace deux tableaux pour avoir de la variété
     * @param {Array} arr1 - Premier tableau
     * @param {Array} arr2 - Deuxième tableau
     * @returns {Array} - Tableau entrelacé
     */
    interleaveArrays(arr1, arr2) {
        const result = [];
        const maxLength = Math.max(arr1.length, arr2.length);

        for (let i = 0; i < maxLength; i++) {
            if (i < arr1.length) result.push(arr1[i]);
            if (i < arr2.length) result.push(arr2[i]);
        }

        return result;
    }

    /**
     * Recherche optimisée sur Unsplash (photos de livres pour enfants)
     * RECHERCHE EN FRANÇAIS
     * @param {string} word - Le mot en français
     * @param {string} theme - Le thème en français
     * @returns {Promise<Array>} - URLs d'images
     */
    async searchUnsplashOptimized(word, theme) {
        try {
            // Recherche en FRANÇAIS sur Unsplash
            const query = theme
                ? `${word} ${theme} livre enfants illustration`
                : `${word} livre enfants illustration`;

            console.log(`📸 Recherche Unsplash (FR): "${query}"`);

            const url = `https://api.unsplash.com/search/photos?query=${encodeURIComponent(query)}&per_page=${CONFIG.imagesPerWord}&orientation=landscape&content_filter=high`;

            const response = await fetch(url, {
                headers: {
                    'Authorization': `Client-ID ${this.unsplashAccessKey}`,
                    'Accept-Version': 'v1'
                }
            });

            if (!response.ok) {
                console.log(`⚠️  Unsplash HTTP ${response.status}`);
                return [];
            }

            const data = await response.json();
            if (data.results && data.results.length > 0) {
                return data.results.map(photo => photo.urls.regular);
            }

            return [];
        } catch (error) {
            console.error('❌ Erreur Unsplash:', error);
            return [];
        }
    }

    /**
     * Recherche sur Freepik via proxy CORS et web scraping
     * @param {string} query - La requête de recherche
     * @returns {Promise<Array>} - Tableau d'URLs d'images
     */
    async searchFreepikWithProxy(query) {
        try {
            console.log('🎨 Recherche Freepik pour:', query);

            // URL de recherche Freepik
            const searchUrl = `https://www.freepik.com/search?format=search&query=${encodeURIComponent(query)}&type=icon`;

            // Essayer chaque proxy jusqu'à trouver un qui fonctionne
            for (const proxy of this.corsProxies) {
                try {
                    const proxyUrl = proxy + encodeURIComponent(searchUrl);
                    console.log(`📡 Tentative proxy: ${proxy.substring(0, 30)}...`);

                    const response = await fetch(proxyUrl, {
                        signal: AbortSignal.timeout(8000) // 8 secondes timeout
                    });

                    if (!response.ok) {
                        console.log(`⚠️  HTTP ${response.status}, tentative suivante...`);
                        continue;
                    }

                    const html = await response.text();
                    console.log(`📄 HTML reçu: ${html.length} caractères`);

                    // Extraire les URLs d'images du HTML (Freepik utilise des URLs CDN)
                    const imageRegex = /https:\/\/[^"']+\.(freepik|flaticon|cdnpk)\.com[^"']+\.(jpg|jpeg|png|webp)/gi;
                    const matches = html.match(imageRegex) || [];

                    // Filtrer et déduper les images
                    const uniqueImages = [...new Set(matches)]
                        .filter(url => !url.includes('thumb'))
                        .filter(url => !url.includes('avatar'))
                        .slice(0, CONFIG.imagesPerWord * 2);

                    if (uniqueImages.length > 0) {
                        console.log(`✅ Freepik: ${uniqueImages.length} images extraites avec ${proxy.substring(0, 20)}...`);
                        return uniqueImages;
                    }

                    console.log('⚠️  Pas d\'images dans cette réponse, proxy suivant...');

                } catch (proxyError) {
                    console.log(`⚠️  Erreur avec ce proxy: ${proxyError.message}`);
                    continue;
                }
            }

            console.log('❌ Aucun proxy Freepik fonctionnel');
            return [];

        } catch (error) {
            console.error('❌ Erreur Freepik:', error);
            return [];
        }
    }

    /**
     * Recherche sur Google Images via proxy CORS
     * @param {string} query - La requête de recherche
     * @returns {Promise<Array>} - Tableau d'URLs d'images
     */
    async searchGoogleImagesWithProxy(query) {
        try {
            console.log('🔍 Recherche Google Images pour:', query);

            // URL de recherche Google Images
            const searchUrl = `https://www.google.com/search?tbm=isch&q=${encodeURIComponent(query)}`;
            const proxyUrl = this.corsProxy + encodeURIComponent(searchUrl);

            const response = await fetch(proxyUrl);
            if (!response.ok) {
                console.log(`⚠️  Google proxy HTTP ${response.status}`);
                return [];
            }

            const html = await response.text();
            console.log(`📄 HTML reçu: ${html.length} caractères`);

            // Extraire les URLs d'images du HTML
            const imageRegex = /https?:\/\/[^"'\s]+\.(jpg|jpeg|png|gif|webp)/gi;
            const matches = html.match(imageRegex) || [];

            // Filtrer et déduper
            const uniqueImages = [...new Set(matches)]
                .filter(url => !url.includes('google') && !url.includes('gstatic'))
                .slice(0, CONFIG.imagesPerWord * 2);

            if (uniqueImages.length > 0) {
                console.log(`✅ Google Images: ${uniqueImages.length} images extraites`);
                return uniqueImages;
            }

            console.log('⚠️  Aucune image Google trouvée');
            return [];

        } catch (error) {
            console.error('❌ Erreur Google Images:', error);
            return [];
        }
    }

    /**
     * Recherche via DuckDuckGo Images avec proxy CORS
     * @param {string} query - La requête de recherche
     * @returns {Promise<Array>} - Tableau d'URLs d'images
     */
    async searchDuckDuckGo(query) {
        try {
            console.log('🦆 Recherche DuckDuckGo pour:', query);

            // URL de recherche DuckDuckGo Images
            const searchUrl = `https://duckduckgo.com/?q=${encodeURIComponent(query)}&t=h_&iax=images&ia=images`;

            // Essayer chaque proxy
            for (const proxy of this.corsProxies) {
                try {
                    const proxyUrl = proxy + encodeURIComponent(searchUrl);
                    console.log(`📡 Tentative proxy: ${proxy.substring(0, 30)}...`);

                    const response = await fetch(proxyUrl, {
                        signal: AbortSignal.timeout(8000)
                    });

                    if (!response.ok) {
                        console.log(`⚠️  HTTP ${response.status}, tentative suivante...`);
                        continue;
                    }

                    const html = await response.text();
                    console.log(`📄 HTML reçu: ${html.length} caractères`);

                    // Extraire les URLs d'images du HTML
                    const imageRegex = /https?:\/\/[^"'\s]+\.(jpg|jpeg|png|gif|webp)/gi;
                    const matches = html.match(imageRegex) || [];

                    // Filtrer et déduper
                    const uniqueImages = [...new Set(matches)]
                        .filter(url => !url.includes('duckduckgo.com'))
                        .filter(url => !url.includes('.ico'))
                        .filter(url => !url.includes('logo'))
                        .slice(0, CONFIG.imagesPerWord * 2);

                    if (uniqueImages.length > 0) {
                        console.log(`✅ DuckDuckGo: ${uniqueImages.length} images extraites avec ${proxy.substring(0, 20)}...`);
                        return uniqueImages;
                    }

                    console.log('⚠️  Pas d\'images dans cette réponse, proxy suivant...');

                } catch (proxyError) {
                    console.log(`⚠️  Erreur avec ce proxy: ${proxyError.message}`);
                    continue;
                }
            }

            console.log('❌ Aucun proxy DuckDuckGo fonctionnel');
            return [];

        } catch (error) {
            console.error('❌ Erreur DuckDuckGo:', error);
            return [];
        }
    }

    /**
     * Obtient le token vqd nécessaire pour DuckDuckGo
     * OBSOLETE: Cette méthode n'est plus utilisée avec la nouvelle approche
     */
    async getVqdToken(query) {
        return null;
    }

    /**
     * Recherche directe via Freepik API (gratuit, 100 req/h)
     * @param {string} word - Le mot en anglais
     * @param {string} theme - Le thème en anglais
     * @returns {Promise<Array>} - Tableau d'URLs d'images
     */
    async searchFreepikDirect(word, theme) {
        try {
            // Clé API de démonstration Freepik
            // Pour production: créer un compte sur https://freepik.com/api
            const apiKey = 'FPSXdd89e2a75d6e4f97b907aa5e9bbf6d88';

            const query = theme ? `${word} ${theme} sticker` : `${word} sticker`;

            const url = `https://api.freepik.com/v1/resources?locale=en-US&term=${encodeURIComponent(query)}&filters[content_type][icon]=1&order=latest&limit=${CONFIG.imagesPerWord * 2}`;

            const response = await fetch(url, {
                headers: {
                    'Accept': 'application/json',
                    'X-Freepik-API-Key': apiKey
                }
            });

            if (!response.ok) {
                throw new Error(`Freepik API error: ${response.status}`);
            }

            const data = await response.json();

            if (data.data && data.data.length > 0) {
                // Extraire les URLs des thumbnails
                const imageUrls = data.data
                    .filter(item => item.thumbnail && item.thumbnail.url)
                    .map(item => item.thumbnail.url);

                console.log(`✅ Freepik: ${imageUrls.length} images trouvées`);
                return imageUrls;
            }

            return [];

        } catch (error) {
            console.warn('⚠️  Freepik API non disponible:', error.message);
            return [];
        }
    }

    /**
     * Recherche via Google Images
     * @param {string} word - Le mot en anglais
     * @param {string} theme - Le thème en anglais
     * @param {boolean} prioritizeFreepik - Prioriser Freepik
     * @returns {Promise<Array>} - Tableau d'URLs d'images
     */
    async searchGoogleImages(word, theme, prioritizeFreepik = true) {
        try {
            // Construction de la requête de recherche
            let searchQuery;
            if (prioritizeFreepik) {
                searchQuery = theme
                    ? `site:freepik.com ${word} ${theme} sticker icon`
                    : `site:freepik.com ${word} sticker icon`;
            } else {
                searchQuery = theme
                    ? `${word} ${theme} clipart cartoon sticker`
                    : `${word} clipart cartoon sticker`;
            }

            // Note: En production, il faudrait utiliser une API backend
            // Car les navigateurs bloquent les requêtes CORS vers Google
            // Pour cette démo, on simule avec des URLs de placeholder

            // Alternative: Utiliser Unsplash API (gratuit, pas de CORS)
            return await this.searchUnsplash(word, theme);

        } catch (error) {
            console.error('Erreur Google Images:', error);
            return [];
        }
    }

    /**
     * Recherche via Pexels (API gratuite sans authentification pour petites requêtes)
     * @param {string} word - Le mot à rechercher
     * @param {string} theme - Le thème
     * @returns {Promise<Array>} - Tableau d'URLs d'images
     */
    async searchPexels(word, theme) {
        try {
            // Utiliser Pexels via leur API publique
            // Note: Pexels nécessite normalement une clé API mais on peut utiliser
            // des URLs directes pour des images spécifiques

            // Alternative: Utiliser Pixabay qui a une API plus permissive
            return await this.searchPixabay(word, theme);

        } catch (error) {
            console.error('Erreur Pexels:', error);
            return this.getPlaceholderImages(word);
        }
    }

    /**
     * Recherche via Pixabay (API publique gratuite)
     * Optimisée pour la maternelle avec mots-clés intelligents
     * @param {string} word - Le mot à rechercher
     * @param {string} theme - Le thème
     * @returns {Promise<Array>} - Tableau d'URLs d'images
     */
    async searchPixabay(word, theme) {
        try {
            // Clé API Pixabay (limite à 100 requêtes/heure)
            const apiKey = '45960108-71a82f16e84e8b1b63f39a27a';

            // Construire des requêtes intelligentes pour la maternelle
            const queries = [];

            if (theme) {
                // Avec thème: essayer plusieurs variantes
                queries.push(`${word} ${theme} cartoon simple`);
                queries.push(`${word} ${theme} illustration`);
                queries.push(`${word} ${theme} clipart`);
            } else {
                // Sans thème
                queries.push(`${word} cartoon simple`);
                queries.push(`${word} illustration children`);
                queries.push(`${word} clipart`);
            }

            // Essayer chaque requête jusqu'à trouver des résultats
            for (const query of queries) {
                console.log(`🔍 Pixabay: recherche "${query}"`);

                const url = `https://pixabay.com/api/?key=${apiKey}&q=${encodeURIComponent(query)}&image_type=illustration&per_page=20&safesearch=true&editors_choice=false`;

                try {
                    const response = await fetch(url);
                    if (!response.ok) {
                        console.log(`⚠️  Pixabay HTTP ${response.status}`);
                        continue;
                    }

                    const data = await response.json();
                    console.log(`📊 Pixabay: ${data.totalHits} résultats pour "${query}"`);

                    if (data.hits && data.hits.length > 0) {
                        // Prendre les meilleures images
                        const imageUrls = data.hits
                            .slice(0, CONFIG.imagesPerWord)
                            .map(hit => hit.webformatURL);

                        console.log(`✅ Pixabay: ${imageUrls.length} images retournées`);
                        return imageUrls;
                    }
                } catch (fetchError) {
                    console.error(`❌ Erreur fetch Pixabay:`, fetchError);
                    continue;
                }
            }

            // Aucun résultat trouvé
            console.log('⚠️  Pixabay: aucun résultat pour toutes les requêtes');
            return [];

        } catch (error) {
            console.error('❌ Erreur Pixabay:', error);
            return [];
        }
    }

    /**
     * Ancienne méthode Unsplash (remplacée par Pixabay)
     */
    async searchUnsplash(word, theme) {
        // Utiliser Pixabay à la place
        return await this.searchPixabay(word, theme);
    }

    /**
     * Génère des URLs d'images placeholder
     * @param {string} word - Le mot
     * @returns {Array} - Tableau d'URLs d'images placeholder
     */
    getPlaceholderImages(word) {
        // Utiliser un service de placeholder avec des couleurs et du texte
        const colors = ['FFB6C1', '87CEEB', '98FB98', 'FFD700', 'DDA0DD'];
        return colors.slice(0, CONFIG.imagesPerWord).map((color, index) => {
            return `https://via.placeholder.com/400x300/${color}/333333?text=${encodeURIComponent(word)}+${index + 1}`;
        });
    }

    /**
     * Télécharge une image en tant que blob
     * @param {string} url - URL de l'image
     * @returns {Promise<string>} - Data URL de l'image
     */
    async downloadImageAsDataURL(url) {
        try {
            // Utiliser fetch pour télécharger l'image
            const response = await fetch(url);
            const blob = await response.blob();

            // Convertir le blob en Data URL
            return new Promise((resolve, reject) => {
                const reader = new FileReader();
                reader.onloadend = () => resolve(reader.result);
                reader.onerror = reject;
                reader.readAsDataURL(blob);
            });

        } catch (error) {
            console.error('Erreur téléchargement image:', error);
            // Retourner l'URL originale si le téléchargement échoue
            return url;
        }
    }

    /**
     * Vérifie si une URL d'image est accessible
     * @param {string} url - URL à vérifier
     * @returns {Promise<boolean>}
     */
    async isImageAccessible(url) {
        return new Promise((resolve) => {
            const img = new Image();
            img.onload = () => resolve(true);
            img.onerror = () => resolve(false);
            img.src = url;
        });
    }
}

// Instance globale
const imageSearcher = new ImageSearcher();
