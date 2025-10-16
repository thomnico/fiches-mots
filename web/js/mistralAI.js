/**
 * Module de génération de mots via Mistral AI
 * Utilise l'API serverless pour générer des listes de mots thématiques
 */

class MistralWordGenerator {
    constructor() {
        this.apiEndpoint = '/api/mistral';
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

        try {
            const response = await fetch(this.apiEndpoint, {
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
            console.error('❌ Erreur génération de mots:', error);
            throw error;
        }
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
