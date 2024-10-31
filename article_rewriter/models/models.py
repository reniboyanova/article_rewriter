import uuid


class RawData:
    def __init__(self, title, subtitle, text, ai_score=100) -> None:
        self.title = title
        self.subtitle = subtitle
        self.text = text
        self.ai_score = ai_score


class BaseArticle(RawData):
    def __init__(self, title, subtitle, text, ai_score=100) -> None:
        super().__init__(title, subtitle, text, ai_score)


class Article(BaseArticle):
    def __init__(self, title, subtitle, text, ai_score=100) -> None:
        super().__init__(title, subtitle, text, ai_score)


class Event:
    def __init__(self, main_event, type, subtype, description) -> None:
        self.uid = str(uuid.uuid4())
        self.main_event = main_event
        self.type = type
        self.subtype = subtype
        self.description = description
