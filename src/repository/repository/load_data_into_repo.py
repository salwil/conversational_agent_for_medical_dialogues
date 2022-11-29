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

from src.conversation_turn.conversation_turn.conversation_element \
    import Question, PredefinedQuestion, Answer, QuestionIntro
from .repositories import QuestionType, QuestionRepository, AnswerRepository, QuestionIntroRepository
import src.helpers.helpers.helpers as helpers


class Repository(Enum):
    QUESTIONS = 'question_repo'
    ANSWERS = 'answer_repo'
    TOPICS = 'topic_repo'
    INTRO = 'question_intro_repo'
    MOREDETAIL = 'more_detail_repo'

class DataLoader:
    def __init__(self, preprocessing_parameters: list, preprocessor=None):
        self.profile_question_repo = QuestionRepository(QuestionType.PROFILE, {})
        self.mandatory_question_repo = QuestionRepository(QuestionType.MANDATORY, {})
        self.fallback_question_repo = QuestionRepository(QuestionType.FALLBACK, {})
        self.modedetail_question_repo = QuestionRepository(QuestionType.MOREDETAIL, {})
        self.generated_question_repo = QuestionRepository(QuestionType.GENERATED, {})
        self.question_intro_repo = QuestionIntroRepository({})
        self.answer_repo = AnswerRepository({})
        self.path_to_data = helpers.get_project_path() + '/src/repository/data/'
        self.path_to_topic_model = helpers.get_project_path() + '/src/model/language_models/mallet_topics/'
        self.preprocessing_parameters = preprocessing_parameters
        self.preprocessor = preprocessor

    # load data from file into repository
    def load_data_into_repository(self, repository: Repository):
        if repository is Repository.QUESTIONS:
            if self.preprocessor:
                with open(self.path_to_data + 'profile_questions.csv') as questions_file:
                    question_reader = csv.reader(questions_file, delimiter='\t', quotechar='"')
                    for question in question_reader:
                        question_type = self.determine_question_type(question[1])
                        if question_type is QuestionType.PROFILE:
                            q = PredefinedQuestion(question[0], 0, question_type, question[2])
                        else:
                            q = Question(question[0], 0, question_type)
                        self.preprocessor.preprocess(q, self.preprocessing_parameters)
                        self.select_repository(question_type=question_type).questions[q.content_preprocessed] = q
            else:
                raise Exception("Please provide a valid preprocessor instance for loading questions into repository.")

        elif repository is Repository.TOPICS:
            with open(self.path_to_data + 'questions_for_topics_10.csv') as topic_keys_file:
                question_reader = csv.reader(topic_keys_file, delimiter='\t', quotechar='"')
                for question in question_reader:
                    p = PredefinedQuestion(question[1], 0, QuestionType.MANDATORY, question[2])
                    self.preprocessor.preprocess(p, self.preprocessing_parameters)
                    topic_number = int(question[0])
                    if topic_number in self.mandatory_question_repo.questions:
                        self.mandatory_question_repo.questions[topic_number].append(p)
                    else:
                        self.mandatory_question_repo.questions[topic_number] = [p]

        elif repository is Repository.INTRO:
            with open(self.path_to_data + 'mental_states_with_intros.csv') as mental_states_file:
                mental_states_reader = csv.reader(mental_states_file, delimiter='\t', quotechar='"')
                for mental_state in mental_states_reader:
                    i = QuestionIntro(mental_state[1], 0, mental_state[2], mental_state[0])
                    if mental_state[0] in self.question_intro_repo.mental_states:
                        self.question_intro_repo.mental_states[mental_state[0]].append(i)
                    else:
                        self.question_intro_repo.mental_states[mental_state[0]] = [i]

        elif repository is Repository.MOREDETAIL:
            if self.preprocessor:
                with open(self.path_to_data + 'more_detail_questions.csv') as questions_file:
                    question_reader = csv.reader(questions_file, delimiter='\t', quotechar='"')
                    for question in question_reader:
                        question_type = QuestionType.MOREDETAIL
                        q = PredefinedQuestion(question[0], 0, question_type, question[1])
                        self.preprocessor.preprocess(q, self.preprocessing_parameters)
                        self.select_repository(question_type=question_type).questions[q.content_preprocessed] = q
            else:
                raise Exception("Please provide a valid preprocessor instance for loading questions into repository.")

        else:
            warnings.warn('There is no data to load for this repository: ' + repository.value, ResourceWarning)

    # store data (e.g. from user input) in repository
    def store_conversation_element(self, repository: str, conversation_element: Answer or Question):
        if repository == Repository.ANSWERS.value:
            #a = Answer(data, 1)
            #self.preprocessor.preprocess(a, self.preprocessing_parameters)
            self.answer_repo.answers[conversation_element.turn_number] = conversation_element
        elif repository == Repository.QUESTIONS.value:
            if conversation_element.content_preprocessed in self.generated_question_repo.questions:
                raise ValueError("Duplicate: Question was already used.")
            else:
                self.generated_question_repo.questions[conversation_element.content_preprocessed] = conversation_element
        else:
            warnings.warn('Repository: ' + repository + ' is not foreseen to store values other than from file.',
                          ResourceWarning)

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
            sys.exit("No repo found for this question type: " + question_type.value)
