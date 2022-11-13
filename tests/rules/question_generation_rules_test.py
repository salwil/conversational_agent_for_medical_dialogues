import unittest
from unittest.mock import MagicMock

import en_core_web_sm

from conversation_turn.conversation_turn.conversation_element import Answer
from preprocess.preprocess.lemmatize import EnglishLemmatizer
from preprocess.preprocess.preprocess import Preprocessor
from rules.rules.question_generation_rules import QuestionGenerationRules

# load computation-intensive classes only once
nlp = en_core_web_sm.load()

class QuestionGenerationRulesTest(unittest.TestCase):

    def setUp(self) -> None:
        # the preprocessor is needed for pronoun replacement only, but this is tested in question_generation_rules and
        # therefore we mock the preprocessor (and also the pronoun replacement method in the below tests)
        self.preprocessor = MagicMock()
        self.question_generation_rules = QuestionGenerationRules(self.preprocessor, nlp)

    def test_generate_highlight_not_who_not_what(self):
        highlight = self.question_generation_rules.generate_highlight("Dr. Mayer told me to take Aspirin")
        self.assertFalse('who' in self.question_generation_rules.allowed_pronouns)
        self.assertFalse('what' in self.question_generation_rules.allowed_pronouns)
        self.assertNotEqual(highlight[0], 'My doctor')
        self.assertNotEqual(highlight[0], 'My jaw')

    def test_generate_highlight_not_when(self):
        highlight = self.question_generation_rules.generate_highlight("It often hurts in the morning")
        self.assertFalse('when' in self.question_generation_rules.allowed_pronouns)
        self.assertNotEqual(highlight[0], 'during')

    def test_generate_highlight_all_pronouns_allowed(self):
        self.question_generation_rules.generate_highlight("When I am at home I feel better.")
        self.assertEqual(['why', 'when', 'where', 'what', 'who', 'how', 'how often', 'how many', 'since'],
                         self.question_generation_rules.allowed_pronouns)

    def test_replace_pronouns(self):
        preprocessor = Preprocessor(EnglishLemmatizer(nlp), nlp)
        question_generation_rules = QuestionGenerationRules(preprocessor, nlp)
        answer = Answer("When I am at home I feel better.", 0)
        question_generation_rules.replace_pronouns(answer)

