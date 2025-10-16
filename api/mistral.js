/**
 * Fonction serverless Vercel pour Mistral AI
 * Génère des listes de mots thématiques pour la maternelle
 */

export default async function handler(req, res) {
    // CORS headers
    res.setHeader('Access-Control-Allow-Origin', '*');
    res.setHeader('Access-Control-Allow-Methods', 'POST, OPTIONS');
    res.setHeader('Access-Control-Allow-Headers', 'Content-Type');

    // Handle preflight
    if (req.method === 'OPTIONS') {
        return res.status(200).end();
    }

    if (req.method !== 'POST') {
        return res.status(405).json({ error: 'Method not allowed' });
    }

    try {
        const { theme, count = 10, excludeWords = [] } = req.body;

        if (!theme) {
            return res.status(400).json({ error: 'Theme parameter required' });
        }

        // Validation du nombre de mots
        const wordCount = Math.min(Math.max(parseInt(count) || 10, 5), 20);

        // Nettoyer et valider les mots à exclure
        const wordsToExclude = Array.isArray(excludeWords)
            ? excludeWords.filter(w => typeof w === 'string' && w.trim().length > 0)
            : [];

        // Clé API depuis les variables d'environnement Vercel
        const apiKey = process.env.MISTRAL_API_KEY;

        if (!apiKey) {
            return res.status(500).json({ error: 'API key not configured' });
        }

        // Construction du prompt XML structuré pour la maternelle française
        let excludeWordsXml = '';
        if (wordsToExclude.length > 0) {
            excludeWordsXml = `

<exclusions priority="CRITICAL">
    ⚠️ INTERDICTION ABSOLUE d'utiliser ces mots (ils sont déjà utilisés):
    ${wordsToExclude.map(w => `- ${w}`).join('\n    ')}

    Tu DOIS proposer des mots COMPLÈTEMENT DIFFÉRENTS de cette liste.
</exclusions>`;
        }

        let prompt = `Tu es un assistant pédagogique spécialisé en éducation maternelle française.

<tâche>
    <objectif>
        Générer EXACTEMENT ${wordCount} mots ou expressions simples en FRANÇAIS sur le thème "${theme}"
    </objectif>

    <public_cible>
        <âge>3-6 ans (Petite/Moyenne/Grande Section de maternelle)</âge>
        <langue>Français uniquement</langue>
    </public_cible>

    <exigences>
        <vocabulaire>
            - Vocabulaire FRANÇAIS courant et concret
            - Mots du quotidien familiers aux jeunes enfants
            - PAS de mots abstraits ou complexes
        </vocabulaire>

        <types_de_mots>
            - Préférence: Noms communs simples
            - Autorisé: Expressions courtes (2-3 mots max, ex: "feuille d'arbre", "pomme de pin")
            - INTERDIT: Verbes conjugués, adjectifs complexes
        </types_de_mots>

        <longueur>
            - Mots simples: maximum 12 lettres
            - Expressions: maximum 3 mots
            - Chaque élément DOIT être représentable par une image simple
        </longueur>
    </exigences>${excludeWordsXml}

    <format_sortie>
        IMPORTANT: Réponds UNIQUEMENT avec la liste des mots, un par ligne.
        - PAS de numérotation (1., 2., etc.)
        - PAS de tirets ou puces (-, *, •)
        - PAS d'explications ou commentaires
        - JUSTE les mots/expressions, un par ligne
    </format_sortie>

    <exemple thème="automne">
        feuille d'arbre
        champignon
        citrouille
        marron
        pluie
        arbre
        écureuil
        pomme de pin
        raisin
        vent d'automne
    </exemple>
</tâche>

Génère maintenant ${wordCount} mots/expressions FRANÇAIS niveau maternelle pour "${theme}":`;

        // Appel à l'API Mistral
        const mistralResponse = await fetch('https://api.mistral.ai/v1/chat/completions', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${apiKey}`
            },
            body: JSON.stringify({
                model: 'open-mistral-7b', // Modèle le plus économique (0.25€/1M tokens)
                messages: [
                    {
                        role: 'user',
                        content: prompt
                    }
                ],
                temperature: 0.7,
                max_tokens: 500
            })
        });

        if (!mistralResponse.ok) {
            const errorData = await mistralResponse.text();
            console.error('Mistral API error:', errorData);
            return res.status(mistralResponse.status).json({
                error: 'Mistral API error',
                details: errorData
            });
        }

        const data = await mistralResponse.json();

        // Extraire la réponse
        const content = data.choices?.[0]?.message?.content;

        if (!content) {
            return res.status(500).json({ error: 'No content in response' });
        }

        // Parser la liste de mots
        const words = content
            .split('\n')
            .map(line => line.trim())
            .filter(line => line.length > 0)
            .filter(line => !line.match(/^\d+[\.\)]/)) // Enlever les numéros éventuels
            .filter(line => line.length <= 30) // Filtrer les lignes trop longues (probablement du texte)
            .slice(0, wordCount); // Limiter au nombre demandé

        return res.status(200).json({
            theme,
            count: words.length,
            words,
            model: 'open-mistral-7b'
        });

    } catch (error) {
        console.error('Mistral API error:', error);
        return res.status(500).json({
            error: 'Internal server error',
            message: error.message
        });
    }
}
