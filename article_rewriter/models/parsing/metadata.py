from datetime import date
from typing import List, Dict, Union
from components import ParsedComponent


class Author(ParsedComponent):
    def __init__(self, name: str, url: str, html: str):
        super().__init__(html)
        self._name = name
        self._url = url

    def __repr__(self):
        return self._name

    @property
    def name(self) -> str:
        return self._name

    @property
    def url(self) -> str:
        return self._url


class Category(ParsedComponent):
    def __init__(self, name: str, url: str, html: str):
        super().__init__(html)
        self._name = name
        self._url = url

    def __repr__(self):
        return self._name

    @property
    def name(self) -> str:
        return self._name

    @property
    def url(self) -> str:
        return self._url


class Tag(ParsedComponent):
    def __init__(self, name: str, url: str, html: str):
        super().__init__(html)
        self._name = name
        self._url = url

    def __repr__(self):
        return self._name

    @property
    def name(self) -> str:
        return self._name

    @property
    def url(self) -> str:
        return self._url


class ArticleMetadata:
    def __init__(
            self,
            article_date: date,
            authors: List[Union[Author, Dict]],
            categories: List[Union[Category, Dict]],
            tags: List[Union[Tag, Dict]],
    ):
        self._date = article_date
        self._authors = authors
        self._categories = categories
        self._tags = tags

        self._init()

    def _init(self):
        if self._authors and isinstance(self._authors[0], dict):
            self._authors = [Author(**x) for x in self._authors]

        if self._categories and isinstance(self._categories[0], dict):
            self._categories = [Category(**x) for x in self._categories]

        if self._tags and isinstance(self._tags[0], dict):
            self._tags = [Tag(**x) for x in self._tags]

    @property
    def date(self) -> date:
        return self._date

    @property
    def authors(self) -> List[Author]:
        return self._authors

    @property
    def categories(self) -> List[Category]:
        return self._categories

    @property
    def tags(self) -> List[Tag]:
        return self._tags

    def to_dict(self):
        return {
            'article_date': self.date,
            'authors': self.authors,
            'categories': self.categories,
            'tags': self.tags,
        }
