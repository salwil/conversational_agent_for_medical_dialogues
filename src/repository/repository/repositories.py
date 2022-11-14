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
from enum import Enum
from src.conversation_turn.conversation_turn.conversation_element import QuestionType


@dataclass
class QuestionRepository:
    question_type: QuestionType
    questions: {} # key: preprocessed question, value: Question

@dataclass
class AnswerRepository:
    answers: {} # key: preprocessed answer, value: Answer

@dataclass
class TopicRepository:
    topics: dict # key: topic number, value: Topic

@dataclass
class QuestionIntroRepository:
    # repo contains question intros per mental state
    mental_states: {}