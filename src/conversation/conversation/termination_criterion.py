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

from conversation_turn.turn import ConversationTurn


class TerminationCriterion:
    def __init__(self):
        self.terminate = False

    def given(self):
        return self.terminate


class TerminationCriterionForConversation(TerminationCriterion):
    def update(self, current_turn: ConversationTurn):
        # do checks whether any termination criterion is reached, and if yes, set ongoing flag to False
        if current_turn.turn_number > 20:
            self.terminate = True
        # if same topic has occurred in x conversation turns we

    def check_user_terminate(self, user_input):
        if user_input == 'q!' or user_input == 'quit!':
            self.terminate = True
