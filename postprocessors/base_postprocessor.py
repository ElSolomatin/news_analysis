from abc import ABC


class BasePostprocessor(ABC):

    def __init__(self):
        pass

    def run(self, news, result):
        pass
