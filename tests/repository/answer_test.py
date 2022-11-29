import unittest
from conversation_turn.conversation_element import Answer

class ConversationElementTest(unittest.TestCase):

    def setUp(self) -> None:
        self.answer = "Ich habe Kopfschmerzen"

    def test_answer_instantiation(self):
        answer = Answer(self.answer, 1, 1)
        answer.content_preprocessed = "Kopfschmerz"
        self.assertEqual(answer.content, "Ich habe Kopfschmerzen")
        self.assertEqual(answer.content_preprocessed, "Kopfschmerz")
        self.assertEqual(answer.number_of_usage, 1)
        self.assertEqual(answer.turn_number, 1)
