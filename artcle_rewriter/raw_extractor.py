import os
import re
from parsers import RawData, HTMLScraper, BaseParser
from openai import OpenAI


class RawExtractor:
    def __init__(self, raw_data: RawData) -> None:
        if not isinstance(raw_data, RawData):
            raise Exception("Can not be extract data of missing RawData")
        self._raw_data = raw_data
        self.__api_key = os.getenv("OPENAI_API_KEY")
        
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
        
        content = chat_completion_text.choices[0].message.content
        
        date_match = re.search(r'"date":\s*"([^"]+)"', content)
        place_match = re.search(r'"place_of_event":\s*"([^"]+)"', content)
        individuals_match = re.search(r'"involved_individuals":\s*\[([^\]]+)\]', content)
        key_points_match = re.search(r'"key_points_in_news":\s*\[([^\]]+)\]', content)
        summary_match = re.search(r'"summary":\s*"([^"]+)"', content, re.DOTALL)
        
        date = date_match.group(1) if date_match else None
        place_of_event = place_match.group(1) if place_match else None
        involved_individuals = [ind.strip().strip('"') for ind in individuals_match.group(1).split(",")] if individuals_match else []
        key_points_in_news = [point.strip().strip('"') for point in key_points_match.group(1).split(",")] if key_points_match else []
        summary = summary_match.group(1).replace('\\n', '\n') if summary_match else None

        return {
            "date": date,
            "place_of_event": place_of_event,
            "involved_individuals": involved_individuals,
            "key_points_in_news": key_points_in_news,
            "summary": summary
        }
