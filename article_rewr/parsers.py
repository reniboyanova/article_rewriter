import requests
import json
from requests.exceptions import HTTPError
from bs4 import BeautifulSoup


class HTMLScraper:
    def __init__(self, source_url: str) -> None:
        self.url = source_url
        self.soup = None
                
    def get_response(self) -> str:
        try:
            response = requests.get(self.url)
            response.raise_for_status()
            return response.text
        except HTTPError as http_err:
            print(f"HTTP error occurred: {http_err}") 
        except Exception as err:
            print(f"Other error occurred: {err}")
    
    def make_soup(self) -> BeautifulSoup:
        if self.soup is None:
            respons_text = self.get_response()
            self.soup = BeautifulSoup(respons_text, 'html.parser')
        return self.soup

class RawData:
    def __init__(self, title, subtitle, text, ai_score=100) -> None:
        self.title = title
        self.subtitle = subtitle
        self.text = text
        self.ai_score = ai_score
        
        
class BaseParser:
    def __init__(self, soup: BeautifulSoup) -> None:
        self._soup = soup

    def extract_raw_data(self, title_tag="headline", anonse_tag="description", article_body_tag="p") -> RawData:
        script_tag = self._soup.find('script', type='application/ld+json')
        if script_tag:
            try:
                json_data = json.loads(script_tag.string)
                title = json_data.get(title_tag, '')
                subtitle = json_data.get(anonse_tag, '')
                try:
                    paragraphs = self._soup.find_all(article_body_tag)
                    article_text = ' '.join([p.get_text() for p in paragraphs])
                except Exception as e:
                    print(f"Exceptions while extracting article body: {e}")
            except json.JSONDecodeError as e:
                print(f"Error decoding json. Exception: {e}")
        return RawData(title, subtitle, article_text)


class SoscuParser(BaseParser):
    def __init__(self, soup: BeautifulSoup) -> None:
        super().__init__(soup)

        
class HurriyetParser(BaseParser):
    def __init__(self, soup: BeautifulSoup) -> None:
        super().__init__(soup)


class CumhuriyetParser(BaseParser):
    def __init__(self, soup: BeautifulSoup) -> None:
        super().__init__(soup)
        

class HubberturkParser(BaseParser):
    def __init__(self, soup: BeautifulSoup) -> None:
        super().__init__(soup)
        
   