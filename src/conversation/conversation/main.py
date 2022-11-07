# -*- coding: utf-8 -*-

# main.py

"""
Bachelor-Thesis: Conversational agent for querying orofacial pain patients

Salome Wildermuth
Matrikel-Nr: 10-289-544
University of Zurich
Institute for Computational Linguistics

- main module for maintaining conversation with user

"""

from .cli import CLI
from src.repository.repository.load_data_into_repo import DataLoader, Repository

cli = CLI()
data_loader = DataLoader()

def main():
    cli.talk()
    load_repositories()



def load_repositories():
    data_loader.load_data_into_repository(Repository.QUESTIONS)
    data_loader.load_data_into_repository(Repository.TOPICS)
    data_loader.load_data_into_repository(Repository.MENTALSTATES)

