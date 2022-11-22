"""
This is a boilerplate pipeline 'data_collection'
generated using Kedro 0.18.3
"""
from .scraper import Crawler

def crawl_links():
    """Obtains the target links"""
    crawler = Crawler()
    crawler.crawl()
    return crawler.collected_links
