# -*- coding: utf-8 -*-

# answer.py

"""
Bachelor-Thesis: Conversational agent for querying orofacial pain patients

Salome Wildermuth
Matrikel-Nr: 10-289-544
University of Zurich
Institute for Computational Linguistics

- Data class for answer (patient's input)

"""
from dataclasses import dataclass, field

@dataclass
class Answer:
    answer: str
    answer_preprocessed: str # or list?
    relevance: float = field(init=False, repr=False)
    number_of_usage: int

    # References to other objects
    conversation_turn = None
