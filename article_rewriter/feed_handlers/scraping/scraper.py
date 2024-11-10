from bs4 import BeautifulSoup
import requests
from urllib.parse import urlparse

from article_rewriter.constants import *
from article_rewriter.feed_handlers.scraping.parsers.cumhuriyet_parser import CumhuriyetParser
from article_rewriter.feed_handlers.scraping.parsers.haberturk_parser import HuberturkParser
from article_rewriter.feed_handlers.scraping.parsers.hurriyet_parser import HurriyetParser
from article_rewriter.feed_handlers.scraping.parsers.sozcu_parser import SozcuParser


DOMAIN_PARSER_MAP = {
    CUMHURIYET_DOMAIN: CumhuriyetParser,
    HABERTURK_DOMAIN: HuberturkParser,
    HURRIYET_DOMAIN: HurriyetParser,
    SOZCU_DOMAIN: SozcuParser,
}


class HTMLScraper:
    @staticmethod
    def _get_response(url: str) -> str:
        response = requests.get(url)
        response.raise_for_status()
        return response.text

    def _make_soup(self, source_url: str) -> BeautifulSoup:
        response_text = self._get_response(source_url)
        return BeautifulSoup(response_text, 'html.parser')

    @staticmethod
    def _get_response_parser(url: str):
        parsed_url = urlparse(url)
        domain = parsed_url.netloc
        if domain.startswith('www.'):
            domain = domain[4:]

        parser_cls = DOMAIN_PARSER_MAP.get(domain)
        if parser_cls is None:
            raise ValueError

        return parser_cls()

    def _scrape(self, source_url: str):
        soup = self._make_soup(source_url)
        parser = self._get_response_parser(source_url)
        return parser.extract_raw_data(soup)    # missing method

    def scrape(self, source_url: str):
        try:
            return self._scrape(source_url)
        except Exception as e:
            return None
