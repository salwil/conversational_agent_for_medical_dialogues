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

class Answer:
    def __init__(self, answer: str):
        self.answer = answer
        self.answer_preprocessed = ' '
        self.relevance = 0.0
        self.number_of_usage = 0

        # References to other objects
        self.conversation_turn = None
