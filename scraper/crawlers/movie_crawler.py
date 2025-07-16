import re
import os
import time
from bs4 import BeautifulSoup
import urllib.request
import urllib.error
from tqdm import tqdm  # ✅ Importamos tqdm para barra de progreso


class MovieCrawler:
    def crawl(self, url):
        currentUrl = url
        pageNumber = 1

        # Extraer el nombre de la subcarpeta desde el parámetro "name"
        try:
            match = re.search(r"name=([^&]+)", url)
            subfolder = match.group(1) if match else "movie"
        except Exception as e:
            print(f"❌ Error extrayendo subcarpeta: {e}")
            subfolder = "movie"

        # Crear carpeta Download/subcarpeta
        base_folder = "Download"
        output_folder = os.path.join(base_folder, subfolder)
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

        print(f"📁 Imágenes se guardarán en: {output_folder}")

        while currentUrl:
            print(f"\n📄 Procesando página {pageNumber}...")

            try:
                request = urllib.request.Request(currentUrl, headers={
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:124.0) Gecko/20100101 Firefox/124.0'
                })
                page = urllib.request.urlopen(request)
                soup = BeautifulSoup(page, "html.parser")
            except Exception as e:
                print(f"❌ Error cargando o analizando página: {e}")
                break

            # Encontrar imágenes primero
            images = []
            for img in soup.find_all("img", src=True):
                imgSrc = img["src"]
                filename = os.path.basename(imgSrc)

                if filename.endswith((".jpg", ".jpeg", ".png")):
                    if "fancaps-movieimages" in imgSrc:
                        final_url = imgSrc
                    else:
                        final_url = f"https://cdni.fancaps.net/file/fancaps-movieimages/{filename}"

                    local_path = os.path.join(output_folder, filename)
                    if not os.path.exists(local_path):
                        images.append((final_url, local_path))

            # Mostrar barra de progreso por todas las imágenes de esta página
            for final_url, local_path in tqdm(images, desc=f"⬇️ Descargando imágenes", unit="img"):
                try:
                    req = urllib.request.Request(final_url, headers={
                        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:124.0) Gecko/20100101 Firefox/124.0',
                        'Referer': url
                    })
                    with urllib.request.urlopen(req) as response, open(local_path, 'wb') as out_file:
                        out_file.write(response.read())
                    time.sleep(0.3)
                except Exception:
                    pass  # Silenciar errores de descarga

            # Buscar la siguiente página
            
            nextPage = soup.find("a", href=lambda href: href and f"&page={pageNumber + 1}" in href)
            if nextPage:
                pageNumber += 1
                currentUrl = f"{url}&page={pageNumber}"
                time.sleep(1)  # Pausa entre páginas
            else:
                currentUrl = None

        print("\n✅ Descarga completada.")
