import os
import re

from openai import OpenAI

from article_rewriter.constants import *
from article_rewriter.models import BaseArticle


class ArticleWriter:
    def __init__(self):
        self._client = OpenAI()

    def _load_user_prompt(self, article_summary: dict) -> str:
        with open(ARTICLE_FROM_SUMMARY_PROMPT_TEMPLATE_PATH) as f:
            prompt_raw = f.read().strip()

        return prompt_raw.format(
            date=article_summary['date'],
            place_of_event=article_summary['place_of_event'],
            involved_individuals=article_summary['involved_individuals'],
            key_points_in_news=article_summary['key_points_in_news'],
            summary=article_summary['summary'],
        )

    def _parse_response(self, content: str):
        title_match = re.search(r'"title":\s*"([^"]+)"', content)
        subtitle_match = re.search(r'"subtitle":\s*"([^"]+)"', content)
        article_text_match = re.search(r'"article_text":\s*"([^"]+)"', content, re.DOTALL)

        title = title_match.group(1) if title_match else None
        subtitle = subtitle_match.group(1) if subtitle_match else None
        article_text = article_text_match.group(1).replace('\\n', '\n') if article_text_match else None

        return BaseArticle(title, subtitle, article_text)

    def write_article(self, article_summary: dict) -> BaseArticle:
        user_prompt = self._load_user_prompt(article_summary)

        chat_completion_text = self._client.chat.completions.create(
            messages=[
                {"role": "system", "content": "You are a professional article writer based on daily news."},
                {"role": "user", "content": user_prompt}
            ],
            model="gpt-4",
            max_tokens=4096,
            temperature=0.2
        )

        content = chat_completion_text.choices[0].message.content
        
        return self._parse_response(content)
