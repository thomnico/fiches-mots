# Guide des Thèmes

Le générateur de fiches détecte automatiquement le thème depuis le nom du fichier et l'utilise pour contextualiser la recherche d'images.

## Format du Nom de Fichier

Le fichier doit suivre le pattern : `mots_THEME.txt`

Exemple : `mots_automne.txt`, `mots_animaux.txt`, `mots_noel.txt`

## Thèmes Testés avec Succès ✅

### 🍂 Automne (`mots_automne.txt`)
```
feuille
champignon
citrouille
marron
```
**Résultat** : Images de feuilles d'arbres, champignons, citrouilles d'Halloween, châtaignes d'automne

### 🐾 Animaux (`mots_animaux.txt`)
```
chat
chien
oiseau
poisson
```
**Résultat** : Dessins d'animaux contextuel (chat portrait, chien, oiseau coloré, poisson)

### 🎄 Noël (`mots_noel.txt`)
```
sapin
cadeau
étoile
neige
```
**Résultat** : Sapin de Noël, cadeaux, étoiles, scène de neige

## Thèmes Prédéfinis

Le script traduit automatiquement ces thèmes en anglais pour une meilleure recherche :

| Nom du fichier | Thème détecté | Recherche en anglais |
|----------------|---------------|----------------------|
| `mots_automne.txt` | automne | "autumn fall" |
| `mots_printemps.txt` | printemps | "spring" |
| `mots_ete.txt` | été | "summer" |
| `mots_hiver.txt` | hiver | "winter" |
| `mots_animaux.txt` | animaux | "animals" |
| `mots_noel.txt` | noël | "christmas" |
| `mots_paques.txt` | pâques | "easter" |

## Traductions de Mots Intégrées

Le script traduit automatiquement les mots français courants en anglais pour OpenClipart :

### Saisons & Nature
- feuille → leaf
- champignon → mushroom
- citrouille → pumpkin
- marron → chestnut
- arbre → tree
- pomme → apple

### Animaux
- chat → cat
- chien → dog
- oiseau → bird
- poisson → fish
- vache → cow
- mouton → sheep
- lapin → rabbit
- souris → mouse

### Noël
- sapin → christmas tree
- cadeau → gift present
- étoile → star
- neige → snow

## Créer un Nouveau Thème

### Étape 1 : Créer le fichier de mots
Créez un fichier `mots_VOTRE_THEME.txt` avec vos mots (un par ligne).

### Étape 2 : Ajouter la traduction du thème (optionnel)
Si vous voulez une traduction spécifique du thème, modifiez le fichier `generate_fiches.py` dans la fonction `detect_theme_from_filename()` :

```python
translations = {
    'automne': 'autumn fall',
    'printemps': 'spring',
    # Ajoutez votre thème ici
    'votre_theme': 'your theme english'
}
```

### Étape 3 : Ajouter des traductions de mots (optionnel)
Pour améliorer la recherche d'images, ajoutez vos traductions dans `search_openclipart()` :

```python
word_translations = {
    'feuille': 'leaf',
    # Ajoutez vos mots ici
    'votre_mot': 'your word'
}
```

### Étape 4 : Générer le PDF
```bash
python generate_fiches.py mots_votre_theme.txt output/fiches_votre_theme.pdf
```

## Exemples d'Autres Thèmes Possibles

### 🍎 Fruits
```
# mots_fruits.txt
pomme
banane
orange
raisin
```

### 🏫 École
```
# mots_ecole.txt
crayon
cahier
livre
tableau
```

### 🏠 Maison
```
# mots_maison.txt
table
chaise
lit
fenêtre
```

### 🎨 Couleurs
```
# mots_couleurs.txt
rouge
bleu
jaune
vert
```

### 🚗 Transports
```
# mots_transports.txt
voiture
vélo
train
avion
```

## Comment Fonctionnent les Thèmes

1. **Détection automatique** : Le script lit le nom du fichier et extrait le thème
2. **Traduction** : Le thème est traduit en anglais si une traduction existe
3. **Recherche contextuelle** : Chaque mot est recherché avec le thème :
   - `feuille + autumn fall` → trouve des feuilles d'automne
   - `chat + animals` → trouve des dessins d'animaux
4. **Sources multiples** : PublicDomainVectors → OpenClipart → Wikimedia Commons
5. **Images pertinentes** : Le contexte améliore significativement la pertinence des résultats

## Résultats

Les thèmes permettent d'obtenir des images **beaucoup plus pertinentes** :

❌ Sans thème : "feuille" → page de cahier, feuille de papier
✅ Avec thème "automne" : "feuille" → feuille d'arbre en automne 🍂

❌ Sans thème : "étoile" → toutes sortes d'étoiles
✅ Avec thème "noël" : "étoile" → étoile de Noël ⭐

## Conseils

- ✅ **Nommez toujours** vos fichiers avec le pattern `mots_THEME.txt`
- ✅ **Utilisez des thèmes cohérents** pour tous les mots d'une liste
- ✅ **Testez votre thème** avant de générer beaucoup de fiches
- ✅ **Ajoutez des traductions** pour des mots spécialisés

---

**Note** : Le système de thèmes est extensible. N'hésitez pas à ajouter vos propres traductions et thèmes dans le code source !
