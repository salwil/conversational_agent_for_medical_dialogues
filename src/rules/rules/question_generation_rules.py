# -*- coding: utf-8 -*-

# qusetion_generation_rules.py

"""
Bachelor-Thesis: Conversational agent for querying orofacial pain patients

Salome Wildermuth
Matrikel-Nr: 10-289-544
University of Zurich
Institute for Computational Linguistics

- Class for all the rules that are involved into the rulebased part of question generation

"""
from pprint import pprint
from enum import Enum
import en_core_web_sm

class NamedEntityTypes(Enum):
    CARDINAL = 'cardinal', # Numerals that do not fall under another type.
    DATE = 'when', # Absolute or relative dates or periods
    TIME = 'when', # Times smaller than a day
    EVENT = 'what', # Named hurricanes, battles, wars, sports events, etc.
    GPE = '?', # Countries, cities, states.
    LOC = 'where', # Non-GPE locations, mountain ranges, bodies of water.
    NORP = 'where',
    ORDINAL = '?', #“first”, “second”, etc.
    ORG = 'who', # Companies, agencies, institutions, etc.
    PERSON = 'who', # People, including fictional.
    WORK_OF_ART = '?' #Titles of books, songs, etc.
    QUANTITY = 'how many' # Measurements, as of weight or distance.
    MONEY = 'how much'# Monetary values, including unit.
    PERCENT = 'how often' # Percentage, including ”%“.
    LANGUAGE = '?' # Any named language.
    PRODUCT = 'what' # Objects, vehicles, foods, etc. (Not services.)
    FAC = 'where' # Buildings, airports, highways, bridges, etc.


class QuestionGenerationRules:
    def __init__(self):
        self.last_answer = None
        # inject this!! currently loaded twice (once in preprocessor and again here)
        self.nlp = en_core_web_sm.load()

    def determine_sentence_adverbiale(self, text):
        doc = self.nlp(text)
        named_entity_types = set(ne.value for ne in NamedEntityTypes)
        found_entities = []
        for label in doc.ents:
            if label[1] in named_entity_types:
                found_entities.append(label[1])
                

        pprint([(X.text, X.label_) for X in doc.ents])