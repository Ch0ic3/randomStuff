import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import logging
import queue

q = queue.Queue()

class crawler:
    def __init__(self,urls=[]):
        self.visited_urls = []
        self.not_vitisted_urls = urls
        self.domain = urls[0].strip("https://")

    def gettext(self, url):
        try:
            return requests.get(url, timeout=2).text
        except requests.exceptions.ReadTimeout:
            return "ERROR"
        except requests.exceptions.ConnectTimeout:
            return "ERROR"
        except requests.exceptions.InvalidSchema:
            return "ERROR"
        except requests.exceptions.MissingSchema:
            return "ERROR"

    def getlinks(self,url, html):
        soup = BeautifulSoup(html, "html.parser")
        for link in soup.find_all("a"):
            path = link.get("href")
            if path and path.startswith("/"):
                path = urljoin(url,path)
            yield path

    def crawl(self,url):
        html = self.gettext(url)
        for url in self.getlinks(url, html):
            try:
                self.addurltovisited(url)
            except TypeError:
                pass

    def addurltovisited(self,url):
        if self.domain in url:
            if url not in self.visited_urls and url not in self.not_vitisted_urls:
                self.not_vitisted_urls.append(url)

    def run(self):
        while self.not_vitisted_urls:
            url = self.not_vitisted_urls.pop(0)
            
            print(url)
            logging.info(f"Crawling: {url}")
            try:
                self.crawl(url)
            except:
                logging.exception(f"Failed to crawl: {url}")
            finally:
                self.visited_urls.append(url)

if __name__ == "__main__":
    host = input("Input Host: ")
    crawler( urls=[host]).run()

