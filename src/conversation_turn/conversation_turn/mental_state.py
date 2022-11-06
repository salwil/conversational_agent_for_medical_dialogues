# -*- coding: utf-8 -*-

# answer.py

"""
Bachelor-Thesis: Conversational agent for querying orofacial pain patients

Salome Wildermuth
Matrikel-Nr: 10-289-544
University of Zurich
Institute for Computational Linguistics

- Data class for patient's mental state

"""
from enum import Enum
from src.repository.repository.mental_state_repo import mentalStates

class mentalState:
    def __init__(self, answer: str):
        self.answer = answer
        self.mentalState = mentalStates.NEUTRAL
        self.propability = 0.0

    def determine_mental_state(self):
        # TODO: determine mental state with bart-mnli based on given answer
        pass



