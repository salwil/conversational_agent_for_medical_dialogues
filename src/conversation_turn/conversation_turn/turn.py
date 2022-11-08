# -*- coding: utf-8 -*-

# question.py

"""
Bachelor-Thesis: Conversational agent for querying orofacial pain patients

Salome Wildermuth
Matrikel-Nr: 10-289-544
University of Zurich
Institute for Computational Linguistics

- Data class for conversation turn

"""

class Turn:
    def __init__(self, turn_number, conversation_archive):
        self.turn_number = turn_number;

        # References to other objects
        self.mental_state = None
        self.input = None
        self.question = None
        self.conversation_archive = conversation_archive

    def write_turn_to_archive(self):
        archive_record = {'answer': self.input, 'question': self.question}
        self.conversation_archive.write(self, archive_record)
