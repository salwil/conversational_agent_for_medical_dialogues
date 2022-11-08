import unittest
import csv
from src.repository.repository.conversation_archive import ConversationArchival, ArchiveOperation

class ConversationArchiveTest(unittest.TestCase):

    def setUp(self) -> None:
        self.archive = ConversationArchival('tests_creation_date')

    def test_archive_is_ready_after_instantiation(self):
        self.assertTrue(self.archive.is_ready)
        self.assertIsNotNone(self.archive.archive_writer)
        self.assertIsNotNone(self.archive.archive_file)

    def test_write_conversation_record_to_archive_file(self):
        archive_record = {'answer': 'I have headache', 'question': 'When do you have headache?'}
        self.archive.write(archive_record)
        self.archive.terminate()
        self.archive.start(ArchiveOperation.READ)
        reader = csv.reader(self.archive.archive_file, delimiter='\t', quotechar='"')
        header = next(reader)
        first_row = next(reader) #
        self.assertEqual(['answer', 'question'], header)
        self.assertEqual(['I have headache', 'When do you have headache?'], first_row)

    def test_terminate_archive(self):
        self.archive.terminate()
        self.assertFalse(self.archive.is_ready)