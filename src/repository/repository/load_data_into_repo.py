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
import warnings
from enum import Enum
import sys
import csv
from src.conversation_turn.conversation_turn.conversation_element import Question, Answer
from src.conversation_turn.conversation_turn.topic import Topic
from .repositories import QuestionType, QuestionRepository, MentalStates, AnswerRepository
import src.helpers.helpers.helpers as helpers

class Repository(Enum):
    QUESTIONS = 'question_repo'
    ANSWERS = 'answer_repo'
    TOPICS = 'topic_repo'
    MENTALSTATES = 'mental_state_repo'


class DataLoader:
    def __init__(self, preprocessing_parameters: list, preprocessor = None):
        self.profile_question_repo = QuestionRepository(QuestionType.PROFILE, {})
        self.mandatory_question_repo = QuestionRepository(QuestionType.MANDATORY, {})
        self.fallback_question_repo = QuestionRepository(QuestionType.FALLBACK, {})
        self.modedetail_question_repo = QuestionRepository(QuestionType.MOREDETAIL, {})
        self.topic_repo = {} # fuer spaeter ev: = TopicRepository({}), aber ev. overengineered
        self.mental_state_repo = None
        self.answer_repo = AnswerRepository({})
        self.path = helpers.get_project_path() + '/src/repository/data/';
        self.preprocessing_parameters = preprocessing_parameters
        self.preprocessor = preprocessor

    # load data from file into repository
    def load_data_into_repository(self, repository: Repository):
        if repository is Repository.QUESTIONS:
            if self.preprocessor:
                with open(self.path + 'questions.csv') as questions_file:
                    question_reader = csv.reader(questions_file, delimiter='\t', quotechar='"')
                    for question in question_reader:
                        question_type = self.determine_question_type(question[1])
                        q = Question(question[0], 0,  question_type)
                        self.preprocessor.preprocess(q, self.preprocessing_parameters)
                        self.select_repository(question_type=question_type).questions[q.content_preprocessed] = q
            else:
                raise Exception("Please provide a valid preprocessor instance for loading questions into repository.")

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
            warnings.warn('There is no data to load for this repository: ' + repository.value, ResourceWarning)

    # store data (e.g. from user input) in repository
    def store_data_in_repository(self, repository: Repository, data: str):
        if repository is Repository.ANSWERS:
            a = Answer(data, 1)
            self.preprocessor.preprocess(a, self.preprocessing_parameters)
            self.answer_repo.answers[a.content_preprocessed] = a


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
