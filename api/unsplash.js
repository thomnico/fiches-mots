/**
 * Fonction serverless Vercel pour Unsplash
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
        const { query, per_page = 20, orientation = 'landscape' } = req.query;

        if (!query) {
            return res.status(400).json({ error: 'Query parameter required' });
        }

        // Clé API depuis les variables d'environnement Vercel
        const accessKey = process.env.UNSPLASH_ACCESS_KEY;

        if (!accessKey) {
            return res.status(500).json({ error: 'API key not configured' });
        }

        // Appel à l'API Unsplash
        const unsplashUrl = `https://api.unsplash.com/search/photos?query=${encodeURIComponent(query)}&per_page=${per_page}&orientation=${orientation}&content_filter=high`;

        const response = await fetch(unsplashUrl, {
            headers: {
                'Authorization': `Client-ID ${accessKey}`
            }
        });

        const data = await response.json();

        return res.status(200).json(data);

    } catch (error) {
        console.error('Unsplash API error:', error);
        return res.status(500).json({ error: 'Internal server error' });
    }
}
