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
    start_question = 'Hello, welcome, blabla'
    answer = print(start_question)
    for profile_question in conversation.data_loader.profile_question_repo:
        ct = ConversationTurn(turn_number, conversation, answer)
        ct.process_question_and_answer_for_patient_profile(profile_question.content)
        turn_number += 1
    next_question = 'Eingangsfrage (tbd).'
    answer = print(next_question)
    while termination_criterion.verify():
        ct = ConversationTurn(turn_number, conversation, answer)
        ct.process_answer_and_create_follow_up_question()
        next_question = ct.generated_question
        answer = print(next_question)
        turn_number += 1