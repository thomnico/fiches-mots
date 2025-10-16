#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Générateur de fiches pédagogiques pour la maternelle française.
Crée des PDFs avec 2 mots par page, chaque mot illustré avec une image
et affiché en trois styles : CAPITALES, script, et cursif.
"""

import os
import sys
import requests
from bs4 import BeautifulSoup
from io import BytesIO
from urllib.parse import quote, unquote
import time

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from PIL import Image


class ImageSearcher:
    """Recherche d'images libres de droits sur PublicDomainVectors, OpenClipart et Freepik."""

    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'FichesMots/1.0 (Educational Purpose)'
        })

    def search_publicdomainvectors(self, word, theme=None):
        """
        Recherche une image sur PublicDomainVectors.org via scraping HTML.
        Vecteurs du domaine public, très simple à utiliser.
        Retourne l'URL de l'image SVG ou None.
        """
        try:
            import re

            # Construire la requête avec le thème et "sticker" si fourni
            if theme:
                search_query = f"{word} {theme} sticker"
            else:
                search_query = f"{word} sticker"

            # 1. Rechercher sur PublicDomainVectors
            search_url = f"https://publicdomainvectors.org/fr/search/{quote(search_query)}"
            response = self.session.get(search_url, timeout=15)
            response.raise_for_status()

            # 2. Extraire les liens vers les pages de détail
            detail_links = re.findall(r'href="(/fr/gratuitement-des-vecteurs/[^"]+)"', response.text)

            if not detail_links:
                return None

            # 3. Prendre le premier résultat
            detail_url = f"https://publicdomainvectors.org{detail_links[0]}"
            response = self.session.get(detail_url, timeout=15)
            response.raise_for_status()

            # 4. Extraire le lien de téléchargement SVG
            svg_match = re.search(r'href="(/download\.php\?file=[^"]+\.svg)"', response.text)

            if svg_match:
                svg_path = svg_match.group(1)
                svg_url = f"https://publicdomainvectors.org{svg_path}"
                return svg_url

            return None

        except Exception as e:
            print(f"⚠️  PublicDomainVectors: {e}")
            return None

    def search_openclipart(self, word, theme=None):
        """
        Recherche une image sur OpenClipart.org via scraping HTML et JSON-LD.
        Dessins vectoriels naïfs en domaine public (CC0).
        Retourne l'URL de l'image SVG ou None.
        """
        try:
            import re
            import json

            # Construire la requête avec le thème si fourni
            # Traduire quelques mots français courants en anglais pour OpenClipart
            word_translations = {
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
                'cadeau': 'gift present',
                'étoile': 'star',
                'neige': 'snow'
            }
            english_word = word_translations.get(word.lower(), word)
            # Ajouter "sticker cartoon" pour des images type sticker enfantines
            if theme:
                search_query = f"{english_word} {theme} sticker cartoon"
            else:
                search_query = f"{english_word} sticker cartoon"

            # 1. Rechercher sur OpenClipart
            search_url = f"https://openclipart.org/search/?query={quote(search_query)}"
            response = self.session.get(search_url, timeout=15)
            response.raise_for_status()

            # 2. Extraire les liens vers les pages de détail
            detail_links = re.findall(r'href="(/detail/\d+/[^"]+)"', response.text)

            if not detail_links:
                return None

            # 3. Prendre le premier résultat
            detail_url = f"https://openclipart.org{detail_links[0]}"
            response = self.session.get(detail_url, timeout=15)
            response.raise_for_status()

            # 4. Extraire le JSON-LD pour obtenir l'URL de l'image
            match = re.search(r'<script type="application/ld\+json">(.*?)</script>',
                            response.text, re.DOTALL)

            if match:
                data = json.loads(match.group(1))
                if 'image' in data and 'url' in data['image']:
                    svg_url = data['image']['url']

                    # Retourner directement le SVG (sera converti en PNG par PIL+cairosvg si installé)
                    # Ou fallback sur Wikimedia si le téléchargement échoue
                    return svg_url

            return None

        except Exception as e:
            print(f"⚠️  OpenClipart: {e}")
            return None

    def search_google_images(self, word, theme=None):
        """
        Recherche une image via Google Images en priorisant Freepik stickers.
        Utilise site:freepik.com pour trouver des stickers adaptés aux enfants.
        Retourne l'URL de l'image ou None.
        """
        try:
            import re

            # Traduire les mots français en anglais
            word_translations = {
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
                'neige': 'snow'
            }
            english_word = word_translations.get(word.lower(), word)

            # Headers pour simuler un navigateur
            headers = {
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.5',
                'Accept-Encoding': 'gzip, deflate',
                'Connection': 'keep-alive',
                'Upgrade-Insecure-Requests': '1'
            }

            # Essayer d'abord avec Freepik via Google
            search_queries = []
            if theme:
                search_queries.append(f"site:freepik.com {english_word} {theme} sticker icon")
                search_queries.append(f"{english_word} {theme} clipart cartoon sticker")
            else:
                search_queries.append(f"site:freepik.com {english_word} sticker icon")
                search_queries.append(f"{english_word} clipart cartoon sticker")

            for search_query in search_queries:
                # URL de recherche Google Images
                search_url = f"https://www.google.com/search?tbm=isch&q={quote(search_query)}"

                response = self.session.get(search_url, headers=headers, timeout=15)
                response.raise_for_status()

                # Extraire les URLs d'images depuis les données JavaScript
                # Google stocke les métadonnées images dans des structures JS
                matches = re.findall(r'\["(https?://[^"]+\.(jpg|jpeg|png|gif|webp))"', response.text)

                if matches:
                    # Prioriser les images Freepik/Flaticon
                    for match in matches:
                        img_url = match[0]
                        if any(domain in img_url for domain in ['freepik.com', 'flaticon.com', 'cdnpk.net']):
                            if img_url.startswith('http') and 'favicon' not in img_url and 'error-image' not in img_url:
                                return img_url

                    # Sinon prendre la première image disponible
                    img_url = matches[0][0]
                    if img_url.startswith('http'):
                        return img_url

                # Pause entre requêtes pour ne pas être bloqué
                time.sleep(0.5)

            return None

        except Exception as e:
            print(f"⚠️  Google Images: {e}")
            return None

    def download_image(self, url):
        """
        Télécharge une image depuis une URL et retourne un objet Image PIL.
        Support SVG via conversion PNG avec cairosvg si disponible.
        """
        try:
            response = self.session.get(url, timeout=15)
            response.raise_for_status()

            # Si c'est un SVG, essayer de le convertir en PNG
            if url.lower().endswith('.svg') or 'svg' in response.headers.get('content-type', ''):
                try:
                    import cairosvg
                    # Convertir SVG en PNG
                    png_data = cairosvg.svg2png(bytestring=response.content)
                    img = Image.open(BytesIO(png_data))
                except ImportError:
                    print(f"⚠️  cairosvg non installé, impossible de convertir le SVG")
                    return None
                except Exception as svg_error:
                    print(f"⚠️  Erreur conversion SVG: {svg_error}")
                    return None
            else:
                img = Image.open(BytesIO(response.content))

            # Convertir en RGB si nécessaire
            if img.mode in ('RGBA', 'LA', 'P'):
                background = Image.new('RGB', img.size, (255, 255, 255))
                if img.mode == 'P':
                    img = img.convert('RGBA')
                background.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
                img = background
            elif img.mode != 'RGB':
                img = img.convert('RGB')

            return img

        except Exception as e:
            print(f"❌ Erreur lors du téléchargement de l'image: {e}")
            return None


