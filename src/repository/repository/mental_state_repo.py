# -*- coding: utf-8 -*-

# mental_state_repo.py

"""
Bachelor-Thesis: Conversational agent for querying orofacial pain patients

Salome Wildermuth
Matrikel-Nr: 10-289-544
University of Zurich
Institute for Computational Linguistics

- Repository containing mental states

"""

from enum import Enum

class mentalStates(Enum):
    NEUTRAL = 'neutral' #default
    SAD = 'sad'
    HAPPY = 'happy'
    AFRAID = 'afraid'
    ANGRY = 'angry'
    SURPRISED = 'surprised'
    DISGUSTED = 'discusted'
    DISAPPOINTED = 'disappointed'
    DISPAIRED = 'dispaired'
    ILL = 'ill'
    CONFUSED = 'confused'