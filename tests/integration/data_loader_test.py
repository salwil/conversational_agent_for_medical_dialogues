import unittest

import en_core_web_sm

from src.preprocess.preprocess.lemmatize import EnglishLemmatizer
from src.preprocess.preprocess.preprocess import Preprocessor
from src.repository.repository.load_data_into_repo import DataLoader, Repository, MentalStates
from src.conversation_turn.conversation_turn.conversation_element import Question, PredefinedQuestion, QuestionType, \
    Answer
from src.conversation_turn.conversation_turn.topic import Topic

# load computation-intensive classes only once
preprocessing_parameters = ['lemmatize', 'tokenize', 'remove_punctuation', 'remove_stopwords']
nlp = en_core_web_sm.load()
lemmatizer = EnglishLemmatizer(nlp)
preprocessor = Preprocessor(lemmatizer, nlp)


class ConversationElementTest(unittest.TestCase):

    def setUp(self) -> None:
        self.data_loader = DataLoader(preprocessing_parameters=preprocessing_parameters,
                                 preprocessor=preprocessor)

    def test_data_loader_profile_question(self):
        # Note: this test only works as long as the Question 'How do you feel today?' is available
        # inside the questions.csv file!
        qr = self.data_loader.profile_question_repo
        q_exp = PredefinedQuestion(content='What is your first name?',
                                   number_of_usage=0,
                                   question_type=QuestionType.PROFILE,
                                   content_in_german="Was ist Ihr Vorname?")
        self.data_loader.load_data_into_repository(Repository.QUESTIONS)
        self.assertEqual(7, len(qr.questions))
        self.assertEqual(q_exp.content_in_german, qr.questions['first name'].content_in_german)
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

    def test_data_loader_nothing_to_load(self):
        with self.assertWarns(ResourceWarning):
            self.data_loader.load_data_into_repository(Repository.ANSWERS)

    def test_data_loader_store_answers(self):
        answer = Answer("I have jaw pain.", 1)
        answer.content_preprocessed = "jaw pain"
        ar = self.data_loader.answer_repo
        self.data_loader.store_conversation_element('answer_repo', answer)
        stored_answers = ar.answers
        self.assertEqual(1, len(stored_answers))
        self.assertTrue('jaw pain' in stored_answers)
        self.assertEqual(stored_answers['jaw pain'].content, "I have jaw pain.")
        self.assertEqual(stored_answers['jaw pain'].number_of_usage, 1)

    def test_data_loader_store_generated_question(self):
        question = Question("When do you have headache?", 1, QuestionType.GENERATED)
        question.content_preprocessed = "headache"
        qr = self.data_loader.generated_question_repo
        self.data_loader.store_conversation_element('question_repo', question)
        stored_questions = qr.questions
        print(stored_questions)
        self.assertEqual(1, len(stored_questions))
        self.assertTrue('headache' in stored_questions)
        self.assertEqual(stored_questions['headache'].content, "When do you have headache?")
        self.assertEqual(stored_questions['headache'].number_of_usage, 1)
