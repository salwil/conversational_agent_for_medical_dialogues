import unittest
from src.repository.repository.load_data_into_repo import DataLoader, Repository, MentalStates
from src.conversation_turn.conversation_turn.conversation_element import Question, QuestionType
from src.conversation_turn.conversation_turn.topic import Topic


class ConversationElementTest(unittest.TestCase):

    def setUp(self) -> None:
        self.data_loader = DataLoader()

    def test_data_loader_profile_question(self):
        # Note: this test only works as long as the Question 'How do you feel today?' is available
        # inside the questions.csv file!
        qr = self.data_loader.profile_question_repo
        q_exp = Question(content='What is your first name?', number_of_usage=0, question_type=QuestionType.PROFILE)
        self.data_loader.load_data_into_repository(Repository.QUESTIONS)
        self.assertEqual(7, len(qr.questions))
        self.assertEqual(repr(q_exp), repr(qr.questions['first name']))

    def test_data_loader_mandatory_question(self):
        # Note: this test only works as long as the Question 'How do you feel today?' is available
        # inside the questions.csv file!
        qr = self.data_loader.mandatory_question_repo
        q_exp = Question(content='Please describe your chief complaint for which you seek consultation.',
                         number_of_usage=0,
                         question_type=QuestionType.MANDATORY)
        self.data_loader.load_data_into_repository(Repository.QUESTIONS)
        self.assertEqual(5, len(qr.questions))
        self.assertEqual(repr(q_exp), repr(qr.questions['please describe chief complaint seek consultation']))

    def test_data_loader_topic(self):
        # Note: this test only works as long as the Question topic 1 is available in this form
        # inside the topics.txt file!
        tr = self.data_loader.topic_repo
        t_exp = Topic(1, ['jaw', 'mouth', 'open', 'eat', 'chew', 'food'], 0.0)
        self.data_loader.load_data_into_repository(Repository.TOPICS)
        self.assertEqual(2, len(tr))
        self.assertEqual(repr(t_exp), repr(tr[1]))

    def test_data_loader_mental_states(self):
        # Note: ms has to be assigned after the loader, else it's None! (don't know why...)
        self.data_loader.load_data_into_repository(Repository.MENTALSTATES)
        ms = self.data_loader.mental_state_repo
        for mental_state in MentalStates:
            self.assertTrue(mental_state in ms)
