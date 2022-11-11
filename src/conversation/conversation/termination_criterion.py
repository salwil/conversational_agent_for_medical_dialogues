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
from src.conversation.conversation.conversation import Conversation


class TerminationCriterion:
    def __init__(self):
        self.terminate_conversation = False

    def given(self):
        return self.terminate_conversation

    def update(self, conversation: Conversation):
        # do checks whether any termination criterion is reached, and if yes, set ongoing flag to False
        if conversation.current_turn.turn_number > 20:
            self.terminate_conversation = True
