import os


BASE_PROMPTS_DIR = 'article_rewriter/writing/prompts'
REWRITE_PROMPTS_DIR = os.path.join(BASE_PROMPTS_DIR, 'rewriting')
EVENT_INFO_PROMPTS_DIR = os.path.join(BASE_PROMPTS_DIR, 'event_info')
SUMMARY_PROMPT_TEMPLATE_PATH = os.path.join(BASE_PROMPTS_DIR, 'summary_user_prompt_template')
EVENT_INFO_PROMPT_TEMPLATE_PATH = os.path.join(BASE_PROMPTS_DIR, 'event_info_user_prompt_template')
ARTICLE_FROM_SUMMARY_PROMPT_TEMPLATE_PATH = os.path.join(BASE_PROMPTS_DIR, 'article_from_summary_user_prompt_template')

CUMHURIYET_DOMAIN = 'cumhuriyet.com.tr'
HABERTURK_DOMAIN = 'haberturk.com'
HURRIYET_DOMAIN = 'hurriyet.com.tr'
SOZCU_DOMAIN = 'sozcu.com.tr'
