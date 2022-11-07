# -*- coding: utf-8 -*-

# cli.py

"""
Bachelor-Thesis: Conversational agent for querying orofacial pain patients

Salome Wildermuth
Matrikel-Nr: 10-289-544
University of Zurich
Institute for Computational Linguistics

- Command Line Interface for interaction with conversational agent system

"""

import sys
import argparse

class CLI ():
    def __init__(self):
        parser = argparse.ArgumentParser('conversation', description='Interact with conversational agent')
        parser.add_argument('--start', required=False, action="store_true",
                            help='Start a conversation')

        args= parser.parse_args()
        self.arguments = (vars(args))

    def talk(self):
        if (self.arguments['start']):
            print("Welcome!!! Please wait a moment until someone has time for you. ")
        else:
            print("Byebye!")