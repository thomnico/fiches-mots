#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Générateur de fiches pédagogiques pour la maternelle française - Version 2.
Utilise Pixabay et Unsplash comme la version web JavaScript.
Aligné sur le rendu JavaScript avec les mêmes tailles de police.
"""

import os
import sys
import requests
from io import BytesIO
from urllib.parse import quote
import time

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from PIL import Image


class ImageSearcher:
    """Recherche d'images via Pixabay et Unsplash APIs."""

    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'FichesMots/2.0 (Educational Purpose)'
        })

        # Charger les clés API depuis les variables d'environnement
        self.pixabay_api_key = os.getenv('PIXABAY_API_KEY', '52789824-40fb09218b750e39916fccc44')
        self.unsplash_access_key = os.getenv('UNSPLASH_ACCESS_KEY', 'J52y_IWplzV6Wz6IsHpAr_TSkHEUTdQd8nvejL4X4PU')

        print(f"🔑 Pixabay API: {'✅' if self.pixabay_api_key else '❌'}")
        print(f"🔑 Unsplash API: {'✅' if self.unsplash_access_key else '❌'}")

    def search_pixabay(self, word, theme=None, per_page=20):
        """
        Recherche des images sur Pixabay (priorité aux vecteurs).
        Retourne une liste d'URLs d'images.
        """
        try:
            # Gestion des mots ambigus (comme dans JS)
            search_word = word
            if word.lower() == 'marron' and theme and theme.lower() == 'automne':
                search_word = 'châtaigne marron'
                print(f"🌰 Mot ambigu détecté: marron → châtaigne marron")

            # 1. Recherche du mot SEUL (plus de variété)
            url = f"https://pixabay.com/api/?key={self.pixabay_api_key}&q={quote(search_word)}&image_type=vector&per_page={per_page}&safesearch=true&lang=fr"

            response = self.session.get(url, timeout=15)
            response.raise_for_status()
            data = response.json()

            images = [hit['webformatURL'] for hit in data.get('hits', [])]

            if images:
                print(f"   ✅ Pixabay vecteurs: {len(images)} images trouvées")
                return images

            # 2. Fallback: avec thème
            if theme and len(images) < 3:
                url = f"https://pixabay.com/api/?key={self.pixabay_api_key}&q={quote(word + ' ' + theme)}&image_type=vector&per_page={per_page}&safesearch=true&lang=fr"
                response = self.session.get(url, timeout=15)
                response.raise_for_status()
                data = response.json()

                themed_images = [hit['webformatURL'] for hit in data.get('hits', [])]
                images.extend(themed_images)

                if themed_images:
                    print(f"   ✅ Pixabay avec thème: {len(themed_images)} images supplémentaires")

            # 3. Fallback: illustrations
            if len(images) < 3:
                url = f"https://pixabay.com/api/?key={self.pixabay_api_key}&q={quote(search_word)}&image_type=illustration&per_page={per_page}&safesearch=true&lang=fr"
                response = self.session.get(url, timeout=15)
                response.raise_for_status()
                data = response.json()

                illust_images = [hit['webformatURL'] for hit in data.get('hits', [])]
                images.extend(illust_images)

                if illust_images:
                    print(f"   ✅ Pixabay illustrations: {len(illust_images)} images supplémentaires")

            # Dédupliquer
            images = list(dict.fromkeys(images))
            return images

        except Exception as e:
            print(f"   ⚠️  Erreur Pixabay: {e}")
            return []

    def search_unsplash(self, word, theme=None, per_page=20):
        """
        Recherche des photos sur Unsplash.
        Retourne une liste d'URLs d'images.
        """
        try:
            # Recherche avec contexte enfantin
            query = f"{word} {theme} livre enfants illustration" if theme else f"{word} livre enfants illustration"

            url = f"https://api.unsplash.com/search/photos?query={quote(query)}&per_page={per_page}&orientation=landscape&content_filter=high"

            headers = {
                'Authorization': f'Client-ID {self.unsplash_access_key}'
            }

            response = self.session.get(url, headers=headers, timeout=15)
            response.raise_for_status()
            data = response.json()

            images = [result['urls']['regular'] for result in data.get('results', [])]

            if images:
                print(f"   ✅ Unsplash: {len(images)} photos trouvées")
                return images

            # Fallback: recherche simple
            if len(images) < 3:
                query = f"{word} {theme}" if theme else word
                url = f"https://api.unsplash.com/search/photos?query={quote(query)}&per_page={per_page}&orientation=landscape&content_filter=high"

                response = self.session.get(url, headers=headers, timeout=15)
                response.raise_for_status()
                data = response.json()

                fallback_images = [result['urls']['regular'] for result in data.get('results', [])]
                images.extend(fallback_images)

                if fallback_images:
                    print(f"   ✅ Unsplash fallback: {len(fallback_images)} photos supplémentaires")

            return images

        except Exception as e:
            print(f"   ⚠️  Erreur Unsplash: {e}")
            return []

    def search_images(self, word, theme=None):
        """
        Recherche des images pour un mot.
        Priorité: Pixabay (vecteurs) puis Unsplash (photos).
        Retourne une liste d'URLs.
        """
        print(f"🔍 Recherche d'images pour: {word}")

        # 1. Essayer Pixabay en priorité
        images = self.search_pixabay(word, theme)

        if len(images) >= 3:
            return images

        # 2. Compléter avec Unsplash si pas assez d'images
        print(f"   ⚠️  Pas assez d'images Pixabay, essai Unsplash...")
        unsplash_images = self.search_unsplash(word, theme)
        images.extend(unsplash_images)

        # Dédupliquer
        images = list(dict.fromkeys(images))

        return images

    def download_image(self, url):
        """
        Télécharge une image depuis une URL et retourne un objet Image PIL.
        """
        try:
            response = self.session.get(url, timeout=15)
            response.raise_for_status()

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
            print(f"   ❌ Erreur téléchargement: {e}")
            return None


