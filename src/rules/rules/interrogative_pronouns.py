# -*- coding: utf-8 -*-

# conversation_element.py

"""
Bachelor-Thesis: Conversational agent for querying orofacial pain patients

Salome Wildermuth
Matrikel-Nr: 10-289-544
University of Zurich
Institute for Computational Linguistics

- Data class for adverbials: locality, temporality, modality, causality

"""
from dataclasses import dataclass, field
from enum import Enum

"""
    CARDINAL = 'how many',  # Numerals that do not fall under another type.
    DATE = 'when',  # Absolute or relative dates or periods
    TIME = 'when',  # Times smaller than a day
    EVENT = 'what',  # Named hurricanes, battles, wars, sports events, etc.
    GPE = '?',  # Countries, cities, states.
    LOC = 'where',  # Non-GPE locations, mountain ranges, bodies of water.
    NORP = 'where',
    ORDINAL = '?',  # “first”, “second”, etc.
    ORG = 'who',  # Companies, agencies, institutions, etc.
    PERSON = 'who',  # People, including fictional.
    WORK_OF_ART = '?'  # Titles of books, songs, etc.
    QUANTITY = 'how many'  # Measurements, as of weight or distance.
    MONEY = 'how much'  # Monetary values, including unit.
    PERCENT = 'how often'  # Percentage, including ”%“.
    LANGUAGE = '?'  # Any named language.
    PRODUCT = 'what'  # Objects, vehicles, foods, etc. (Not services.)
    FAC = 'where'  # Buildings, airports, highways, bridges, etc.
    """

class Position(Enum):
    EOS = 'eos',
    BOS = 'bos'

@dataclass
class InterrogativePronoun():
    interrogative_pronouns_with_trigger = {
        'why': ('because', Position.EOS),
        'when': ('during', Position.EOS),
        'where': ('at the University Hospital', Position.EOS),
        'what': ('Your jaw', Position.BOS),
        'who': ('Your Doctor', Position.BOS),
        'how': ('in form of', Position.EOS),
        'how often': ('once a day', Position.BOS),
        'how many': ('5 of', Position.BOS),
        'since': ('since one year', Position.EOS)
    }

    ne_type_for_interrogative_pronouns = {
        'CARDINAL': ['how many', 'how often'],
        'DATE': ['when', 'how often'],
        'TIME': ['when','how often'],
        'EVENT': ['what', 'where'],
        'GPE': ['where', 'what'],
        'LOC': ['where'],
        'NORP': ['where'],
        'FAC': ['where'],
        'PERSON': ['who'],
        'QUANTITY': ['how many'],
        'PRODUCT': ['what', 'which'],
    }

    """
    ne_type_for_interrogative_pronouns = {
        'CARDINAL': {'how many': 0, 'how often': 0},
        'DATE': {'when': 0, 'how often': 0},
        'TIME': {'when': 0, 'how often': 0},
        'EVENT': {'what': 0, 'where': 0},
        'GPE': {'where': 0},
        'LOC': {'where': 0},
        'NORP': {'where': 0},
        'FAC': {'where': 0},
        'PERSON': {'who': 0},
        'QUANTITY': {'how many': 0},
        'PRODUCT': {'what': 0, 'which': 0},
    }
    
    ne_type_for_interrogative_pronouns = {
        NamedEntityTypes.CARDINAL: {'how many': 0, 'how often': 0},
        NamedEntityTypes.DATE: {'when': 0, 'how often': 0},
        NamedEntityTypes.TIME: {'when': 0, 'how often': 0},
        NamedEntityTypes.EVENT: {'what': 0, 'where': 0},
        NamedEntityTypes.GPE: {'where': 0},
        NamedEntityTypes.LOC: {'where': 0},
        NamedEntityTypes.NORP: {'where': 0},
        NamedEntityTypes.FAC: {'where': 0},
        NamedEntityTypes.PERSON: {'who': 0},
        NamedEntityTypes.QUANTITY: {'how many': 0},
        NamedEntityTypes.PRODUCT: {'what': 0, 'which': 0},
    }
    """

