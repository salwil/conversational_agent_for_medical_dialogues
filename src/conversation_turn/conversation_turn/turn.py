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
from src.conversation.conversation.conversation import Conversation
from src.conversation_turn.conversation_turn.conversation_element import Answer
from src.repository.repository.repositories import AnswerRepository


class ConversationTurn:
    def __init__(self, turn_number, conversation: Conversation, patient_input: str):
        self.turn_number = turn_number

        # References to other objects
        self.mental_state = None
        self.patient_input = patient_input
        self.answer: Answer = None
        self.question = None
        self.conversation = conversation

    def process_input(self):
        preprocessed_answer = self.conversation.preprocessor.preprocess(self.patient_input,
                                                                        self.conversation.preprocessing_parameters)
        self.answer = Answer(self.patient_input, 1, preprocessed_answer)


    def write_turn_to_archive(self):
        archive_record = {'answer': self.patient_input, 'question': self.question}
        self.conversation_archive.write(self, archive_record)
