from article_rewriter.article_manager import ArticleManager


article_manager = ArticleManager()


def write_from_raw_data(url: str):
    article = article_manager.rewrite_article_from_raw_data(url)
    print(f"Article from raw data:\n\n{article.text}\n\nAI SCORE: {article.ai_score}\n")


def write_from_base_article(url: str):
    article = article_manager.rewrite_article_from_base_article(url)
    print(f"Article from base article:\n\n{article.text}\n\nAI SCORE: {article.ai_score}\n")


def extract_event_info(url: str):
    event_info = article_manager.extract_event_info(url)
    print(event_info)


def main(url: str, from_raw_data: bool = True):
    if from_raw_data:
        write_from_raw_data(url)
    else:
        write_from_base_article(url)


if __name__ == "__main__":
    article_url = "https://www.cumhuriyet.com.tr/dunya/ikinci-intifadadan-bu-yana-bir-ilk-bati-seriada-zirhli-personel-2256336"

    write_from_raw_data(article_url)
    write_from_base_article(article_url)
    extract_event_info(article_url)
