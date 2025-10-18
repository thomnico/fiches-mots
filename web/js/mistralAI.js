/**
 * Module de génération de mots via Mistral AI
 * Utilise l'API serverless pour générer des listes de mots thématiques
 */

class MistralWordGenerator {
    constructor() {
        this.apiEndpoint = '/api/mistral';
        this.timeout = 45000; // 45 secondes (plus long pour mobile)
        this.maxRetries = 2; // Nombre de tentatives en cas d'erreur réseau
    }

    /**
     * Fetch avec timeout et gestion des erreurs réseau
     * @private
     */
    async fetchWithTimeout(url, options = {}, timeoutMs = this.timeout) {
        const controller = new AbortController();
        const timeoutId = setTimeout(() => controller.abort(), timeoutMs);

        try {
            const response = await fetch(url, {
                ...options,
                signal: controller.signal
            });
            clearTimeout(timeoutId);
            return response;
        } catch (error) {
            clearTimeout(timeoutId);

            // Détecter le type d'erreur
            if (error.name === 'AbortError') {
                throw new Error('La génération prend trop de temps. Vérifiez votre connexion internet.');
            }

            if (error.message.includes('Failed to fetch') ||
                error.message.includes('NetworkError') ||
                error.message.includes('ERR_INTERNET_DISCONNECTED')) {
                throw new Error('Pas de connexion internet. Vérifiez votre réseau et réessayez.');
            }

            throw error;
        }
    }

    /**
     * Génère une liste de mots pour un thème donné
     * @param {string} theme - Le thème (ex: "automne", "animaux", "noël")
     * @param {number} count - Nombre de mots à générer (5-20)
     * @param {Array<string>} excludeWords - Mots à exclure (optionnel)
     * @returns {Promise<Array<string>>} - Liste de mots générés
     */
    async generateWords(theme, count = 10, excludeWords = []) {
        if (!theme || theme.trim().length === 0) {
            throw new Error('Le thème ne peut pas être vide');
        }

        const cleanTheme = theme.trim();
        const wordCount = Math.min(Math.max(parseInt(count) || 10, 5), 20);

        console.log(`🪄 Génération de ${wordCount} mots sur le thème "${cleanTheme}"...`);
        if (excludeWords.length > 0) {
            console.log(`🚫 Mots à exclure: ${excludeWords.join(', ')}`);
        }

        // Tentatives avec retry en cas d'erreur réseau
        let lastError = null;

        for (let attempt = 0; attempt <= this.maxRetries; attempt++) {
            if (attempt > 0) {
                console.log(`🔄 Tentative ${attempt + 1}/${this.maxRetries + 1}...`);
                // Attendre un peu avant de réessayer (1 seconde par tentative)
                await new Promise(resolve => setTimeout(resolve, 1000 * attempt));
            }

            try {
                const response = await this.fetchWithTimeout(this.apiEndpoint, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({
                        theme: cleanTheme,
                        count: wordCount,
                        excludeWords: excludeWords
                    })
                });

                if (!response.ok) {
                    const errorData = await response.json().catch(() => ({}));

                    // Erreurs 5xx sont temporaires, on peut retry
                    if (response.status >= 500 && attempt < this.maxRetries) {
                        lastError = new Error(errorData.error || `Erreur serveur: ${response.status}`);
                        continue;
                    }

                    throw new Error(errorData.error || `Erreur API: ${response.status}`);
                }

                const data = await response.json();

                if (!data.words || !Array.isArray(data.words)) {
                    throw new Error('Format de réponse invalide');
                }

                if (data.words.length === 0) {
                    throw new Error('Aucun mot généré par l\'IA');
                }

                console.log(`✅ ${data.words.length} mots générés:`, data.words);

                return data.words;

            } catch (error) {
                lastError = error;

                // Si c'est une erreur réseau et qu'on a encore des retries, continuer
                if ((error.message.includes('connexion internet') ||
                     error.message.includes('prend trop de temps')) &&
                    attempt < this.maxRetries) {
                    console.log(`⚠️ ${error.message} - Nouvelle tentative...`);
                    continue;
                }

                // Sinon, lancer l'erreur
                console.error('❌ Erreur génération de mots:', error);
                throw error;
            }
        }

        // Si on arrive ici, toutes les tentatives ont échoué
        console.error('❌ Toutes les tentatives ont échoué');
        throw lastError;
    }

    /**
     * Teste si l'API Mistral est configurée et accessible
     * @returns {Promise<boolean>}
     */
    async testConnection() {
        try {
            const words = await this.generateWords('test', 3);
            return words.length > 0;
        } catch (error) {
            console.error('Test de connexion Mistral échoué:', error);
            return false;
        }
    }
}

// Instance globale
const mistralWordGenerator = new MistralWordGenerator();
