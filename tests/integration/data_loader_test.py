import unittest
from src.repository.repository.load_data_into_repo import DataLoader, Repository, mentalStates
from src.conversation_turn.conversation_turn.conversation_element import Question
from src.conversation_turn.conversation_turn.topic import Topic

class ConversationElementTest(unittest.TestCase):

    def setUp(self) -> None:
        self.data_loader = DataLoader()

    def test_data_loader_question(self):
        # Note: this test only works as long as the Question 'How do you feel today?' is availabie
        # inside the questions.csv file!
        qr = self.data_loader.question_repo
        q_exp = Question(content='How do you feel today?', number_of_usage=0, question_type='intro')
        self.data_loader.load_data_into_repository(Repository.QUESTIONS)
        self.assertEqual(1, len(qr))
        self.assertEqual(repr(q_exp), repr(qr['feel today']))

    def test_data_loader_topic(self):
        # Note: this test only works as long as the Question topic 1 is availabie in this form
        # inside the topics.txt file!
        tr = self.data_loader.topic_repo
        t_exp = Topic(1, ['jaw', 'mouth', 'open', 'eat', 'chew', 'food'], 0.0)
        self.data_loader.load_data_into_repository(Repository.TOPICS)
        self.assertEqual(2, len(tr))
        self.assertEqual(repr(t_exp), repr(tr[1]))

    def test_data_loader_mental_states(self):
        # Note: ms has to be assigned after the loader, else it's None!
        self.data_loader.load_data_into_repository(Repository.MENTALSTATES)
        ms = self.data_loader.mental_state_repo
        for mental_state in mentalStates:
            self.assertTrue(mental_state in ms)

