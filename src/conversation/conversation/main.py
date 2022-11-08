# -*- coding: utf-8 -*-

# main.py

"""
Bachelor-Thesis: Conversational agent for querying orofacial pain patients

Salome Wildermuth
Matrikel-Nr: 10-289-544
University of Zurich
Institute for Computational Linguistics

- main module for maintaining conversation with user

"""

from .cli import CLI
from .conversation import Conversation
from .termination_criterion import TerminationCriterion
from src.conversation_turn.conversation_turn.turn import ConversationTurn

cli = CLI()
conversation = Conversation()
termination_criterion = TerminationCriterion()


def main():
    cli.talk()
    conversation.load_repositories()
    conversation.load_models()
    maintain_conversation()


def maintain_conversation():
    turn_number = 1
    while termination_criterion.verify():
        ConversationTurn(turn_number, conversation)
        turn_number += 1
