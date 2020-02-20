from abc import ABC


class BasePredictor(ABC):
    def __init__(self):
        pass

    def predict(self, headline: str):
        pass
