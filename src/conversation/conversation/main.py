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

cli = CLI()

def main():
    cli.talk()




