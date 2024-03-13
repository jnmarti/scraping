import re
from hashlib import sha256
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

root_address = "https://elsalvadorgram.com/"

class Crawler(object):
    @classmethod
    def get_browser(cls):
        options = webdriver.ChromeOptions()
        options.add_argument("--no-sandbox")
        options.add_argument('--headless')
        return webdriver.Chrome(options=options)

    def __init__(self):
        self.root_address = "https://elsalvadorgram.com"
        self.browser = Crawler.get_browser()
        self.local_page_regex = f"^{self.root_address}"
        self.valid_page_regex = re.compile("^https:\/\/elsalvadorgram.com\/[0-9]+\/[0-9]+\/[a-zA-Z^\-]+\/")
        self.collected_links = []

    def is_valid_url(self, url):
        return self.valid_page_regex.match(url) is not None

    def get_links(self):
        self.browser.get(self.root_address)
        bs = BeautifulSoup(self.browser.page_source)
        link_tags = bs.find_all("a")
        links = {tag.get("href") for tag in link_tags}
        valid_links = [link for link in links if self.is_valid_url(link) and link not in self.collected_links]
        self.collected_links.extend(valid_links)
        return valid_links

    def crawl(self):
        iteration_links = self.get_links(self.root_address)
        while len(iteration_links) > 0:
            batch_links = iteration_links
            iteration_links = []
            for link in batch_links:
                iteration_links.extend(self.get_links(link))


class Scraper(object):

    def get_image_url(self, article):
        try:
            return article.find("div", {"id": self.image_tag_id}).find("img")["src"]
        except Exception:
            return None
    

    def get_title(self, article):
        try:
            return article.find("header", {"id": self.title_tag_id}).find("h1").text
        except Exception:
            return None

    def get_content(self, article):
        try:
            paragraphs = article.find("section", {"id": self.content_tag_id}).find_all("p")
            return "\n".join([p.text for p in paragraphs])
        except Exception:
            return None

    def scrape(self, url):
        self.browser.get(url)
        bs = BeautifulSoup(self.browser.page_source)
        article = bs.find("article")
        return {
            "image_src": self.get_image_url(article),
            "title": self.get_title(article),
            "content": self.get_content(article),
            "link": url
        }

    @classmethod
    def get_hash(cls, link):
        value = bytes(link, encoding="utf-8")
        return hex(int(sha256(value).hexdigest(), 16) % (10**16))
