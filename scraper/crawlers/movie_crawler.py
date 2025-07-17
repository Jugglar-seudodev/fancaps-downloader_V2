import re
import os
import time
from bs4 import BeautifulSoup
import urllib.request
import urllib.error
from tqdm import tqdm
import sys

class MovieCrawler:
    def crawl(self, url):
        currentUrl = url
        pageNumber = 1

        try:
            match = re.search(r"name=([^&]+)", url)
            subfolder = match.group(1) if match else "movie"
        except Exception as e:
            print(f"❌ Error extracting subfolder: {e}")
            subfolder = "movie"

        base_folder = "Download"
        output_folder = os.path.join(base_folder, subfolder)
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

        print(f"📁 Images will be saved to: {output_folder}")

        while True:
            all_images = []
            pages_processed = 0

            # Recolectar imágenes de las siguientes 10 páginas
            for i in range(10):
                print(f"🔎 Collecting from page {pageNumber}...")
                full_url = f"{url}&page={pageNumber}"
                try:
                    request = urllib.request.Request(full_url, headers={
                        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:124.0) Gecko/20100101 Firefox/124.0'
                    })
                    page = urllib.request.urlopen(request)
                    soup = BeautifulSoup(page, "html.parser")
                except Exception as e:
                    print(f"❌ Error loading page {pageNumber}: {e}")
                    return

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
                            all_images.append((final_url, local_path))

                nextPage = soup.find("a", href=lambda href: href and f"&page={pageNumber + 1}" in href)
                if not nextPage:
                    print("🚫 No more pages.")
                    break

                pageNumber += 1
                pages_processed += 1
                time.sleep(1)

            # Si no se encontraron imágenes, se termina
            if not all_images:
                print("⚠️ No more images to download.")
                break

            # Descargar todas las imágenes con una sola barra
            print(f"⬇️ Downloading {len(all_images)} images from {pages_processed} pages...")
            for final_url, local_path in tqdm(all_images, desc="📦 Downloading batch", unit="img"):
                try:
                    req = urllib.request.Request(final_url, headers={
                        'User-Agent': 'Mozilla/5.0',
                        'Referer': url
                    })
                    with urllib.request.urlopen(req) as response, open(local_path, 'wb') as out_file:
                        out_file.write(response.read())
                    time.sleep(0.3)
                except Exception:
                    pass

            if pages_processed < 10:
                break  # Ya no hay más bloques de 10 páginas

        print("\n✅ Download completed")
        sys.exit(0)