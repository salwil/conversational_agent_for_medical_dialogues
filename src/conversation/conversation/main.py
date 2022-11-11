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

from src.conversation.conversation.cli import CLI
from src.conversation.conversation.conversation import Conversation
from src.conversation.conversation.termination_criterion import TerminationCriterion
from src.conversation_turn.conversation_turn.turn import ConversationTurn

cli = CLI()



def main():
    #cli.talk()
    conversation = Conversation()
    conversation.load_repositories()
    conversation.load_models()
    maintain_conversation(conversation)


def maintain_conversation(conversation):
    termination_criterion = TerminationCriterion()
    turn_number = 1
    start_question = 'Hello, welcome, blabla'
    print(start_question)
    answer = input()
    for profile_question in conversation.data_loader.profile_question_repo.questions.values():
        ct = ConversationTurn(turn_number, conversation, answer)
        print(profile_question.content)
        ct.process_question_and_answer_for_patient_profile(profile_question.content)
        answer = input()
        turn_number += 1
    next_question = 'Eingangsfrage (tbd).'
    print(next_question)
    answer = input()
    while not termination_criterion.given():
        ct = ConversationTurn(turn_number, conversation, answer)
        ct.process_answer_and_create_follow_up_question()
        next_question = ct.generated_question
        print(next_question)
        answer = input()
        turn_number += 1

if __name__ == "__main__":
    main()
