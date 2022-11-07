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
import datetime

class Gender(Enum):
    FEM = 'feminin',
    MASC = 'masculin'
    NA = 'none'

@dataclass
class Patient:
    first_name: str = field(init = False)
    surname: str = field(init = False)
    gender: Gender.NA = field(init = False)
    date_of_birth: str = field(init = False)
    height_in_cm: int = field(init = False)
    weight_in_kg: int = field(init = False)
    medical_care_provider: str = field(init = False)
    creation_timestamp: datetime = datetime.datetime.now()
    creation_timestamp_formatted: str = creation_timestamp.strftime("%m-%d-%Y-%H-%M-%S")


