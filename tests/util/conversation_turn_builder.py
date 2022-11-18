# -*- coding: utf-8 -*-

# conversation_builder.py

"""
Bachelor-Thesis: Conversational agent for querying orofacial pain patients

Salome Wildermuth
Matrikel-Nr: 10-289-544
University of Zurich
Institute for Computational Linguistics

- Class for building conversation turns

"""
from abc import abstractmethod, ABC
from unittest.mock import MagicMock

from conversation_turn.conversation_turn.turn import ConversationTurn
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
    def conversation_turn(self) -> None:
        pass



class ConversationBuilder(Builder):
    def __init__(self):
        self.reset()

    def reset(self):
        self._conversation_turn = ConversationTurn()

    def conversation_turn(self) -> Conversation:
        conversation_turn = self._conversation_turn
        self.reset()
        return conversation_turn


    def with_answer(self, content_en: str, number_of_usage = None, content_in_2nd_pers = None, content_with_hl = None):
        if number_of_usage:
            answer = Answer(content_en, number_of_usage)
        else:
            answer = Answer(content_en, 1)
        if content_in_2nd_pers:
            answer.content_in_2nd_pers = content_in_2nd_pers
        if content_with_hl:
            answer.content_with_hl = content_with_hl
        self._conversation.question_generator.set_answer(answer)
        return self