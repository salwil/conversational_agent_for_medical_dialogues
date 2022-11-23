# -*- coding: utf-8 -*-

# repositories.py

"""
Bachelor-Thesis: Conversational agent for querying orofacial pain patients

Salome Wildermuth
Matrikel-Nr: 10-289-544
University of Zurich
Institute for Computational Linguistics

- Repository containing questions

"""
from dataclasses import dataclass
from src.conversation_turn.conversation_turn.conversation_element import QuestionType


@dataclass
class QuestionRepository:
    question_type: QuestionType
    questions: {} # key: preprocessed question, value: Question

@dataclass
class AnswerRepository:
    answers: {} # key: conversation turn, value: Answer

@dataclass
class TopicRepository:
    topics: {} # key: topic number, value: Topic, maybe not used?

@dataclass
class QuestionIntroRepository:
    # repo contains question intros per mental state
    mental_states: {}
