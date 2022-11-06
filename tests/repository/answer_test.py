import unittest
from src.conversation_turn.conversation_turn.conversation_element import Answer

class ConversationElementTest(unittest.TestCase):

    def setUp(self) -> None:
        self.answer = "Ich habe Kopfschmerzen"
        self.answer_preprocessed = "Kopfschmerz"

    def test_answer(self):
        answer = Answer(self.answer, self.answer_preprocessed, 1, "blabla")
        self.assertEqual(answer.content, "Ich habe Kopfschmerzen")
        self.assertEqual(answer.number_of_usage, 1)
