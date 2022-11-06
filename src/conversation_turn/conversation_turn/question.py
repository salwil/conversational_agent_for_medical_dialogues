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

from answer import Answer

class Intro:
    def __init__(self):
        self.phrase = ' '
        self.number_of_usage = 0
        #mental state that asks for this intro
        self.mental_state = None

class Question:
    def __init__(self, question: str, answer: Answer, intro: Intro):
        self.question = question
        self.question_preprocessed = ' '
        self.probability = ' '
        self.generated = False
        self.asked = False

        # References to other objects
        self.intro = intro
        self.answer = answer
        self.follow_up_question = None #Of type question
        self.conversation_turn = None

