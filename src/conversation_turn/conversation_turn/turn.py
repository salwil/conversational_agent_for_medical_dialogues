# -*- coding: utf-8 -*-

# question.py

"""
Bachelor-Thesis: Conversational agent for querying orofacial pain patients

Salome Wildermuth
Matrikel-Nr: 10-289-544
University of Zurich
Institute for Computational Linguistics

- Data class for conversation turn

"""

class Turn:
    def __init__(self, turn_number):
        self.turn_number = turn_number;

        # References to other objects
        self.mental_state = None
        self.input = None
