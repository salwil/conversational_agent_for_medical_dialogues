# -*- coding: utf-8 -*-

# conversation_element.py

"""
Bachelor-Thesis: Conversational agent for querying orofacial pain patients

Salome Wildermuth
Matrikel-Nr: 10-289-544
University of Zurich
Institute for Computational Linguistics

- Data class for answer (patient's input)

"""
from dataclasses import dataclass, field
from enum import Enum
from .turn import Turn

@dataclass
class ConversationElement:
    content: str
    content_preprocessed: list = field(init=False, repr=False)
    content_tokenized: list = field(init=False, repr=False)
    number_of_usage: int

    # Reference to other objects
    conversation_turn: Turn = field(init=False, repr=False)

@dataclass
class Answer(ConversationElement):
    # when instantiating an oject of answers, the preprocessed content has to be provided already:
    content_preprocessed: list
    relevance: float = field(init=False, repr=False)

class ConversationIntro(ConversationElement):
    def __init__(self):
        #mental state that asks for this intro
        self.mental_state = None

class QuestionType(Enum):
    INTRO = 'intro'
    MANDATORY = 'mandatory'
    FALLBACK = 'fallback'
    MOREDETAIL = 'moredetail'

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