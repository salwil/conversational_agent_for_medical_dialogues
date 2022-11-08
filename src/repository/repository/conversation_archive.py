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
from enum import Enum
import sys
import csv
import src.helpers.helpers.helpers as helpers

class ArchiveRecord(TypedDict):
    answer: str
    question: str

class ArchiveOperation(Enum):
    READ = 'r',
    WRITE = 'w'

class ConversationArchival:
    def __init__(self, creation_date):
        self.archive_dir = helpers.get_project_path() + '/src/repository/data/conversation_archive/'
        self.archive_file_name = creation_date + '.csv'
        self.fieldnames = ['answer', 'question']
        self.is_ready = False
        self.archive_file = None
        self.archive_writer = None
        self.start(ArchiveOperation.WRITE)

    def start(self, operation: ArchiveOperation):
        if self.is_ready:
            print("Archive is already running.")
        else:
            helpers.create_directory_if_not_exists(self.archive_dir)
            if operation is ArchiveOperation.WRITE:
                self.archive_file = open(self.archive_dir + self.archive_file_name, 'w')
                self.archive_writer = csv.DictWriter(self.archive_file,
                                                     delimiter='\t',
                                                     quotechar='"',
                                                     fieldnames=self.fieldnames)
                self.archive_writer.writeheader()
            elif operation is ArchiveOperation.READ:
                self.archive_file = open(self.archive_dir + self.archive_file_name, 'r')
            else:
                sys.exit("Unknown archive operation. Allowed are: READ, WRITE")
            self.is_ready = True

    def write(self, archive_record: ArchiveRecord):
        if self.is_ready:
            self.archive_writer.writerow(archive_record)
        else:
            sys.exit("Start archive before writing to archive by using the start_archive() method.")

    def terminate(self):
        if self.is_ready:
            self.archive_file.close()
            self.is_ready = False
        else:
            print("No need for terminating, the archive is not running.")
