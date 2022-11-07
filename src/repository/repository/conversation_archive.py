# -*- coding: utf-8 -*-

# conversation_archive.py

"""
Bachelor-Thesis: Conversational agent for querying orofacial pain patients

Salome Wildermuth
Matrikel-Nr: 10-289-544
University of Zurich
Institute for Computational Linguistics

- Writes each conversation turn to file

"""
from typing import TypedDict

import sys
import csv
import src.helpers.helpers.helpers as helpers

class ArchiveRecord(TypedDict):
    answer: str
    question: str

class ConversationArchival:
    def __init__(self, creation_date):
        self.archive_dir = helpers.get_project_path() + '/src/repository/data/conversation_archive/'
        self.patient_file = creation_date + '.csv'
        self.fieldnames = ['answer', 'question']
        self.is_ready = False
        self.archive_file = None
        self.archive_writer = None
        self.start_archive()

    def start_archive(self):
        helpers.create_directory_if_not_exists(self.archive_dir)
        self.archive_file = open(self.archive_dir + self.patient_file, 'w')
        self.archive_writer = csv.DictWriter(self.archive_file, delimiter='\t', quotechar='"', fieldnames=self.fieldnames)
        self.archive_writer.writeheader()
        self.is_ready = True

    def write_archive_record(self, archive_record: ArchiveRecord):
        if self.is_ready:
            self.archive_writer.writerow(archive_record)
        else:
            sys.exit("Start archive before writing to archive by using the start_archive() method.")
