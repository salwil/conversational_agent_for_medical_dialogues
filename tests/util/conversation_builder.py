# -*- coding: utf-8 -*-

# conversation_builder.py

"""
Bachelor-Thesis: Conversational agent for querying orofacial pain patients

Salome Wildermuth
Matrikel-Nr: 10-289-544
University of Zurich
Institute for Computational Linguistics

- Class for building conversations

"""
from abc import abstractmethod, ABC
from unittest.mock import MagicMock

from model.model.question_generation import QuestionGenerator
from src.conversation.conversation.conversation import Conversation
from src.conversation_turn.conversation_turn.conversation_element import Question, PredefinedQuestion, QuestionType, \
    Answer, QuestionIntro


class Builder(ABC):
    """
    The Builder interface specifies methods for creating the different parts of
    the Product objects.
    """

    @property
    @abstractmethod
    def conversation(self) -> None:
        pass

    @abstractmethod
    def with_profile_question(self) -> None:
        pass

    @abstractmethod
    def with_mandatory_question(self) -> None:
        pass

    """
    @abstractmethod
    def with_generated_question(self) -> None:
        pass
    """


class ConversationBuilder(Builder):
    def __init__(self):
        self.reset()

    def reset(self):
        self._conversation = Conversation()

    def conversation(self) -> Conversation:
        conversation = self._conversation
        self.reset()
        return conversation

    def with_profile_question(self, question_de: str, question_en: str, preprocessed_en: str) -> None:
        profile_question = PredefinedQuestion(question_de, 1, question_de, QuestionType.PROFILE)
        profile_question.content_preprocessed = preprocessed_en
        self._conversation.data_loader.profile_question_repo.questions[profile_question.content_preprocessed]\
            = profile_question
        return self

    def with_mandatory_question(self, question_de: str, question_en: str, preprocessed_en: str) -> None:
        mandatory_question = PredefinedQuestion(question_de, 1, question_de, QuestionType.PROFILE)
        mandatory_question.content_preprocessed = preprocessed_en
        #self._conversation.data_loader.profile_question_repo.questions[mandatory_question.content_preprocessed]\
        #    = mandatory_question
        self._conversation.data_loader.mandatory_question_repo.questions[mandatory_question.content_preprocessed]\
            = mandatory_question
        return self

    def with_question_intro_repository(self):
        self._conversation.data_loader.question_intro_repo.mental_states = {}
        return self

    def with_question_intro(self, mental_state: str, question_intro_de: str, question_intro_en: str) -> None:
        question_intro = QuestionIntro(question_intro_en, 0, question_intro_de, mental_state)
        self._conversation.data_loader.question_intro_repo.mental_states[mental_state] = [question_intro]
        return self

    def with_question_generator(self, preprocessor = None, nlp = None):
        if preprocessor:
            if nlp:
                self._conversation.question_generator = QuestionGenerator(preprocessor, nlp)
            else:
                self._conversation.question_generator = QuestionGenerator(preprocessor, MagicMock())
        else:
            self._conversation.question_generator = QuestionGenerator(MagicMock(), MagicMock())
        if self._conversation.data_loader.question_intro_repo.mental_states:
            self._conversation.question_generator.update_question_intro_repository(
                self._conversation.data_loader.question_intro_repo)
        if self._conversation.data_loader.generated_question_repo.questions:
            self._conversation.question_generator.update_generated_questions_repository(
                self._conversation.data_loader.generated_question_repo)
        return self

    """ Das wird alles gemacht mit QuestionGenerator Instantiierung
    def with_question_generation_rules(self, preprocessor = None, nlp = None):
        answer = self._conversation.question_generator.answer
        if preprocessor:
            if nlp:
                self._conversation.question_generator.question_generation_rules = \
                    QuestionGenerationRules(preprocessor, nlp, answer)
            else:
                self._conversation.question_generator.question_generation_rules = \
                    QuestionGenerationRules(preprocessor, MagicMock())
        else:
            self._conversation.question_generator.question_generation_rules = \
                QuestionGenerationRules(MagicMock(), MagicMock())

        return self
        """

    def with_answer(self, content_en: str, number_of_usage = None, content_in_2nd_pers = None, content_with_hl = None, mental_state = None, turn_number = None):
        if number_of_usage:
            if turn_number:
                answer = Answer(content_en, number_of_usage, turn_number)
            else:
                answer = Answer(content_en, number_of_usage, 1)
        else:
            answer = Answer(content_en, 1, 1)
        if content_in_2nd_pers:
            answer.content_in_2nd_pers = content_in_2nd_pers
        if content_with_hl:
            answer.content_with_hl = content_with_hl
        if mental_state:
            answer.mental_state = mental_state
        self._conversation.question_generator.set_answer(answer)
        return self



    """
    def with_generated_question(self, question_en: str, preprocessed_en) -> None:
        generated_question = Question(question_en, 0, QuestionType.GENERATED)
        generated_question.content_preprocessed = preprocessed_en
        self._conversation.data_loader.generated_question_repo.questions[generated_question.content_preprocessed] \
            = generated_question
        return self
        """




