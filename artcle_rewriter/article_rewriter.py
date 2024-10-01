import os
from openai import OpenAI
from scraper import Scraper
from utils.utils import load_json

prompts_path = os.path.abspath("article_rewriter\prompts.json")
# prompts = load_json("article_rewriter/prompts.json")
print(prompts_path)

class AIRewriter:
    def __init__(self, src_url, prompts_list) -> None:
        self.__scraper = None
        
        try:
            self.__scraper =  Scraper(src_url)
        except Exception as e:
            raise Exception(f"Error from Scraper, self.__scraper can not be set of exception: {e}")
        
        if self.__scraper is not None:
            self.__scraper.extract_data()
            self.data = self.__scraper.data
            
    
        self.prompts = prompts_list