class FichePDFGenerator:
    """Générateur de fiches pédagogiques au format PDF - Aligné sur le rendu JavaScript."""

    def __init__(self, output_path="output/fiches.pdf"):
        self.output_path = output_path
        self.page_width, self.page_height = A4
        self.image_searcher = ImageSearcher()

        # Marges et dimensions (alignées sur JS)
        self.margin = 56.7  # 2cm en points
        self.word_height = (self.page_height - 2 * self.margin) / 2

        # Tailles de police alignées sur web/js/config.js
        self.font_size_capital = 32
        self.font_size_script = 36   # +30%
        self.font_size_cursive = 64  # +100%

    def setup_fonts(self):
        """Configure les polices pour les différents styles."""
        # Polices par défaut
        self.font_capital = "Helvetica-Bold"
        self.font_script = "Helvetica"
        self.font_cursive = "Times-Italic"

        # Chercher les polices personnalisées
        capital_path = None
        script_path = None
        cursive_path = None

        for ext in ['.ttf', '.otf']:
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
                print(f"⚠️  Erreur police capital: {e}")

        if script_path:
            try:
                pdfmetrics.registerFont(TTFont('Script', script_path))
                self.font_script = 'Script'
                print(f"✅ Police script chargée: {script_path}")
            except Exception as e:
                print(f"⚠️  Erreur police script: {e}")

        if cursive_path:
            try:
                pdfmetrics.registerFont(TTFont('Cursive', cursive_path))
                self.font_cursive = 'Cursive'
                print(f"✅ Police cursive chargée: {cursive_path}")
            except Exception as e:
                print(f"⚠️  Erreur police cursive: {e}")

    def draw_word_fiche(self, c, word, img, y_position):
        """
        Dessine une fiche pour un mot - Alignée sur le rendu JavaScript.
        """
        x_center = self.page_width / 2
        current_y = y_position - 1.5 * cm

        # 1. Image en haut (si disponible)
        if img:
            # Dimensions maximales (alignées sur JS: 7cm x 5cm)
            max_img_width = 198.45   # 7cm en points
            max_img_height = 141.75  # 5cm en points

            # Calculer les proportions
            aspect = img.width / img.height
            if aspect > max_img_width / max_img_height:
                width = max_img_width
                height = width / aspect
            else:
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

                # Bordure noire (2pt comme dans JS)
                c.setStrokeColorRGB(0, 0, 0)
                c.setLineWidth(2)
                c.rect(img_x - 5.67, img_y - 5.67, width + 11.34, height + 11.34, stroke=1, fill=0)

                c.drawImage(img_reader, img_x, img_y, width=width, height=height, preserveAspectRatio=True)
                current_y = img_y - 42.5  # spacing: 1.5cm = 42.5 points
            except Exception as e:
                print(f"⚠️  Erreur insertion image: {e}")
                current_y -= max_img_height + 42.5
        else:
            current_y -= 42.5

        # 2. Mot en CAPITALES (OpenDyslexic Bold, 32pt)
        c.setFont(self.font_capital, self.font_size_capital)
        c.setFillColorRGB(0, 0, 0)
        c.drawCentredString(x_center, current_y, word.upper())
        current_y -= 40  # Espacement aligné sur JS

        # 3. Mot en script (OpenDyslexic, 36pt)
        c.setFont(self.font_script, self.font_size_script)
        c.setFillColorRGB(0, 0, 0)
        c.drawCentredString(x_center, current_y, word.lower())
        current_y -= 48  # Espacement aligné sur JS

        # 4. Mot en cursif (Écolier, 64pt - TRÈS GRAND)
        c.setFont(self.font_cursive, self.font_size_cursive)
        c.setFillColorRGB(0, 0, 0)
        c.drawCentredString(x_center, current_y, word.lower())

    def generate(self, words, theme=None):
        """
        Génère le PDF avec toutes les fiches.
        """
        print(f"\n📄 Génération du PDF: {self.output_path}")
        print(f"📝 {len(words)} mots à traiter")
        if theme:
            print(f"🎨 Thème: {theme}\n")

        # Créer le dossier de sortie
        os.makedirs(os.path.dirname(self.output_path) or '.', exist_ok=True)

        # Initialiser le canvas
        c = canvas.Canvas(self.output_path, pagesize=A4)

        # Métadonnées PDF
        c.setTitle("Fiches Pédagogiques - Maternelle")
        c.setAuthor("Générateur Fiches-Mots v2")
        c.setSubject(f"Fiches éducatives - Thème: {theme or 'général'}")
        c.setKeywords("éducation, maternelle, dyslexie, accessibilité")

        self.setup_fonts()
        print()

        # Traiter les mots par paires (2 par page)
        for i in range(0, len(words), 2):
            page_words = words[i:i+2]
            print(f"--- Page {i//2 + 1} ---")

            for idx, word in enumerate(page_words):
                # Rechercher des images
                image_urls = self.image_searcher.search_images(word, theme)

                img = None
                if image_urls:
                    print(f"   ✅ {len(image_urls)} images disponibles, téléchargement de la première...")
                    img = self.image_searcher.download_image(image_urls[0])
                    if img:
                        print(f"   ✅ Image téléchargée avec succès")
                else:
                    print(f"   ⚠️  Aucune image trouvée")

                # Position Y (haut ou bas de page)
                y_pos = self.page_height - self.margin if idx == 0 else self.page_height / 2

                # Dessiner la fiche
                self.draw_word_fiche(c, word, img, y_pos)

                # Délai pour ne pas surcharger les APIs
                time.sleep(0.5)

            print()
            c.showPage()  # Nouvelle page

        # Sauvegarder le PDF
        c.save()
        print(f"✅ PDF généré avec succès: {self.output_path}\n")


