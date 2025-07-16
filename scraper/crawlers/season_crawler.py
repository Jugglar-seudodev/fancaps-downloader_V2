from bs4 import BeautifulSoup
from scraper.crawlers import episode_crawler
import re
import urllib.request
import urllib.error
from scraper.utils.colors import Colors

class SeasonCrawler:
    def crawl(self, url):
        epLinks = []
        picLinks = []
        currentUrl = url
        page = 1

        while currentUrl:
            try:
                request = urllib.request.Request(currentUrl, headers={
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:124.0) Gecko/20100101 Firefox/124.0'
                })
                content = urllib.request.urlopen(request)
            except urllib.error.URLError as e:
                Colors.print(f"Error opening URL: {e.reason}", Colors.RED)
                break
            except urllib.error.HTTPError as e:
                Colors.print(f"HTTP Error: {e.code} {e.reason}", Colors.RED)
                break

            try:
                soup = BeautifulSoup(content, 'html.parser')
            except Exception as e:
                Colors.print(f"Error parsing page: {e}", Colors.RED)
                break

            # Encontrar todos los links de episodios
            for a in soup.find_all('a', class_='btn', href=True):
                href = a['href']
                if 'episodeimages.php?' in href:
                    if not href.startswith("http"):
                        href = 'https://fancaps.net' + href
                    epLinks.append(href)

            # Buscar paginación
            next_link = soup.find("a", href=lambda h: h and f"&page={page + 1}" in h)
            if next_link:
                page += 1
                currentUrl = url + f"&page={page}"
            else:
                currentUrl = None

        # Usar el episode_crawler
        crawler = episode_crawler.EpisodeCrawler()
        for epLink in epLinks:
            try:
                episodeResult = crawler.crawl(epLink)
                picLinks.append(episodeResult)
                Colors.print(f"\t{epLink} crawled", Colors.GREEN)
            except Exception as e:
                Colors.print(f"Failed to crawl {epLink}: {e}", Colors.RED)

        return picLinks
