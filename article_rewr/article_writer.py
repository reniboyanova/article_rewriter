import os
import re
from openai import OpenAI
from parsers import RawData

class BaseArticle(RawData):
    def __init__(self, title, subtitle, text, ai_score=100) -> None:
        super().__init__(title, subtitle, text, ai_score)
    

class ArticleWriter:
    def __init__(self, article_summary) -> None:
        self.__article_summary = article_summary

    def write_article(self) -> BaseArticle:
        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

        user_prompt = f"""  {self.__article_summary}
        Base on key-value pairs in this dictionary and web search,
        make an article with title, subtitle and article body text.
        Make content authentic, natural, and free from plagiarism, sound like it's written by a human.
        Return the article in a dictionary with 3 keys - title, subtitle, and article_text.
       """

        chat_completion_text = client.chat.completions.create(
            messages=[
                {"role": "system", "content": "You are a professional article writer based on daily news."},
                {"role": "user", "content": user_prompt}
            ],
            model="gpt-4",
            max_tokens=4096,
            temperature=0.2
        )

        content = chat_completion_text.choices[0].message.content
        
        title_match = re.search(r'"title":\s*"([^"]+)"', content)
        subtitle_match = re.search(r'"subtitle":\s*"([^"]+)"', content)
        article_text_match = re.search(r'"article_text":\s*"([^"]+)"', content, re.DOTALL)

        title = title_match.group(1) if title_match else None
        subtitle = subtitle_match.group(1) if subtitle_match else None
        article_text = article_text_match.group(1).replace('\\n', '\n') if article_text_match else None
        
        return BaseArticle(title, subtitle, article_text)


        
        
        