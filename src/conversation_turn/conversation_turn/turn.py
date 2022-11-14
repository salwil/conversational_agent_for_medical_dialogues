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
from src.conversation_turn.conversation_turn.conversation_element import Answer, Question, QuestionType


class ConversationTurn:
    def __init__(self, turn_number:int, conversation: Conversation, patient_input: str):
        self.turn_number = turn_number

        # References to other objects
        self.mental_state = None
        self.patient_input = patient_input
        self.generated_question: str = None
        self.answer: Answer = None
        self.question: Question = None
        self.conversation = conversation
        self.preprocessor = conversation.preprocessor
        self.nlp = conversation.nlp

    def process_question_and_answer_for_patient_profile(self, question: str):
        """
        Here the questions are predefined, so the sentiment analysis and question generation steps can be skipped,
        also the question must not be stored in the question repository, it was already loaded when the application
        started.
        :return:
        """
        self.__create_answer_object_and_store()
        self.generated_question = question
        self.__write_turn_to_archive()

    def process_answer_and_create_follow_up_question(self):
        self.__predict_mental_state()
        self.__create_answer_object_and_store()
        self.__generate_question()
        self.__create_question_object_and_store()
        self.__write_turn_to_archive()

    def __create_answer_object_and_store(self):
        """
        Creates an answer object and stores it in the corresponding repository
        :return:
        """
        self.answer = Answer(self.patient_input, 1)
        # as soon as we have created the answer object, we have to update the QuestionGenerator object with it
        self.conversation.question_generator.set_answer(self.answer)
        self.conversation.preprocessor.preprocess(self.answer, self.conversation.preprocessing_parameters)
        self.conversation\
            .data_loader\
            .store_conversation_element('answer_repo', self.answer)

    def __create_question_object_and_store(self):
        """
        Creates an question object and stores it in the corresponding repository
        :param text: question content (original generated question, not preprocessed)
        :return:
        """
        self.question = Question(self.generated_question, 1, QuestionType.GENERATED)
        self.conversation.preprocessor.preprocess(self.question, self.conversation.preprocessing_parameters)
        self.conversation\
            .data_loader\
            .store_conversation_element('question_repo', self.question)

    def __predict_mental_state(self):
        self.mental_state = self.conversation.sentiment_detector.predict_mental_state(self.patient_input)

    def __generate_question(self):
        print(self.turn_number)
        if self.turn_number % 3 == 0:
            # for variety we enforce one of our preferred interrogative pronouns, every third turn.
            self.generated_question = self.conversation.question_generator.generate_with_highlight()
        else:
            self.generated_question = self.conversation.question_generator.generate()

    def __german_to_english(self, text):
        self.conversation.translator_de_en.translate(text)

    def __english_to_german(self, text):
        self.conversation.translator_en_de.translate(text)

    def __write_turn_to_archive(self):
        archive_record = {'answer': self.patient_input, 'question': self.generated_question}
        self.conversation.conversation_archive.write(archive_record)
