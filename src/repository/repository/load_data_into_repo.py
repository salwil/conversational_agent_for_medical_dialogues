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
from question_repo import

class Repository(Enum):
    QUESTIONS = 'question_repo'
    TOPICS = 'topic_repo'

class DataLoader:
    def __init__(self, repository: Repository):
        if repository is Repository.QUESTIONS:
            with open('../data/questions.txt') as questions_file:

        elif repository is Repository.TOPICS:
            pass
        else:
            sys.exit('Repository not known: ' + repository.value)


    with open(attributes_file, 'r') as txtfile:
        relevant_attributes = []
        attributes = txtfile.readlines()
        for attribute in attributes:
            if attribute.startswith('\t\t') or attribute.startswith('\t'):
                if attribute.startswith('\tMC:'):
                    pass
                else:
                    attribute = attribute.replace('\n', '')
                    attribute = attribute.replace('\t', '')
                    relevant_attributes.append(attribute)
