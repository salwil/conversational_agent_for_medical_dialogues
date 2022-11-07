import unittest
import datetime
from src.conversation.conversation.patient import Patient

class ConversationElementTest(unittest.TestCase):

    def setUp(self) -> None:
        self.patient = Patient()
        self.patient.first_name = 'firstname'
        self.patient.surname = 'surname'
        self.patient.gender = 'feminin'
        self.patient.date_of_birth = '12-12-1990'

    def test_date_of_conversation_is_set_at_instantiation(self):
        self.assertEqual(datetime.datetime.now().year, self.patient.creation_timestamp.year)
        self.assertEqual(datetime.datetime.now().month, self.patient.creation_timestamp.month)
        self.assertEqual(datetime.datetime.now().day, self.patient.creation_timestamp.day)
        self.assertEqual(datetime.datetime.now().hour, self.patient.creation_timestamp.hour)
