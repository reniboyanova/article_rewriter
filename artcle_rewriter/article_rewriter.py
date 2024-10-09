from openai import OpenAI
from parsers import HTMLScraper, BaseParser, HubberturkParser, RawData
from article_writer import ArticleWriter, BaseArticle
from utils.utils import load_json, get_api_key

PROMPTS = load_json("./prompts.json").get('prompts', [])

def part_prompt(client: OpenAI, part_prompt, max_len=4096):
    chat_completion_text = client.chat.completions.create(
        messages=[
            {"role": "system", "content": "You are a skilled content writer who creates human-like articles."},
            {"role": "user", "content": part_prompt}
                ],
            model="gpt-4o",
            max_tokens=max_len,
            temperature=0.8
            )
            
    return chat_completion_text.choices[0].message.content.strip()


class Article(BaseArticle):
    def __init__(self, title: str, subtitle: str, article_text: str) -> None:
        super().__init__(title, subtitle, article_text)

# TODO clear class from attributes
class AIRewriter:
    def __init__(self, src_url, parser: BaseParser, prompts_list) -> None:
        # Can be add some checker for valid websites with regex
        self.__scraper = None
        self.__data: RawData = None
        
        try:
            self.__scraper =  HTMLScraper(src_url)
        except Exception as e:
            raise Exception(f"Error from Scraper, self.__scraper can not be set of exception: {e}")
        
        if self.__scraper is not None:
            soup = self.__scraper.make_soup()
            if not isinstance(parser, BaseParser):
                print(f"Parser need to be instanse of BaseParser, but got {type(parser)}")
                self.__parser = BaseParser(soup)
            else:
                self.__parser = parser
        self.__data = self.__parser.extract_raw_data()
        
        self.prompts = prompts_list
        if not self.prompts:
            print("List with prompts is empty, please list at least one prompt!")
            self.prompts = list(input())
            
        self.__api_key = get_api_key('./OPEN_AI_API_KEY.txt')
            
    # TODO make it gets RawData as param   
    def gpt_rewriter(self) -> dict:
        client = OpenAI(api_key=self.__api_key)

        results = {}

        for index, prompt in enumerate(self.prompts):
            title_prompt = f"{prompt}\n\nRewrite the title:\n{self.__data.title}"
            anonse_prompt = f"{prompt}\n\nRewrite the subtitle (anonse):\n{self.__data.subtitle}"
            text_prompt = f"{prompt}\n\nRewrite the article text:\n{self.__data.text}"

            results[index] = {
                'title': part_prompt(client, title_prompt),
                'anonse': part_prompt(client, anonse_prompt),
                'text': part_prompt(client, text_prompt)
            }
        
        return results
    
    