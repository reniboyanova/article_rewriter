import re

from openai import OpenAI

from article_rewriter.constants import *
from article_rewriter.models.models import RawData


class SummaryExtractor:
    def __init__(self):
        self._client = OpenAI()

    def _load_user_prompt(self, raw_data: RawData) -> str:
        with open(SUMMARY_PROMPT_TEMPLATE_PATH) as f:
            prompt_raw = f.read().strip()

        return prompt_raw.format(title=raw_data.title, subtitle=raw_data.subtitle, text=raw_data.text)

    def _parse_response(self, content):
        date_match = re.search(r'"date":\s*"([^"]+)"', content)
        place_match = re.search(r'"place_of_event":\s*"([^"]+)"', content)
        individuals_match = re.search(r'"involved_individuals":\s*\[([^\]]+)\]', content)
        key_points_match = re.search(r'"key_points_in_news":\s*\[([^\]]+)\]', content)
        summary_match = re.search(r'"summary":\s*"([^"]+)"', content, re.DOTALL)

        date = date_match.group(1) if date_match else None
        place_of_event = place_match.group(1) if place_match else None
        involved_individuals = [ind.strip().strip('"') for ind in
                                individuals_match.group(1).split(",")] if individuals_match else []
        key_points_in_news = [point.strip().strip('"') for point in
                              key_points_match.group(1).split(",")] if key_points_match else []
        summary = summary_match.group(1).replace('\\n', '\n') if summary_match else None

        return {
            "date": date,
            "place_of_event": place_of_event,
            "involved_individuals": involved_individuals,
            "key_points_in_news": key_points_in_news,
            "summary": summary
        }

    def extract_summary(self, raw_data: RawData) -> dict:
        if not isinstance(raw_data, RawData):
            raise TypeError("Can not be extract data of missing RawData")

        user_prompt = self._load_user_prompt(raw_data)

        chat_completion_text = self._client.chat.completions.create(
            messages=[
                {"role": "system", "content": "You are a skilled news redactor who can summarise them perfect."},
                {"role": "user", "content": user_prompt}
            ],
            model="gpt-4o",
            max_tokens=4096,
            temperature=0.8
        )

        content = chat_completion_text.choices[0].message.content

        return self._parse_response(content)