class FichePDFGenerator:
    """Générateur de fiches pédagogiques au format PDF."""

    def __init__(self, output_path="output/fiches.pdf"):
        self.output_path = output_path
        self.page_width, self.page_height = A4
        self.image_searcher = ImageSearcher()

        # Marges et dimensions
        self.margin = 2 * cm
        self.word_height = (self.page_height - 2 * self.margin) / 2

    def setup_fonts(self):
        """Configure les polices pour les différents styles."""
        # Note: Utilisation des polices système par défaut
        # Pour une version complète, ajouter des polices dans le dossier fonts/
        self.font_capital = "Helvetica-Bold"
        self.font_script = "Helvetica"
        self.font_cursive = "Times-Italic"

        # Si des polices personnalisées existent (support .ttf et .otf)
        capital_path = None
        script_path = None
        cursive_path = None

        # Chercher les polices (priorité .otf puis .ttf)
        for ext in ['.otf', '.ttf']:
            if not capital_path and os.path.exists(f"fonts/capital{ext}"):
                capital_path = f"fonts/capital{ext}"
            if not script_path and os.path.exists(f"fonts/script{ext}"):
                script_path = f"fonts/script{ext}"
            if not cursive_path and os.path.exists(f"fonts/cursive{ext}"):
                cursive_path = f"fonts/cursive{ext}"

        # Enregistrer les polices trouvées
        if capital_path:
            try:
                pdfmetrics.registerFont(TTFont('Capital', capital_path))
                self.font_capital = 'Capital'
                print(f"✅ Police CAPITALES chargée: {capital_path}")
            except Exception as e:
                print(f"⚠️  Erreur chargement police capital: {e}")

        if script_path:
            try:
                pdfmetrics.registerFont(TTFont('Script', script_path))
                self.font_script = 'Script'
                print(f"✅ Police script chargée: {script_path}")
            except Exception as e:
                print(f"⚠️  Erreur chargement police script: {e}")

        if cursive_path:
            try:
                pdfmetrics.registerFont(TTFont('Cursive', cursive_path))
                self.font_cursive = 'Cursive'
                print(f"✅ Police cursive chargée: {cursive_path}")
            except Exception as e:
                print(f"⚠️  Erreur chargement police cursive: {e}")

    def draw_word_fiche(self, c, word, img, y_position):
        """
        Dessine une fiche pour un mot à une position Y donnée.

        Args:
            c: Canvas ReportLab
            word: Le mot à afficher
            img: Image PIL ou None
            y_position: Position Y de départ (haut de la fiche)
        """
        x_center = self.page_width / 2
        current_y = y_position - 1.5 * cm

        # 1. Image en haut (si disponible)
        if img:
            # Dimensions maximales pour l'image (réduites pour éviter chevauchement)
            max_img_height = 5 * cm
            max_img_width = 7 * cm

            # Calculer les proportions
            aspect = img.width / img.height
            if aspect > max_img_width / max_img_height:
                # Image plus large
                width = max_img_width
                height = width / aspect
            else:
                # Image plus haute
                height = max_img_height
                width = height * aspect

            img_x = x_center - width / 2
            img_y = current_y - height

            try:
                # Convertir PIL Image en ImageReader
                img_buffer = BytesIO()
                img.save(img_buffer, format='PNG')
                img_buffer.seek(0)
                img_reader = ImageReader(img_buffer)

                # Bordure pour meilleure délimitation (accessibilité visuelle)
                c.setStrokeColorRGB(0, 0, 0)
                c.setLineWidth(2)
                c.rect(img_x - 0.2*cm, img_y - 0.2*cm, width + 0.4*cm, height + 0.4*cm, stroke=1, fill=0)

                c.drawImage(img_reader, img_x, img_y, width=width, height=height, preserveAspectRatio=True)
                current_y = img_y - 1.5 * cm  # Espace augmenté entre image et texte
            except Exception as e:
                print(f"⚠️  Erreur lors de l'insertion de l'image: {e}")
                current_y -= max_img_height + 1.0 * cm
        else:
            current_y -= 0.5 * cm  # Moins d'espace si pas d'image

        # 2. Mot en CAPITALES (OpenDyslexic Bold)
        # Taille augmentée pour accessibilité
        c.setFont(self.font_capital, 32)
        # Noir pur pour contraste maximal (WCAG AAA)
        c.setFillColorRGB(0, 0, 0)
        c.drawCentredString(x_center, current_y, word.upper())
        current_y -= 1.2 * cm

        # 3. Mot en script (OpenDyslexic Regular)
        # Taille augmentée pour accessibilité
        c.setFont(self.font_script, 28)
        c.setFillColorRGB(0, 0, 0)
        c.drawCentredString(x_center, current_y, word.lower())
        current_y -= 1.2 * cm

        # 4. Mot en cursif (Écolier)
        # Taille augmentée significativement pour meilleure lisibilité
        c.setFont(self.font_cursive, 32)
        c.setFillColorRGB(0, 0, 0)
        c.drawCentredString(x_center, current_y, word.lower())

    def generate(self, words, theme=None):
        """
        Génère le PDF avec toutes les fiches.

        Args:
            words: Liste de mots à inclure dans le PDF
            theme: Thème optionnel pour contextualiser la recherche d'images
        """
        print(f"📄 Génération du PDF: {self.output_path}")
        print(f"📝 {len(words)} mots à traiter")
        if theme:
            print(f"🎨 Thème détecté: {theme}")
        print()

        # Créer le dossier de sortie si nécessaire
        os.makedirs(os.path.dirname(self.output_path) or '.', exist_ok=True)

        # Initialiser le canvas
        c = canvas.Canvas(self.output_path, pagesize=A4)

        # Métadonnées PDF pour accessibilité
        c.setTitle("Fiches Pédagogiques - Maternelle")
        c.setAuthor("Générateur Fiches-Mots")
        c.setSubject(f"Fiches éducatives avec {len(words)} mots")
        c.setKeywords("éducation, maternelle, dyslexie, accessibilité, apprentissage")

        self.setup_fonts()

        # Traiter les mots par paires (2 par page)
        for i in range(0, len(words), 2):
            page_words = words[i:i+2]

            print(f"--- Page {i//2 + 1} ---")

            for idx, word in enumerate(page_words):
                print(f"🔍 Recherche d'image pour: {word}")

                # Rechercher l'image - priorité aux vecteurs du domaine public
                img_url = None
                img = None

                # 1. PRIORITÉ: PublicDomainVectors (simple et fiable)
                print(f"   🎨 Recherche sur PublicDomainVectors...")
                img_url = self.image_searcher.search_publicdomainvectors(word, theme)

                # 2. Fallback: OpenClipart
                if not img_url:
                    print(f"   🖼️  Recherche sur OpenClipart...")
                    img_url = self.image_searcher.search_openclipart(word, theme)

                # 3. Fallback: Google Images
                if not img_url:
                    print(f"   🔍 Recherche sur Google Images...")
                    img_url = self.image_searcher.search_google_images(word, theme)

                if img_url:
                    print(f"✅ Image trouvée: {img_url}")
                    img = self.image_searcher.download_image(img_url)
                    if img:
                        print(f"✅ Image téléchargée avec succès")
                    time.sleep(1)  # Délai pour ne pas surcharger le serveur

                # Position Y (haut ou bas de page)
                y_pos = self.page_height - self.margin if idx == 0 else self.page_height / 2

                # Dessiner la fiche
                self.draw_word_fiche(c, word, img, y_pos)

                # Ligne de séparation entre les deux mots
                if idx == 0 and len(page_words) > 1:
                    c.setStrokeColorRGB(0.8, 0.8, 0.8)
                    c.setLineWidth(0.5)
                    c.line(self.margin, self.page_height / 2,
                          self.page_width - self.margin, self.page_height / 2)

            print()
            c.showPage()  # Nouvelle page

        # Sauvegarder le PDF
        c.save()
        print(f"✅ PDF généré avec succès: {self.output_path}")


