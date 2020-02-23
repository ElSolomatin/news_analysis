import copy
import json
import logging
import os
import re

import nltk
import numpy as np
import torch
from nltk import WordNetLemmatizer

from predictors.base_predictor import BasePredictor
from predictors.cnn.model import CNNText


class CNNPredictor(BasePredictor):
    __slots__ = [
        'model',
        'models',
        'word2idx',
        'stop_words',
        'models_path'
    ]

    def __init__(self, inputs_path: str):
        super().__init__()

        self.model = CNNText()

        self.models_path = os.path.join(inputs_path, 'models/')
        self.word2idx_path = os.path.join(inputs_path, 'word2idx')
        self.stop_words_path = os.path.join(inputs_path, 'stopWords')
        if torch.cuda.is_available():
            self.model.cuda()

        self.models, self.word2idx, self.stop_words = self.__predictor_preprocess()

    def predict(self, text: str):

        tokens = self.__tokenize_news(text, self.stop_words)

        tokens = [self.word2idx[t] if t in self.word2idx else self.word2idx['UNKNOWN'] for t in tokens]

        if len(tokens) < 5 or tokens == [self.word2idx['UNKNOWN']] * len(
                tokens):  # tokens cannot be too short or unknown
            return 'Unknown'
        else:
            feature = torch.LongTensor([tokens])

            logits = []

            for model in self.models:

                model.eval()

                if torch.cuda.is_available():
                    feature = feature.cuda()

                logit = model(feature)

                predictor = torch.exp(logit[:, 1]) / (torch.exp(logit[:, 0]) + torch.exp(logit[:, 1]))

                logits.append(predictor.item())

            signal = self.__signals(np.mean(logits))

        return signal

    def __tokenize_news(self, headline, stop_words):
        tokens = nltk.word_tokenize(headline)
        tokens = list(map(self.__unify_word, tokens))
        tokens = list(map(self.__unify_word, tokens))  # some words fail filtering in the 1st time
        tokens = list(map(self.__digit_filter, tokens))
        tokens = list(map(self.__unify_word_meaning, tokens))
        tokens = [t for t in tokens if t not in stop_words and t != ""]
        return tokens

    @staticmethod
    def __unify_word(word):  # went -> go, apples -> apple, BIG -> big
        """unify verb tense and noun singular"""
        ADJ, ADJ_SAT, ADV, NOUN, VERB = 'a', 's', 'r', 'n', 'v'
        for wt in [ADJ, ADJ_SAT, ADV, NOUN, VERB]:
            try:
                word = WordNetLemmatizer().lemmatize(word, pos=wt)
            except:
                pass
        return word.lower()

    @staticmethod
    def __digit_filter(word):
        check = re.match(r'\d*\.?\d*', word).group()
        if check == '':
            return word
        else:
            return ''

    @staticmethod
    def __unify_word_meaning(word):
        if word in ["bigger-than-expected", "higher-than-expected", "better-than-expected", "stronger-than-expected"]:
            return "better"
        elif word in ["smaller-than-expected", "lower-than-expected", "weaker-than-expected", "worse-than-expected"]:
            return "lower"
        elif word in ["no", "not", "n't"]:
            return "not"
        else:
            return word

    def __predictor_preprocess(self):
        # load trained thinning samples (Bayesian CNN models) from input/models/

        logging.info('Predictor preprocess start...')

        models = []

        for num, each_model in enumerate(os.listdir(self.models_path)):

            if torch.cuda.is_available():
                self.model.load_state_dict(torch.load(self.models_path
                                                      + each_model))
            else:
                self.model.load_state_dict(torch.load(self.models_path
                                                      + each_model, map_location=lambda storage, loc: storage))
            models.append(copy.deepcopy(self.model))
            if num > 30:  # in case memory overloads
                break

        with open(self.word2idx_path, 'r') as file:
            word2idx = json.load(file)

        stop_words = set()

        with open(self.stop_words_path) as file:
            for word in file:
                stop_words.add(word.strip())

        logging.info('Predictor preprocess was end')

        return models, word2idx, stop_words

    @staticmethod
    def __signals(digit):

        strong_signal = 0.4

        unknown_threshold = 0.05

        if digit > 0.5 + strong_signal:
            return 'Strong Buy'
        elif digit > 0.5 + unknown_threshold:
            return 'Buy'
        elif digit > 0.5 - unknown_threshold:
            return 'Unknown'
        elif digit > 0.5 - strong_signal:
            return 'Sell'
        else:
            return 'Strong Sell'
