import os
from openai import OpenAI
from parsers import RawData
from article_writer import BaseArticle
from ai_detector import AIDetector
from utils.utils import load_json

PROMPTS = load_json("./prompts.json").get('prompts', [])


class Article(BaseArticle):
    def __init__(self, title, subtitle, text, ai_score=100) -> None:
        super().__init__(title, subtitle, text, ai_score)


class BaseAIRewriter:
    def __init__(self, raw_data: RawData, os_var_name: str) -> None:
        if not isinstance(raw_data, RawData):
            raise TypeError(f"raw_data must be of type RawData, but got {type(raw_data)}")
        self._raw_data = raw_data
        api_key = os.getenv(os_var_name)
        if api_key:
            self._api_key = api_key
        
    def rewrite(self) -> Article:
        raise NotImplementedError("Method must be implemented in child class")
    
    
class GPTRewriter(BaseAIRewriter):
    def __init__(self, raw_data: RawData, os_var_name: str, model: str) -> None:
        super().__init__(raw_data, os_var_name)
        self.__client = OpenAI(api_key=self._api_key)
        self.__max_len = 4096
        self.__model = model
            
    def rewrite(self, content) -> Article:
        chat_completion_text = self.__client.chat.completions.create(
        messages=[
            {"role": "system", "content": "You are a skilled content writer who creates human-like articles."},
            {"role": "user", "content": content}
                ],
            model=self.__model,
            max_tokens=self.__max_len,
            temperature=0.8
            )
            
        return chat_completion_text.choices[0].message.content.strip()

class BaseRewriterManager:
    def __init__(self, raw_data: RawData, os_var_name: str) -> None:
        pass

   
class GPTRewriterManager(BaseRewriterManager):
    def __init__(self, raw_data: RawData, os_var_name: str, model: str) -> None:
        super().__init__(raw_data, os_var_name)
        self.gpt_rewriter = GPTRewriter(raw_data, os_var_name, model)
        self._ai_detector = AIDetector

    def trigger_multiple_prompts_rewrite(self, prompt_list=PROMPTS) -> Article:
        data = self.gpt_rewriter._raw_data
        index = 0
        
        while index < len(prompt_list):
            prompt = prompt_list[index]
            title_prompt = f"{prompt}\n\nRewrite the title:\n{data.title}"
            anonse_prompt = f"{prompt}\n\nRewrite the subtitle (anonse):\n{data.subtitle}"
            text_prompt = f"{prompt}\n\nRewrite the article text:\n{data.text}"

            rewritten_title = self.gpt_rewriter.rewrite(title_prompt)
            rewritten_anonse = self.gpt_rewriter.rewrite(anonse_prompt)
            rewritten_text = self.gpt_rewriter.rewrite(text_prompt)

            ai_detection_result = self._ai_detector.get_ai_detection_edenai(rewritten_text)
            
            if "ai_score" in ai_detection_result:
                ai_score = ai_detection_result['ai_score']
            if ai_score < 50:
                return Article(rewritten_title, rewritten_anonse, rewritten_text, ai_score)
          
            index += 1
        return Article(rewritten_title, rewritten_anonse, rewritten_text, ai_score)
