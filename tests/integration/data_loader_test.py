import unittest
from src.repository.repository.load_data_into_repo import DataLoader, Repository
from src.conversation_turn.conversation_turn.conversation_element import Question

class ConversationElementTest(unittest.TestCase):

    def setUp(self) -> None:
        self.data_loader = DataLoader()

    def test_data_loader(self):
        # Note: this test only works as long as the Question 'How do you feel today?' is availabie
        # inside the questions.csv file!
        qr = self.data_loader.question_repo
        q = Question(content='How do you feel today?', number_of_usage=0, question_type='intro')
        self.data_loader.load_data_into_repository(Repository.QUESTIONS)
        self.assertEqual(len(qr),1)
        self.assertEqual(repr(qr['feel today']), repr(q))
