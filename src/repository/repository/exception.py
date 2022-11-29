# -*- coding: utf-8 -*-

# exception.py

"""
Bachelor-Thesis: Conversational agent for querying orofacial pain patients

Salome Wildermuth
Matrikel-Nr: 10-289-544
University of Zurich
Institute for Computational Linguistics

- Class repository custom exceptions

"""

class DuplicateError(Exception):
    def __init__(self, message):
        super().__init__(message)

