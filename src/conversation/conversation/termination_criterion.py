# -*- coding: utf-8 -*-

# termination_criterion.py

"""
Bachelor-Thesis: Conversational agent for querying orofacial pain patients

Salome Wildermuth
Matrikel-Nr: 10-289-544
University of Zurich
Institute for Computational Linguistics

- Class for modeling termination criteria of a topic conversation or of the whole conversation

"""


class TerminationCriterion:
    def __init__(self):
        self.conversation_ongoing = True

    def ongoing(self):
        return self.conversation_ongoing