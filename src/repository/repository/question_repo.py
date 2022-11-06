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
    questions: dict
