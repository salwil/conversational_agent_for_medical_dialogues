import unittest
from datetime import date
from src.conversation.conversation.patient import Patient

class ConversationElementTest(unittest.TestCase):

    def setUp(self) -> None:
        self.patient = Patient("name", "surname", 25, 'feminin', '12-12-1990')
        self.answer_preprocessed = "Kopfschmerz"

    def test_date_of_conversation_is_set_at_instantiation(self):
        self.assertEqual(date.today(), self.patient.date_of_conversation)