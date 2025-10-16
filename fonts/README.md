# Polices utilisées

## OpenDyslexic (CAPITALS & Script)

- **Source** : [OpenDyslexic](https://opendyslexic.org/)
- **Auteur** : Abelardo Gonzalez
- **Licence** : Creative Commons Attribution 3.0 Unported
- **Type** : Police pour dyslexiques
- **Téléchargements** : Millions d'utilisateurs dans le monde

Cette police est spécifiquement conçue pour les personnes dyslexiques avec des lettres aux formes distinctes pour éviter la confusion.

## Écolier (Cursive)

- **Source** : [DaFont - Écolier](https://www.dafont.com/ecolier.font)
- **Auteur** : Jean-Marie Douteau
- **Licence** : Gratuit pour usage personnel
- **Type** : Police scolaire française cursive
- **Téléchargements** : Plus de 2 millions

Cette police cursive est la référence de l'écriture manuscrite française enseignée à l'école primaire.

## Fichiers installés

Le projet utilise un mix de polices optimisées pour l'apprentissage :

- `capital.ttf` - **OpenDyslexic-Bold** pour CAPITALES (dyslexie-friendly)
- `script.ttf` - **OpenDyslexic-Regular** pour script/minuscules (dyslexie-friendly)
- `cursive.ttf` - **Écolier** (ec_cour.TTF) pour cursif français

## Détection automatique

Le script `generate_fiches.py` détecte automatiquement les polices .ttf dans ce dossier et les utilise pour générer les fiches :
- Si les polices sont trouvées, elles sont chargées et utilisées
- Sinon, le script utilise les polices système par défaut

## Polices alternatives

Pour personnaliser davantage, vous pouvez remplacer les fichiers :
- `capital.ttf` - Police pour les CAPITALES
- `script.ttf` - Police pour le texte en minuscules
- `cursive.ttf` - Police cursive manuscrite
