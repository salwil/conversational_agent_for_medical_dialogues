# -*- coding: utf-8 -*-

# load_data_into_repo.py

"""
Bachelor-Thesis: Conversational agent for querying orofacial pain patients

Salome Wildermuth
Matrikel-Nr: 10-289-544
University of Zurich
Institute for Computational Linguistics

- Class for loading data into repositories

"""
from enum import Enum
import sys
import csv
from src.conversation_turn.conversation_turn.conversation_element import Question
from src.conversation_turn.conversation_turn.topic import Topic
from src.preprocess.preprocess.preprocess import Preprocessor
from src.preprocess.preprocess.lemmatize import EnglishLemmatizer
import src.helpers.helpers.helpers as helpers

class Repository(Enum):
    QUESTIONS = 'question_repo'
    TOPICS = 'topic_repo'


class DataLoader:
    def __init__(self):
        self.question_repo = {}
        self.topic_repo = {}
        self.preprocessor = Preprocessor(lemmatizer=EnglishLemmatizer())
        self.path = helpers.get_project_path() + '/src/repository/data/';

    def load_data_into_repository(self, repository: Repository):
        if repository is Repository.QUESTIONS:
            with open(self.path + 'questions.csv') as questions_file:
                question_reader = csv.reader(questions_file, delimiter='\t', quotechar='"')
                for question in question_reader:
                    q = Question(question[0], 0,  question[1])
                    self.preprocessor.preprocess(q, ['lemmatize',
                                                     'tokenize',
                                                     'remove_punctuation',
                                                     'remove_stopwords'])
                    self.question_repo[q.content_preprocessed] = q

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
        else:
            sys.exit('Repository not known: ' + repository.value)
