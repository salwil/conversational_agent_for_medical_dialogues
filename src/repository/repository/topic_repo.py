# -*- coding: utf-8 -*-

# topic_repo.py

"""
Bachelor-Thesis: Conversational agent for querying orofacial pain patients

Salome Wildermuth
Matrikel-Nr: 10-289-544
University of Zurich
Institute for Computational Linguistics

- Repository containing topics

"""
from dataclasses import dataclass, field

@dataclass
class TopicRepository:
    topics: dict # key: topic number, value: Topic