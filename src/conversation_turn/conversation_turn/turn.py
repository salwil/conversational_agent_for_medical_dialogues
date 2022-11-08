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
from src.conversation_turn.conversation_turn.conversation_element import Answer, Question


class ConversationTurn:
    def __init__(self, turn_number, conversation: Conversation, patient_input: str):
        self.turn_number = turn_number

        # References to other objects
        self.mental_state = None
        self.patient_input = patient_input
        self.answer: Answer = None
        self.question: Question = None
        self.conversation = conversation

    def capture_input(self):
        self.conversation.data_loader.store_data_in_repository(self.input)

    def determine_mental_state(self):
        self.conversation.sentiment_detector.predict_mental_state(self.patient_input)

    def generate_question(self):
        self.conversation.question_generator.generate(self.patient_input)


    def write_turn_to_archive(self):
        archive_record = {'answer': self.patient_input, 'question': self.question}
        self.conversation_archive.write(self, archive_record)
