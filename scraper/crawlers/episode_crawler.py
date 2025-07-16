import re
from bs4 import BeautifulSoup
import urllib.request
import urllib.error
import os

class EpisodeCrawler:
    def crawl(self, url):
        picLinks = []  # Lista de enlaces de imágenes
        currentUrl = url
        pageNumber = 1

        # Analiza la URL
        match = re.search(r"https://fancaps.net/([a-zA-Z]+)/.*\?(\d+)-(.*?)/(.*)", url)
        if not match:
            print("Invalid URL format.")
            return {"subfolder": "", "links": []}

        epType = match.group(1)
        series_name = match.group(3).replace(" ", "_")
        episode_name = match.group(4).replace(" ", "_")
        subfolder = os.path.join(series_name, episode_name)

        while currentUrl:
            try:
                request = urllib.request.Request(
                    currentUrl,
                    headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:124.0) Gecko/20100101 Firefox/124.0'}
                )
                page = urllib.request.urlopen(request)
            except urllib.error.URLError as e:
                print(f"Error opening URL: {e.reason}")
                break
            except urllib.error.HTTPError as e:
                print(f"HTTP Error: {e.code} {e.reason}")
                break

            try:
                soup = BeautifulSoup(page, "html.parser")
            except Exception as e:
                print(f"Error parsing page: {e}")
                break

            # Captura todas las imágenes sin filtro específico
            for img in soup.find_all("img", src=True):
                imgSrc = img["src"]
                filename = imgSrc.split("/")[-1]
                if filename.endswith((".jpg", ".jpeg", ".png")):
                    picLinks.append(imgSrc)

            # Buscar paginación
            nextPage = soup.find("a", href=lambda href: href and f"&page={pageNumber + 1}" in href)
            if nextPage:
                pageNumber += 1
                currentUrl = f"{url}&page={pageNumber}"
            else:
                currentUrl = None

        return {
            'subfolder': subfolder,
            'links': picLinks
        }
