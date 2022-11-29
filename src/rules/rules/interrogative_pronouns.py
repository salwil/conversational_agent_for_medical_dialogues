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

class Position(Enum):
    EOS = 'eos',
    BOS = 'bos'

@dataclass
class InterrogativePronoun():
    interrogative_pronouns_with_trigger = {
        #'why': ('because', Position.EOS),
        'when': ('during', Position.EOS),
        'where': ('at the hospital', Position.EOS),
        'what': ('Something', Position.BOS),
        'who': ('Somebody', Position.BOS),
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


