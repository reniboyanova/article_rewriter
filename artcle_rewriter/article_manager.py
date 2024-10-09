from article_rewriter import BaseRewriterManager, GPTRewriterManager
from parsers import HTMLScraper, BaseParser, RawData
from raw_extractor import RawExtractor

MODEL = "gpt-4o"
OPENAI_API_KEY = "OPENAI_API_KEY"
    
class ArticleManager:
    def __init__(self, url) -> None:
        if not url:
            raise ValueError("Url can't be None or ''. Please provide an utl")
        # TODO make a regex validation for all valid urls
        self.__soup = HTMLScraper(url)
        self.__parser = BaseParser(self.__soup)
        self.__raw_data: RawData = self.__parser.extract_raw_data()
        self.__rewriter_mng: dict[str, BaseRewriterManager] = {}
    
    
    def trigger_raw_extracting(self) -> dict:
        raw_extr = RawExtractor(self.__raw_data)
        return raw_extr.extract_raw_data()
    
    
    def trigger_article_write(self):
        pass
    
    
    def gpt_rewriter_manager(self):
        gpt_rewriter_mng = GPTRewriterManager(self.__raw_data, OPENAI_API_KEY, MODEL)
        self.__rewriter_mng['gpt-4o-rewriter'] = gpt_rewriter_mng
        
    def trigger_rewrite_by_raw_data(self):
        pass
            
       

        
        
        
        
    