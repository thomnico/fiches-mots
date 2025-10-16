/**
 * Configuration globale de l'application
 */

const CONFIG = {
    // Traductions français -> anglais pour la recherche
    wordTranslations: {
        'feuille': 'leaf',
        'champignon': 'mushroom',
        'citrouille': 'pumpkin',
        'marron': 'chestnut',
        'arbre': 'tree',
        'pomme': 'apple',
        'chat': 'cat',
        'chien': 'dog',
        'oiseau': 'bird',
        'poisson': 'fish',
        'vache': 'cow',
        'mouton': 'sheep',
        'lapin': 'rabbit',
        'souris': 'mouse',
        'sapin': 'christmas tree',
        'cadeau': 'gift',
        'étoile': 'star',
        'neige': 'snow',
        'soleil': 'sun',
        'lune': 'moon',
        'nuage': 'cloud',
        'pluie': 'rain'
    },

    // Traductions de thèmes
    themeTranslations: {
        'automne': 'autumn fall',
        'printemps': 'spring',
        'été': 'summer',
        'hiver': 'winter',
        'animaux': 'animals',
        'noel': 'christmas',
        'noël': 'christmas',
        'fruits': 'fruits',
        'légumes': 'vegetables',
        'couleurs': 'colors'
    },

    // Configuration PDF (en points, 1 cm = 28.35 points)
    pdf: {
        pageWidth: 595.28,  // A4 width in points
        pageHeight: 841.89, // A4 height in points
        margin: 56.7,       // 2cm in points
        fontSize: {
            capital: 32,
            script: 36,     // +30% (28 * 1.3 ≈ 36)
            cursive: 64     // +100% (32 * 2 = 64)
        },
        imageMaxHeight: 141.75, // 5cm
        imageMaxWidth: 198.45,  // 7cm
        spacing: 56.70          // 2cm (espacement entre image et texte)
    },

    // Nombre d'images à proposer par mot
    imagesPerWord: 3,

    // APIs et moteurs de recherche
    searchEngines: {
        google: {
            enabled: true,
            priority: 1
        }
    }
};

// Fonction utilitaire pour traduire un mot
function translateWord(word) {
    return CONFIG.wordTranslations[word.toLowerCase()] || word;
}

// Fonction utilitaire pour traduire un thème
function translateTheme(theme) {
    return CONFIG.themeTranslations[theme.toLowerCase()] || theme;
}