def load_words_from_file(filepath):
    """Charge une liste de mots depuis un fichier texte."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            words = [line.strip() for line in f if line.strip()]
        return words
    except FileNotFoundError:
        print(f"❌ Fichier non trouvé: {filepath}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Erreur lecture fichier: {e}")
        sys.exit(1)


def detect_theme_from_filename(filepath):
    """Détecte le thème à partir du nom du fichier."""
    import re
    filename = os.path.basename(filepath)
    match = re.search(r'mots[_-]([^.]+)\.txt', filename)
    if match:
        return match.group(1)
    return None


def main():
    """Point d'entrée principal."""
    print("=" * 60)
    print("Générateur de Fiches Pédagogiques v2 (Pixabay + Unsplash)")
    print("=" * 60)

    # Charger la liste de mots
    words_file = "mots_automne.txt"
    if len(sys.argv) > 1:
        words_file = sys.argv[1]

    print(f"\n📖 Chargement: {words_file}")
    words = load_words_from_file(words_file)
    print(f"✅ {len(words)} mots: {', '.join(words)}")

    # Détecter le thème
    theme = detect_theme_from_filename(words_file)

    # Générer le PDF
    if len(sys.argv) > 2:
        output_file = sys.argv[2]
    else:
        theme_name = theme or 'maternelle'
        output_file = f"output/fiches_{theme_name}.pdf"

    generator = FichePDFGenerator(output_file)
    generator.generate(words, theme=theme)

    print("=" * 60)
    print("✅ Génération terminée!")
    print("=" * 60)


if __name__ == "__main__":
    main()
