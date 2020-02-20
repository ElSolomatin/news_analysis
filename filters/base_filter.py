from abc import ABC

from templates.base_news_template import BaseNewsTemplate


class BaseFilter(ABC):

    def __init__(self):
        pass

    def is_valid(self, news: BaseNewsTemplate) -> bool:
        pass
