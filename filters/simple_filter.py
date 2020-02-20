from filters.base_filter import BaseFilter
from templates.base_news_template import BaseNewsTemplate


class SimpleFilter(BaseFilter):
    __slots__ = [
        'searched_words',
        'common_words'
    ]

    def __init__(self):
        super().__init__()

        self.searched_words = []
        self.common_words = [
            'inc', 'corp', 'group',
            '&', 'holdings', 'co',
            'corporation', 'technologies', 'corporation',
            'pharmaceuticals', 'energy', 'therapeutics',
            'financial', 'international', 'systems',
            'industries', 'привилегированные', 'акции',
            'health', 'global', 'company',
            'services', 'the', 'new', 'a']

        with open('filters/files/positions.txt', 'r') as f:

            for line in f.read().splitlines():

                for words in line.split('|'):

                    for word in words.split(' '):

                        word = word.lower()

                        if word not in self.common_words \
                                and word not in self.searched_words:

                            self.searched_words.append(word)

    def is_valid(self, news: BaseNewsTemplate) -> bool:
        return len([word for word in news.headline.split() if word.lower() in self.searched_words]) > 0
