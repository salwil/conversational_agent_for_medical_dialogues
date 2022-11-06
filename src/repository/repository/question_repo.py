# -*- coding: utf-8 -*-

# question_repo.py

"""
Bachelor-Thesis: Conversational agent for querying orofacial pain patients

Salome Wildermuth
Matrikel-Nr: 10-289-544
University of Zurich
Institute for Computational Linguistics

- Repository containing questions

"""
from dataclasses import dataclass, field

@dataclass
class QuestionRepository:
    key: str # short (preprocessed question)
    answer_preprocessed: str # or list?
    relevance: float = field(init=False, repr=False)
    number_of_usage: int

    # References to other objects
    conversation_turn = None