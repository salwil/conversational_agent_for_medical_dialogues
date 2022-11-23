import pathlib
import unittest
from typing import List

import en_core_web_sm

from src.preprocess.preprocess.lemmatize import EnglishLemmatizer
from src.preprocess.preprocess.preprocess import Preprocessor
from src.repository.repository.load_data_into_repo import DataLoader, Repository
from src.conversation_turn.conversation_turn.conversation_element import Question, PredefinedQuestion, QuestionType, \
    Answer
from src.conversation_turn.conversation_turn.topic import Topic
import src.helpers.helpers.helpers as helpers


# load computation-intensive classes only once
preprocessing_parameters = ['lemmatize', 'tokenize', 'remove_punctuation', 'remove_stopwords']
nlp = en_core_web_sm.load()
lemmatizer = EnglishLemmatizer(nlp)
preprocessor = Preprocessor(lemmatizer, nlp)

path_to_files = helpers.get_project_path() + '/src/repository/data/'

class ConversationElementTest(unittest.TestCase):

    def setUp(self) -> None:

        self.data_loader = DataLoader(preprocessing_parameters=preprocessing_parameters,
                                 preprocessor=preprocessor)

    @unittest.skipIf(not pathlib.Path(path_to_files + 'questions.csv').exists(),
                     "Please add the file questions.csv to the repository/data/ folder.")
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

    @unittest.skipIf(not pathlib.Path(path_to_files + 'questions_for_topics_10.csv').exists(),
                     "Please add the file questions_for_topics_10.csv to the repository/data/ folder.")
    def test_data_loader_topic(self):
        mqr = self.data_loader.mandatory_question_repo
        self.data_loader.load_data_into_repository(Repository.TOPICS)
        self.assertEqual(10, len(mqr.questions))
        self.assertTrue(4 in mqr.questions)
        self.assertIsInstance(mqr.questions[4], list)
        self.assertIsInstance(mqr.questions[4][0], PredefinedQuestion)

    @unittest.skipIf(not pathlib.Path(path_to_files + 'mental_states_with_intros.csv').exists(),
                     "Please add the file mental_states_with_intros.csv to the repository/data/ folder.")
    def test_data_loader_mental_states(self):
        self.data_loader.load_data_into_repository(Repository.INTRO)
        ci = self.data_loader.question_intro_repo
        stored_intros = ci.mental_states
        self.assertGreater(len(ci.mental_states), 0)
        self.assertTrue('happy' in stored_intros)

    def test_data_loader_nothing_to_load(self):
        with self.assertWarns(ResourceWarning):
            self.data_loader.load_data_into_repository(Repository.ANSWERS)

    def test_data_loader_store_answers(self):
        answer = Answer("I have jaw pain.", 1, 1)
        answer.content_preprocessed = "jaw pain"
        ar = self.data_loader.answer_repo
        self.data_loader.store_conversation_element('answer_repo', answer)
        stored_answers = ar.answers
        self.assertEqual(1, len(stored_answers))
        self.assertTrue(1 in stored_answers)
        self.assertEqual(stored_answers[1].content, "I have jaw pain.")
        self.assertEqual(stored_answers[1].content_preprocessed, "jaw pain")
        self.assertEqual(stored_answers[1].number_of_usage, 1)

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