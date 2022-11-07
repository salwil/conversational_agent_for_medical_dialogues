import unittest
from src.repository.repository.conversation_archive import ConversationArchival

class ConversationArchiveTest(unittest.TestCase):

    def setUp(self) -> None:
        self.archive = ConversationArchival('creation_date')

    def test_archive_is_ready_after_instantiation(self):
        self.assertTrue(self.archive.is_ready)
        self.assertIsNotNone(self.archive.archive_writer)
        self.assertIsNotNone(self.archive.archive_file)

