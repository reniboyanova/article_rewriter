import re
from openai import OpenAI
from parsers import RawData
from utils.utils import get_api_key


class BaseArticle(RawData):
    def __init__(self, title, subtitle, text) -> None:
        super().__init__(title, subtitle, text)
        self.ai_score: float = 0
    

class ArticleWriter:
    def __init__(self, article_summary) -> None:
        self.__article_summary = article_summary

    def write_article(self) -> BaseArticle:
        client = OpenAI(api_key=get_api_key('./OPEN_AI_API_KEY.txt'))

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

if __name__ == "__main__":
    example_data_output  = {
    "date": "2024-10-07",
    "place_of_event": "Barvikha Luxury Village concert hall",
    "involved_individuals": ["Valentina Alekseeva", "Irina Mironova", "Ulyana Evdokimova"],
    "key_points_in_news": [
        "Valentina Alekseeva won the Miss Russia 2024 beauty pageant.",
        "Alekseeva will represent Russia in the 73rd Miss Universe competition.",
        "She received a prize of 1 million rubles.",
        "Irina Mironova was the runner-up, and Ulyana Evdokimova secured third place.",
        "Valentina Alekseeva is a medical student at Pirogov Russian National Research Medical University."
    ],
    "summary": "Valentina Alekseeva, an 18-year-old from the Chuvash Republic, won the Miss Russia 2024 beauty pageant. She will represent Russia in the 73rd Miss Universe competition and received a 1 million ruble prize. The event took place at the Barvikha Luxury Village concert hall, with Irina Mironova and Ulyana Evdokimova placing second and third, respectively. Alekseeva is currently pursuing a medical degree."
}
    art_wr = ArticleWriter(example_data_output)
    
    print(art_wr.write_article().__dict__)
        
        
        