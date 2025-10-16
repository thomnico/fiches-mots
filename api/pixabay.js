/**
 * Fonction serverless Vercel pour Pixabay
 * Cache la clé API côté serveur
 */

export default async function handler(req, res) {
    // CORS headers
    res.setHeader('Access-Control-Allow-Origin', '*');
    res.setHeader('Access-Control-Allow-Methods', 'GET, OPTIONS');
    res.setHeader('Access-Control-Allow-Headers', 'Content-Type');

    // Handle preflight
    if (req.method === 'OPTIONS') {
        return res.status(200).end();
    }

    if (req.method !== 'GET') {
        return res.status(405).json({ error: 'Method not allowed' });
    }

    try {
        const { query, image_type = 'vector', per_page = 20, lang = 'fr' } = req.query;

        if (!query) {
            return res.status(400).json({ error: 'Query parameter required' });
        }

        // Clé API depuis les variables d'environnement Vercel
        const apiKey = process.env.PIXABAY_API_KEY;

        if (!apiKey) {
            return res.status(500).json({ error: 'API key not configured' });
        }

        // Appel à l'API Pixabay
        const pixabayUrl = `https://pixabay.com/api/?key=${apiKey}&q=${encodeURIComponent(query)}&image_type=${image_type}&per_page=${per_page}&safesearch=true&lang=${lang}`;

        const response = await fetch(pixabayUrl);
        const data = await response.json();

        return res.status(200).json(data);

    } catch (error) {
        console.error('Pixabay API error:', error);
        return res.status(500).json({ error: 'Internal server error' });
    }
}
