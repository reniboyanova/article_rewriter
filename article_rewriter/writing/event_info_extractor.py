import json
import os
from typing import Dict

from article_rewriter.constants import *
from article_rewriter.models.models import RawData

from openai import OpenAI


MODEL = "gpt-4o"


class EventInfoExtractor:
    def __init__(self, model: str = MODEL):
        self._client = OpenAI()
        self._model = model

        self._prompts = self._load_prompts()

    def _load_prompts(self) -> Dict[str, str]:
        prompts = {}

        file_names = os.listdir(EVENT_INFO_PROMPTS_DIR)
        for fn in file_names:
            file_path = os.path.join(EVENT_INFO_PROMPTS_DIR, fn)
            with open(file_path) as f:
                prompts[fn] = f.read().strip()

        return prompts

    def _load_user_prompt(self, prompt, raw_data):
        with open(EVENT_INFO_PROMPT_TEMPLATE_PATH) as f:
            prompt_raw = f.read().strip()

        return prompt_raw.format(prompt=prompt, title=raw_data.title, subtitle=raw_data.subtitle, text=raw_data.text)

    def _extract_event_json(self, raw_data: RawData, prompt: str):
        user_prompt = self._load_user_prompt(prompt, raw_data)

        chat_completion_text = self._client.chat.completions.create(
            messages=[
                {"role": "system", "content": "You are a skilled news redactor."},
                {"role": "user", "content": user_prompt},
            ],
            model=self._model,
            max_tokens=4096,
            temperature=0.8,
            response_format={"type": "json_object"}
        )

        res = chat_completion_text.choices[0].message.content.strip()
        return json.loads(res)

    def extract_event_info(self, raw_data: RawData):
        all_data = {}

        for prompt_type, prompt in self._prompts.items():
            all_data[prompt_type] = self._extract_event_json(raw_data, prompt)

        return all_data
