# -*- coding: utf-8 -*-

# load_data_into_repo.py

"""
Bachelor-Thesis: Conversational agent for querying orofacial pain patients

Salome Wildermuth
Matrikel-Nr: 10-289-544
University of Zurich
Institute for Computational Linguistics

- Class for loading data into memory
- Containers for questions, topics and mental states are called repositories.
- question_repo provides collection of questions (datatype Question)
- topic_repo provides collection of topics (datatype Topic)
- mental_state_repo provides collection of mental states (datatype mentalState)

"""
from enum import Enum
import sys
import csv
from src.conversation_turn.conversation_turn.conversation_element import Question
from src.conversation_turn.conversation_turn.topic import Topic
from .question_repo import QuestionType, QuestionRepository
from .mental_state_repo import MentalStates
from src.preprocess.preprocess.preprocess import Preprocessor
from src.preprocess.preprocess.lemmatize import EnglishLemmatizer
import src.helpers.helpers.helpers as helpers

class Repository(Enum):
    QUESTIONS = 'question_repo'
    TOPICS = 'topic_repo'
    MENTALSTATES = 'mental_state_repo'


class DataLoader:
    def __init__(self):
        self.profile_question_repo = QuestionRepository(QuestionType.PROFILE, {})
        self.mandatory_question_repo = QuestionRepository(QuestionType.MANDATORY, {})
        self.fallback_question_repo = QuestionRepository(QuestionType.FALLBACK, {})
        self.modedetail_question_repo = QuestionRepository(QuestionType.MOREDETAIL, {})
        self.topic_repo = {} # fuer spaeter ev: = TopicRepository({}), aber ev. overengineered
        self.mental_state_repo = None
        self.path = helpers.get_project_path() + '/src/repository/data/';

    def load_data_into_repository(self, repository: Repository):
        if repository is Repository.QUESTIONS:
            preprocessor = Preprocessor(lemmatizer=EnglishLemmatizer())
            with open(self.path + 'questions.csv') as questions_file:
                question_reader = csv.reader(questions_file, delimiter='\t', quotechar='"')
                for question in question_reader:
                    question_type = self.determine_question_type(question[1])
                    q = Question(question[0], 0,  question_type)
                    preprocessor.preprocess(q, ['lemmatize',
                                                'tokenize',
                                                'remove_punctuation',
                                                'remove_stopwords'])
                    self.select_repository(question_type=question_type).questions[q.content_preprocessed] = q

        elif repository is Repository.TOPICS:
            with open(self.path + 'topics.txt') as questions_file:
                topics = questions_file.readlines()
                topic_number = 1
                for keywords in topics:
                    keyword_list = keywords.split(', ')
                    keyword_list_clean = [k.rstrip("\n") for k in keyword_list]
                    t = Topic(topic_number, keyword_list_clean, 0.0)
                    self.topic_repo[topic_number] = t
                    topic_number += 1
        elif repository is Repository.MENTALSTATES:
            self.mental_state_repo = MentalStates
            print(self.mental_state_repo)
        else:
            sys.exit('Repository not known: ' + repository.value)

    def determine_question_type(self, question_type: str):
        if question_type == QuestionType.PROFILE.value:
            return QuestionType.PROFILE
        elif question_type == QuestionType.MANDATORY.value:
            return QuestionType.MANDATORY
        elif question_type == QuestionType.FALLBACK.value:
            return QuestionType.FALLBACK
        elif question_type == QuestionType.MOREDETAIL.value:
            return QuestionType.MOREDETAIL
        else:
            sys.exit("No repo found for this question type: " + question_type)

    def select_repository(self, question_type: QuestionType):
        if question_type is QuestionType.PROFILE:
            return self.profile_question_repo
        elif question_type is QuestionType.MANDATORY:
            return self.mandatory_question_repo
        elif question_type is QuestionType.FALLBACK:
            return self.mandatory_question_repo
        elif question_type is QuestionType.MOREDETAIL:
            return self.modedetail_question_repo
        else:
            sys.exit("No repo found for this question type: " + question_type)
