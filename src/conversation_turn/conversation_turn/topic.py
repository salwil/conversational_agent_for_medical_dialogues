# -*- coding: utf-8 -*-

# topic.py

"""
Bachelor-Thesis: Conversational agent for querying orofacial pain patients

Salome Wildermuth
Matrikel-Nr: 10-289-544
University of Zurich
Institute for Computational Linguistics

- Data class for topic

"""
from dataclasses import dataclass

@dataclass
class Topic:
    keywords: list
    relevance: float