def load_words_from_file(filepath):
    """Charge une liste de mots depuis un fichier texte (un mot par ligne)."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            words = [line.strip() for line in f if line.strip()]
        return words
    except FileNotFoundError:
        print(f"❌ Fichier non trouvé: {filepath}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Erreur lors de la lecture du fichier: {e}")
        sys.exit(1)


def detect_theme_from_filename(filepath):
    """
    Détecte le thème à partir du nom du fichier.
    Ex: mots_automne.txt → automne
        mots_animaux.txt → animaux
    """
    import re
    filename = os.path.basename(filepath)
    # Chercher le pattern mots_THEME.txt
    match = re.search(r'mots[_-]([^.]+)\.txt', filename)
    if match:
        theme = match.group(1)
        # Traduire quelques thèmes courants
        translations = {
            'automne': 'autumn fall',
            'printemps': 'spring',
            'ete': 'summer',
            'hiver': 'winter',
            'animaux': 'animals',
            'noel': 'christmas',
            'paques': 'easter'
        }
        return translations.get(theme, theme)
    return None


def main():
    """Point d'entrée principal du script."""
    print("=" * 60)
    print("Générateur de Fiches Pédagogiques pour la Maternelle")
    print("=" * 60)
    print()

    # Charger la liste de mots
    words_file = "mots_automne.txt"

    if len(sys.argv) > 1:
        words_file = sys.argv[1]

    print(f"📖 Chargement des mots depuis: {words_file}")
    words = load_words_from_file(words_file)
    print(f"✅ {len(words)} mots chargés: {', '.join(words)}")

    # Détecter le thème depuis le nom du fichier
    theme = detect_theme_from_filename(words_file)
    if theme:
        print(f"🎨 Thème détecté: {theme}")
    print()

    # Générer le PDF avec le nom du thème
    if len(sys.argv) > 2:
        output_file = sys.argv[2]
    else:
        # Construire le nom du fichier avec le thème
        if theme:
            theme_name = os.path.basename(words_file).replace('mots_', '').replace('.txt', '')
            output_file = f"output/fiches_{theme_name}.pdf"
        else:
            output_file = "output/fiches_maternelle.pdf"

    generator = FichePDFGenerator(output_file)
    generator.generate(words, theme=theme)

    print()
    print("=" * 60)
    print("✅ Génération terminée!")
    print("=" * 60)


if __name__ == "__main__":
    main()
