# -*- coding: utf-8 -*-

# conversation_element.py

"""
Bachelor-Thesis: Conversational agent for querying orofacial pain patients

Salome Wildermuth
Matrikel-Nr: 10-289-544
University of Zurich
Institute for Computational Linguistics

- Data class for conversation elements: answer (patient's input), question, question intro, question type

"""
from dataclasses import dataclass, field
from enum import Enum

from conversation_turn.conversation_turn.topic import Topic

@dataclass
class ConversationElement:
    content: str
    content_preprocessed: list = field(init=False, repr=False)
    content_tokenized: list = field(init=False, repr=False)
    number_of_usage: int

@dataclass
class Answer(ConversationElement):
    # when instantiating an oject of answers, the preprocessed content has to be provided already:
    # content_preprocessed: list
    content_in_2nd_pers: str = field(init=False, repr = False)
    relevance: float = field(init=False, repr=False)
    topic: Topic = field(init=False, repr=False)

class ConversationIntro(ConversationElement):
    def __init__(self):
        #mental state that asks for this intro
        self.mental_state = None

class QuestionType(Enum):
    PROFILE = 'profile'
    MANDATORY = 'mandatory'
    FALLBACK = 'fallback'
    MOREDETAIL = 'moredetail'
    GENERATED = 'generated'


@dataclass
class Question(ConversationElement):
    probability: float = field(init = False, repr = False)
    generated = False
    asked = False
    question_type: QuestionType

    # References to other objects
    intro: ConversationIntro = field(init = False, repr = False)
    answer: Answer = field(init = False, repr = False)
    #follow_up_question: Question = field(init = False, repr = False)


@dataclass
class PredefinedQuestion(Question):
    """
    Special class for the predefined questions (profile, mandatory and more detail questions). They are available in
    english as well as in german in the file they're read from.
    """
    content_in_german: str