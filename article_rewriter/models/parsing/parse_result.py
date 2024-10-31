from typing import List

from article_rewriter.models.parsing.metadata import ArticleMetadata
from article_rewriter.models.parsing.components import ParsedComponent


class ParseResult:
    def __init__(self, components: List[ParsedComponent], metadata: ArticleMetadata):
        self._components = components
        self._metadata = metadata

    @property
    def components(self):
        return self._components

    @property
    def metadata(self):
        return self._metadata
