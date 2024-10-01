import requests
from requests.exceptions import HTTPError
from bs4 import BeautifulSoup

class Scraper:
    def __init__(self, source_url: str) -> None:
        self.url = source_url
        self.soup = None
        self.data = {'title': '', 'anonse': '', 'article_text': ''}
        
    def get_response(self) -> str:
        try:
            response = requests.get(self.url)
            response.raise_for_status()
            return response.text
        except HTTPError as http_err:
            print(f"HTTP error occurred: {http_err}") 
        except Exception as err:
            print(f"Other error occurred: {err}")
    
    def _make_soup(self) -> BeautifulSoup:
        if self.soup is None:
            respons_text = self.get_response()
            self.soup = BeautifulSoup(respons_text, 'html.parser')
            
    def _extract_title(self) -> None:
        h1_tag = self.soup.find('h1')
        if h1_tag:
            self.data['title'] = h1_tag.get_text()
            return
    
    def _extract_anonse(self) -> None:
        h2_tag = self.soup.find('h2')
        if h2_tag:
            self.data['anonse'] = h2_tag.get_text()
            return
        
    def _extract_article_txt(self) -> None:
        paragraphs = self.soup.find_all('p')
        article_text = ' '.join([p.get_text() for p in paragraphs])
        self.data['article_text'] = article_text
        return
    
    def extract_data(self) -> None:
        self._make_soup()
        self._extract_title()
        self._extract_anonse()
        self._extract_article_txt()
        
