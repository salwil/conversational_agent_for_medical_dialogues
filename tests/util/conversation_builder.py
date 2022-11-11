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

from src.conversation.conversation.conversation import Conversation
from src.conversation_turn.conversation_turn.conversation_element import Question, ProfileQuestion


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

    def with_profile_question(self, question: ProfileQuestion) -> None:
        self._conversation.data_loader.profile_question_repo.questions[question.content_preprocessed] = question
        return self


    def with_mandatory_question(self, question: Question) -> None:
        self._conversation.data_loader.mandatory_question_repo.questions[question.content_preprocessed] = question
        return self


