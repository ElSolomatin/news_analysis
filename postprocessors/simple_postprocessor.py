from postprocessors.base_postprocessor import BasePostprocessor


class SimplePostprocessor(BasePostprocessor):

    def __init__(self):
        super().__init__()

    def run(self, news, result):
        pass
