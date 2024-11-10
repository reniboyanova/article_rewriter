from bs4 import BeautifulSoup
from datetime import datetime, date
from typing import List, Union, Optional, Dict
from metadata import *
from components import *
import requests
from parse_result import ParseResult
from urllib.parse import urlparse


class SozcuParser:
    def __init__(self, url: str):
        if not self.is_valid_sozcu_url(url):
            raise ValueError("URL must start with 'https://www.sozcu.com.tr/'")
        
        response = requests.get(url)
        html_content = response.text
        self.soup = BeautifulSoup(html_content, 'html.parser')
        self.article = self.soup.find("article")
        if not self.article:
            raise ValueError("No <article> tag found in the provided HTML content.")

    def is_valid_sozcu_url(self, url: str) -> bool:
        parsed_url = urlparse(url)
        return parsed_url.scheme == "https" and parsed_url.netloc == "www.sozcu.com.tr"

    def parse_date(self) -> Optional[date]:
        date_element = self.article.find("time", {"datetime": True})
        if date_element:
            return datetime.fromisoformat(date_element["datetime"]).date()
        return None

    def parse_authors(self) -> List[Author]:
        author_div = self.article.find("div", class_="content-meta-name")
        authors = []
        if author_div:
            name = author_div.get_text(strip=True)
            img = author_div.find("img", src=True)
            url = img["src"] if img else None
            authors.append(Author(name=name, url=url, html=str(author_div)))
        return authors

    def parse_categories(self) -> List[Category]:
        category_elements = self.article.select("div.pe-2 a")
        categories = []
        for cat in category_elements:
            category_name = cat.text.strip().replace(" -", "").strip()
            if category_name:
                categories.append(Category(name=category_name, url=cat["href"], html=str(cat)))
        return categories

    def parse_tags(self) -> List[Tag]:
        tag_elements = self.article.select("ul.tags a")
        return [Tag(name=tag.text.strip(), url=tag["href"], html=str(tag)) for tag in tag_elements]

    def parse_components(self) -> List[ParsedComponent]:
        components = []
        for level in range(1, 4):
            for header in self.article.find_all(f'h{level}'):
                components.append(ParsedHeading(text=header.text.strip(), level=level, html=str(header)))

        for paragraph in self.article.select(".article-body p"):
            components.append(ParsedParagraph(text=paragraph.text.strip(), html=str(paragraph)))

        for link in self.article.select("a"):
            if link.get("href"):
                components.append(ParsedLink(text=link.text.strip(), url=link["href"], html=str(link)))

        for img in self.article.find_all("img"):
            components.append(ParsedImage(url=img["src"], description=img.get("alt", ""), html=str(img)))

        video_div = self.article.find("div", id="my-dailymotion-player")
        if video_div:
            script_tag = video_div.find_next("script", text=True)
            if script_tag and 'video' in script_tag.text:
                video_id = script_tag.text.split("'video':")[1].split(',')[0].strip().strip("'\"")
                url = f"https://www.dailymotion.com/video/{video_id}"
                components.append(ParsedVideo(url=url, name="Dailymotion Video", html=str(video_div)))

        return components

    def parse_html_to_markdown(self) -> ParseResult:
        metadata = ArticleMetadata(
            article_date=self.parse_date(),
            authors=self.parse_authors(),
            categories=self.parse_categories(),
            tags=self.parse_tags()
        )

        components = self.parse_components()

        return ParseResult(components=components, metadata=metadata)