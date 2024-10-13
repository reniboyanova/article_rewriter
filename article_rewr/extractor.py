import uuid
import os
from parsers import RawData, BaseParser, HTMLScraper
from openai import OpenAI
from utils.utils import load_json

API_KEY = "OPENAI_API_KEY"
MODEL = "gpt-4o"
PROMPTS = load_json("./parts_prompt.json")

# Classes for each one, based on json response
class Event:
    def __init__(self, main_event, type, subtype, description) -> None:
        self.uid = str(uuid.uuid4())
        self.main_event = main_event
        self.type = type
        self.subtype = subtype
        self.description = description
        
class MainExtractor:
    def __init__(self, extracted_info: RawData) -> None:
        if not isinstance(extracted_info, RawData):
            raise TypeError(f"extracted_info must be of type <cls RawData> but goot {type(extracted_info)}")
        self.__extracted_info: RawData = extracted_info
        self.__api_key = os.getenv(API_KEY)
        
        if not self.__api_key:
            raise ValueError("API_KEY is empty, plese check os env for API_KEY")
        
        self.__client = OpenAI(api_key=self.__api_key)
        self.__max_len = 4096
        self.__model = MODEL
        
    def extract_event_json(self, prompt_type: str):
        prompt = PROMPTS.get(prompt_type)
        prompt = ''.join(s for s in prompt)
        content = f""" {prompt}
                    Title: {self.__extracted_info.title}
                    Subtitle: {self.__extracted_info.subtitle}
                    Article Text: {self.__extracted_info.text}
                    """
        
        chat_completion_text = self.__client.chat.completions.create(
        messages=[
            {"role": "system", "content": "You are a skilled news redactor."},
            {"role": "user", "content": content},
                ],
            model=self.__model,
            max_tokens=self.__max_len,
            temperature=0.8,
            response_format={"type":"json_object" }
            )
            
        return chat_completion_text.choices[0].message.content.strip()
        
        
if __name__ == "__main__":
    scraper = HTMLScraper("https://www.cumhuriyet.com.tr/siyaset/ozgur-ozel-chpnin-adayini-anlatti-aslan-gibi-bir-cumhuriyet-halk-2257352")
    soup = scraper.make_soup()
    parser = BaseParser(soup)
    
    raw_data = parser.extract_raw_data()
    
    event_extr = MainExtractor(raw_data)
    
    print(event_extr.extract_event_json("summary_prompt"))
        