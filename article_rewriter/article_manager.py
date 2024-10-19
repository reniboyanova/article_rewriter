from typing import Union

from article_rewriter.writing.article_rewriter import GPTRewriterManager
from article_rewriter.writing.article_writer import ArticleWriter
from article_rewriter.models import Article
from article_rewriter.feed_handlers.scraping.scraper import HTMLScraper
from article_rewriter.writing.summary_extractor import SummaryExtractor
from article_rewriter.writing.event_info_extractor import EventInfoExtractor


class ArticleManager:
    def __init__(self):
        self._scraper = HTMLScraper()
        self._rewrite_manager = GPTRewriterManager()
        self._article_writer = ArticleWriter()
        self._summary_extractor = SummaryExtractor()
        self._event_info_extractor = EventInfoExtractor()

    def rewrite_article_from_raw_data(self, article_url: str) -> Union[Article, None]:
        raw_data = self._scraper.scrape(article_url)
        if raw_data is None:
            return None

        return self._rewrite_manager.write(raw_data)

    def rewrite_article_from_base_article(self, article_url: str) -> Union[Article, None]:
        raw_data = self._scraper.scrape(article_url)
        if raw_data is None:
            return None

        summary = self._summary_extractor.extract_raw_data(raw_data)
        base_article = self._article_writer.write_article(summary)
        return self._rewrite_manager.write(base_article)

    def extract_event_info(self, article_url):
        raw_data = self._scraper.scrape(article_url)
        if raw_data is None:
            return None

        return self._event_info_extractor.extract_event_info(raw_data)
