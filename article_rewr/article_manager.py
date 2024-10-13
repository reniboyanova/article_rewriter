from article_rewriter import GPTRewriterManager, Article
from parsers import HTMLScraper, BaseParser, RawData
from raw_extractor import RawExtractor
from article_writer import ArticleWriter, BaseArticle

MODEL = "gpt-4o"
OPENAI_API_KEY = "OPENAI_API_KEY"
    
class ArticleManager:
    def __init__(self, url) -> None:
        if not url:
            raise ValueError("Url can't be None or ''. Please provide an utl")
        # TODO make a regex validation for all valid urls
        self.__scraper = HTMLScraper(url)
        self.__soup = self.__scraper.make_soup()
        self.__parser = BaseParser(self.__soup)
        self.__raw_data: RawData = self.__parser.extract_raw_data()    
    
    def _trigger_summary_extracting(self) -> dict:
        raw_extractor = RawExtractor(self.__raw_data)
        return raw_extractor.extract_raw_data()

    def _trigger_article_write(self) -> BaseArticle:
        art_writer = ArticleWriter(self._trigger_summary_extracting())
        return art_writer.write_article()

    def _get_gpt_rewriter_manager(self, data: RawData|BaseArticle) -> GPTRewriterManager:
        if not OPENAI_API_KEY:
            raise EnvironmentError("API key for OpenAI is missing. Please set the OPENAI_API_KEY.")
        
        return GPTRewriterManager(data, OPENAI_API_KEY, MODEL)

    def trigger_rewrite_by_raw_data(self) -> Article:
        gpt_rewriter_mng = self._get_gpt_rewriter_manager(self.__raw_data)
        return gpt_rewriter_mng.trigger_multiple_prompts_rewrite()

    def trigger_rewrite_by_base_article(self) -> Article:
        base_article = self._trigger_article_write()
        gpt_rewriter_mng = self._get_gpt_rewriter_manager(base_article)
        return gpt_rewriter_mng.trigger_multiple_prompts_rewrite()
    
    
def main(url):
     article_manager = ArticleManager(url)
     article_rewrite_by_raw_data = article_manager.trigger_rewrite_by_raw_data()
     print(f"This is from raw data\n Text: {article_rewrite_by_raw_data.text} \n AI SCORE: {article_rewrite_by_raw_data.ai_score}\n")
     
     article_rewrite_by_base_art = article_manager.trigger_rewrite_by_base_article()
     print(f"This is from base article\n Text: {article_rewrite_by_base_art.text} \n AI SCORE: {article_rewrite_by_base_art.ai_score}\n")
     

if __name__ == "__main__":
    main("https://www.cumhuriyet.com.tr/dunya/ikinci-intifadadan-bu-yana-bir-ilk-bati-seriada-zirhli-personel-2256336")


       

        
        
        
        
    