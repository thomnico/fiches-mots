#!/usr/bin/env python3
"""
Serveur proxy simple pour contourner les restrictions CORS
Permet à l'interface web d'utiliser la même logique de recherche que le script Python
"""

from http.server import HTTPServer, SimpleHTTPRequestHandler
import json
import re
import requests
from urllib.parse import urlparse, parse_qs, unquote
import sys

class CORSRequestHandler(SimpleHTTPRequestHandler):
    """Handler HTTP avec support CORS et proxy pour recherche d'images"""

    def end_headers(self):
        """Ajoute les headers CORS à toutes les réponses"""
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        super().end_headers()

    def do_OPTIONS(self):
        """Gère les requêtes OPTIONS (pre-flight CORS)"""
        self.send_response(200)
        self.end_headers()

    def do_GET(self):
        """Gère les requêtes GET"""
        parsed_path = urlparse(self.path)

        # Route /api/search-images pour la recherche d'images
        if parsed_path.path == '/api/search-images':
            self.handle_image_search(parsed_path)
        else:
            # Servir les fichiers statiques normalement
            super().do_GET()

    def handle_image_search(self, parsed_path):
        """Recherche d'images via Google (comme dans generate_fiches.py)"""
        try:
            # Parser les paramètres de requête
            params = parse_qs(parsed_path.query)
            word = params.get('word', [''])[0]
            theme = params.get('theme', [''])[0]
            count = int(params.get('count', ['3'])[0])

            if not word:
                self.send_error(400, "Missing 'word' parameter")
                return

            print(f"🔍 Recherche d'images pour: {word} (thème: {theme or 'aucun'})")

            # Traductions (comme dans le script Python)
            word_translations = {
                'feuille': 'leaf', 'champignon': 'mushroom', 'citrouille': 'pumpkin',
                'marron': 'chestnut', 'arbre': 'tree', 'pomme': 'apple',
                'chat': 'cat', 'chien': 'dog', 'oiseau': 'bird',
                'poisson': 'fish', 'vache': 'cow', 'mouton': 'sheep',
                'lapin': 'rabbit', 'souris': 'mouse', 'sapin': 'christmas tree',
                'cadeau': 'gift', 'étoile': 'star', 'neige': 'snow'
            }
            english_word = word_translations.get(word.lower(), word)

            # Recherche Google Images avec Freepik prioritaire
            images = self.search_google_images(english_word, theme, count)

            # Retourner les résultats en JSON
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()

            response_data = {
                'success': True,
                'word': word,
                'theme': theme,
                'images': images,
                'count': len(images)
            }
            self.wfile.write(json.dumps(response_data).encode())

            print(f"✅ {len(images)} images trouvées pour '{word}'")

        except Exception as e:
            print(f"❌ Erreur: {e}")
            self.send_response(500)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            error_data = {
                'success': False,
                'error': str(e)
            }
            self.wfile.write(json.dumps(error_data).encode())

    def search_google_images(self, word, theme, count=3):
        """Recherche d'images Google (identique au script Python)"""
        try:
            # Headers pour simuler un navigateur
            headers = {
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.5',
            }

            # Construire les requêtes de recherche
            search_queries = []
            if theme:
                search_queries.append(f"site:freepik.com {word} {theme} sticker icon")
                search_queries.append(f"{word} {theme} clipart cartoon sticker")
            else:
                search_queries.append(f"site:freepik.com {word} sticker icon")
                search_queries.append(f"{word} clipart cartoon sticker")

            all_images = []

            for search_query in search_queries:
                if len(all_images) >= count:
                    break

                # URL Google Images
                from urllib.parse import quote
                search_url = f"https://www.google.com/search?tbm=isch&q={quote(search_query)}"

                response = requests.get(search_url, headers=headers, timeout=15)
                response.raise_for_status()

                # Extraire les URLs d'images
                matches = re.findall(r'\["(https?://[^"]+\.(jpg|jpeg|png|gif|webp))"', response.text)

                # Prioriser Freepik/Flaticon
                for match in matches:
                    img_url = match[0]
                    if any(domain in img_url for domain in ['freepik.com', 'flaticon.com', 'cdnpk.net']):
                        if 'favicon' not in img_url and 'error-image' not in img_url:
                            if img_url not in all_images:
                                all_images.append(img_url)
                                if len(all_images) >= count:
                                    break

                # Ajouter d'autres images si pas assez
                if len(all_images) < count:
                    for match in matches:
                        img_url = match[0]
                        if img_url not in all_images:
                            all_images.append(img_url)
                            if len(all_images) >= count:
                                break

            return all_images[:count]

        except Exception as e:
            print(f"⚠️  Erreur recherche Google: {e}")
            return []

def run_server(port=8000):
    """Démarre le serveur proxy"""
    server_address = ('', port)
    httpd = HTTPServer(server_address, CORSRequestHandler)

    print("=" * 60)
    print("🚀 Serveur proxy démarré")
    print(f"🌐 URL: http://localhost:{port}")
    print("📡 API: http://localhost:{port}/api/search-images?word=chat&theme=animaux")
    print("=" * 60)
    print("\nAppuyez sur Ctrl+C pour arrêter le serveur")
    print()

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n\n🔒 Serveur arrêté")
        httpd.shutdown()

if __name__ == '__main__':
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8000
    run_server(port)
