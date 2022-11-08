# -*- coding: utf-8 -*-

# qusetion_generation.py

"""
Bachelor-Thesis: Conversational agent for querying orofacial pain patients

Salome Wildermuth
Matrikel-Nr: 10-289-544
University of Zurich
Institute for Computational Linguistics

- Classes for translation

"""

from transformers import MarianMTModel, MarianTokenizer
import src.helpers.helpers.helpers as helpers

class Translator:
    def __init__(self, path_to_model: str):
        self.model = MarianMTModel.from_pretrained(path_to_model)
        self.tokenizer = MarianTokenizer.from_pretrained(path_to_model)

    def translate(self, text: list):
        translated = self.model.generate(**self.tokenizer(text, return_tensors="pt", padding=True))
        return [self.tokenizer.decode(t, skip_special_tokens=True) for t in translated][0]

class TranslatorDeEn(Translator):
    def __init__(self):
        model_path = helpers.get_project_path() + '/src/model/language_models/opus-mt-de-en-survey-answers/checkpoint-3500'
        super().__init__(model_path)

class TranslatorEnDe(Translator):
    def __init__(self):
        model_path = helpers.get_project_path() + '/src/model/language_models/opus-mt-en-de-survey-questions'
        super().__init__(model_path)

