from markdownify import markdownify
from typing import Optional, List, Dict


class ParsedComponent:
    def __init__(self, html: str):
        self._html = html

    def _to_markdown(self) -> str:
        return markdownify(self._html, heading_style="ATX")

    def to_markdown(self) -> str:
        return self._to_markdown()
    


class ParsedHeading(ParsedComponent):
    def __init__(self, text: str, level: int):
        self._text = text
        self._level = level

    def _to_markdown(self) -> str:
        return f"{'#' * self._level} {self._text}"

    @property
    def text(self) -> str:
        return self._text

    @property
    def level(self) -> int:
        return self._level


class ParsedParagraph(ParsedComponent):
    def __init__(self, text: str):
        self._text = text

    def _to_markdown(self) -> str:
        return self._text

    @property
    def text(self) -> str:
        return self._text


class ParsedLink(ParsedComponent):
    def __init__(self, text: str, url: str):
        self._text = text
        self._url = url

    def _to_markdown(self) -> str:
        return f"[{self._text}]({self._url})"

    @property
    def text(self) -> str:
        return self._text

    @property
    def url(self) -> str:
        return self._url


class ParsedImage(ParsedComponent):
    def __init__(self, url: str, description: Optional[str], html: str):
        super().__init__(html)
        self._url = url
        self._description = description

    def _to_markdown(self) -> str:
        return f"![{self._description}]({self._url})"

    @property
    def url(self) -> str:
        return self._url

    @property
    def description(self) -> str:
        return self._description


class ParsedVideo(ParsedComponent):
    def __init__(self, url: str, name: Optional[str], html: str):
        super().__init__(html)
        self._url = url
        self._name = name

    def _to_markdown(self) -> str:
        return f"[Watch {self._name}]({self._url})" if self._url else markdownify(self._html, heading_style="ATX")

    @property
    def url(self) -> str:
        return self._url

    @property
    def name(self) -> str:
        return self._name


class ParsedEquation(ParsedComponent):
    def __init__(self, latex: str, equation_number: Optional[int] = None):
        self._latex = latex
        self._equation_number = equation_number

    def _to_markdown(self) -> str:
        md = self._latex
        if self._equation_number is not None:
            md += f'    ({self._equation_number})'
        return md

    @property
    def latex(self) -> str:
        return self._latex

    @property
    def equation_number(self) -> Optional[int]:
        return self._equation_number


class ParsedCitation(ParsedComponent):
    def __init__(self, text: str, citation_text: str):
        self._text = text
        self._citation_text = citation_text

    def _to_markdown(self) -> str:
        return f'{self._text}\n> {self._citation_text}'

    @property
    def text(self) -> str:
        return self._text

    @property
    def citation_text(self) -> str:
        return self._citation_text


class ListItem:
    def __init__(self, indent: int, bullet: str, content: str):
        self._indent = indent
        self._bullet = bullet
        self._content = content

    @property
    def indent(self) -> int:
        return self._indent

    @property
    def bullet(self) -> str:
        return self._bullet

    @property
    def content(self) -> str:
        return self._content


class ParsedList(ParsedComponent):
    def __init__(self, items: List[ListItem]):
        self._items = items

    def _to_markdown(self) -> str:
        return '\n'.join(f'{"  " * i.indent}{i.bullet} {i.content}' for i in self._items)

    @property
    def items(self) -> List[ListItem]:
        return self._items
