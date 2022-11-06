# -*- coding: utf-8 -*-

# question.py

"""
Bachelor-Thesis: Conversational agent for querying orofacial pain patients

Salome Wildermuth
Matrikel-Nr: 10-289-544
University of Zurich
Institute for Computational Linguistics

- Data class for question

"""

from enum import Enum
from dataclasses import dataclass, field
from conversation_element import Answer
from turn import Turn

class Intro:
    def __init__(self):
        self.phrase = ' '
        self.number_of_usage = 0
        #mental state that asks for this intro
        self.mental_state = None

class QuestionType(Enum):
    INTRO = 'intro'
    MANDATORY = 'mandatory'
    FALLBACK = 'fallback'
    MOREDETAIL = 'moredetail'

@dataclass
class Question:
    question: str
    question_preprocessed: str = field(init = False, repr = False)
    probability: float = field(init = False, repr = False)
    generated = False
    asked = False
    question_type: QuestionType

    # References to other objects
    intro: Intro = field(init = False, repr = False)
    answer: Answer = field(init = False, repr = False)
    #follow_up_question: Question = field(init = False, repr = False)
    conversation_turn: Turn = field(init = False, repr = False)

