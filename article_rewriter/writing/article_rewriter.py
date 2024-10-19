import os
from typing import Union

from openai import OpenAI

from article_rewriter.constants import *
from article_rewriter.models import Article
from article_rewriter.writing.ai_detection.ai_detector import AIDetector


class GPTRewriterManager:
    def __init__(self, model: str = 'gpt-4o'):
        self._client = OpenAI()
        self._model = model
        self._ai_detector = AIDetector()

    def _load_prompts_multiple_rewrite(self):
        prompts = []

        prompt_file_names = os.listdir(REWRITE_PROMPTS_DIR)
        for fn in prompt_file_names:
            file_path = os.path.join(REWRITE_PROMPTS_DIR, fn)
            with open(file_path) as f:
                prompts.append(f.read().strip())

        return prompts

    def _rewrite(self, content, max_tokens=4096, temperature=0.8) -> str:
        chat_completion_text = self._client.chat.completions.create(
            messages=[
                {"role": "system", "content": "You are a skilled content writer who creates human-like articles."},
                {"role": "user", "content": content}
            ],
            model=self._model,
            max_tokens=max_tokens,
            temperature=temperature
        )

        return chat_completion_text.choices[0].message.content.strip()

    def write(self, data) -> Union[Article, None]:
        prompt_list = self._load_prompts_multiple_rewrite()

        best_result = {
            'score': None,
            'rewritten_title': None,
            'rewritten_anonse': None,
            'rewritten_text': None,
        }

        for prompt in prompt_list:
            title_prompt = f"{prompt}\n\nRewrite the title:\n{data.title}"
            anonse_prompt = f"{prompt}\n\nRewrite the subtitle (anonse):\n{data.subtitle}"
            text_prompt = f"{prompt}\n\nRewrite the article text:\n{data.text}"

            rewritten_title = self._rewrite(title_prompt)
            rewritten_anonse = self._rewrite(anonse_prompt)
            rewritten_text = self._rewrite(text_prompt)

            ai_detection_result = self._ai_detector.get_ai_detection_edenai(rewritten_text)
            if ai_detection_result is None:
                continue

            ai_score = ai_detection_result['ai_score']
            if ai_score < 50:
                return Article(rewritten_title, rewritten_anonse, rewritten_text, ai_score)

            if best_result['score'] is None or best_result['score'] > ai_score:
                best_result = {
                    'score': ai_score,
                    'rewritten_title': rewritten_title,
                    'rewritten_anonse': rewritten_anonse,
                    'rewritten_text': rewritten_text,
                }

        if best_result['score'] is None:
            return None

        return Article(
            best_result['rewritten_title'],
            best_result['rewritten_anonse'],
            best_result['rewritten_text'],
            best_result['ai_score'],
        )
