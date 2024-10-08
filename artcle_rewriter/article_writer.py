import json
from openai import OpenAI
from utils.utils import get_api_key

class ArticleWriter:
    def __init__(self, aritcle_summary) -> None:
        self.__article_summary = aritcle_summary
    
    
    def write_article(self):
        client = OpenAI(api_key=get_api_key('./OPEN_AI_API_KEY.txt'))
        
        user_prompt = f"""  {self.__article_summary}
        Base on key-value pairs in this dictioanary and web search,
        make an article whith title, subtitle and article body text.
        Make content authentic, natural, and free from plagiarism, sound like it's writen by human.
        Return article in dictionary with 3 keys - title, subtitle and article_text.
       """
        
        chat_completion_text = client.chat.completions.create(
        messages=[
            {"role": "system", "content": "You are profesional article writer based on daily news."},
            {"role": "user", "content": user_prompt}
                ],
            model="gpt-4o",
            max_tokens=4096,
            temperature=0.2
            )
        
        content = chat_completion_text.choices[0].message.content
        
        if content.startswith("```") and content.endswith("```"):
            content = content[3:-3].strip()
        
        try:
            article_dict = json.loads(content)
            article_text = article_dict.get('article_text', '')
            formatted_article_text = f'"""\n{article_text.replace("\\n\\n", "\n\n")}\n"""'
            article_dict['article_text'] = formatted_article_text
            return article_dict
        
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON: {e}")
            return content

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
    
    print(art_wr.write_article())
        
        
        