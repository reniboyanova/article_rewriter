from parsers import RawData, HTMLScraper, BaseParser
from openai import OpenAI
from utils.utils import get_api_key



class RawExtractor:
    def __init__(self, raw_data: RawData) -> None:
        if not isinstance(raw_data, RawData):
            raise Exception("Can not be extract data of missing RawData")
        self._raw_data = raw_data
        self.__api_key = get_api_key('./OPEN_AI_API_KEY.txt')
        
    def extract_raw_data(self):
        client = OpenAI(api_key=self.__api_key)
        
        user_prompt = f"""Plese extract key points from provided news:
                title: {self._raw_data.title}
                subtitle: {self._raw_data.subtitle}
                article text:{self._raw_data.text}
                
                Return them in dictionary as key: value pairs;
                I'll provide you with the key names and a description of what the value should contain (in parentheses)
                Keys: date (in datetime format only if exist); place_of_event (string, if exist); involved_individuals (List of names (strings))
                    key_points_in_news (A list of the most significant events from the news based on the involved individuals and their actions. 
                    Based on locations and events that occurred there, and based on dates, times, and events that happened around them.)
                    summary (make a summary of provided news).
                If information that need to be set as a value doesn't exist set value to None;
                """
        
        chat_completion_text = client.chat.completions.create(
        messages=[
            {"role": "system", "content": "You are a skilled news redactor who can summarise them perfect."},
            {"role": "user", "content": user_prompt}
                ],
            model="gpt-4o",
            max_tokens=4096,
            temperature=0.8
            )
        
        return chat_completion_text.choices[0].message.content


if __name__ == "__main__":
    
    html_scraper = HTMLScraper("https://www.hurriyet.com.tr/kelebek/televizyon/ulkesini-miss-universede-temsil-edecek-iste-rusyanin-en-guzel-kizi-42555641")
    html_scraper.make_soup()
    parser = BaseParser(html_scraper.soup)
    
    raw_data = parser.extract_raw_data()
    raw_extr = RawExtractor(raw_data)
    print(raw_extr.extract_raw_data())
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
    