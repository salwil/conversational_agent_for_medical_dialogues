# -*- coding: utf-8 -*-

# patient.py

"""
Bachelor-Thesis: Conversational agent for querying orofacial pain patients

Salome Wildermuth
Matrikel-Nr: 10-289-544
University of Zurich
Institute for Computational Linguistics

- Data class for patient

"""

from dataclasses import dataclass, field
from enum import Enum
from datetime import date

class Gender(Enum):
    FEM = 'feminin',
    MASC = 'masculin'
    NA = 'none'

@dataclass
class Patient:
    first_name: str
    surname: str
    gender: Gender.NA
    date_of_birth: str
    height_in_cm: int
    weight_in_kg: int
    medical_care_provider: str
    date_of_conversation: date = date.today()

