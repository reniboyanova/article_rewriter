from typing import Union

import json

from article_rewriter.models import RawData


class BaseParser:
    def extract_raw_data(
            self,
            soup,
            title_tag="headline",
            anonse_tag="description",
            article_body_tag="p",
    ) -> Union[RawData, None]:
        script_tag = soup.find('script', type='application/ld+json')
        if not script_tag:
            return None

        try:
            json_data = json.loads(script_tag.string)
            title = json_data.get(title_tag, '')
            subtitle = json_data.get(anonse_tag, '')
            paragraphs = soup.find_all(article_body_tag)
            article_text = ' '.join([p.get_text() for p in paragraphs])
            return RawData(title, subtitle, article_text)
        except Exception as e:
            print(f"Error during data extraction. Exception: {e}")
            return None
