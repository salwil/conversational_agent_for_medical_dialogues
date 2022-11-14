import unittest
from unittest.mock import MagicMock

import en_core_web_sm

from conversation_turn.conversation_turn.conversation_element import Answer
from preprocess.preprocess.lemmatize import EnglishLemmatizer
from preprocess.preprocess.preprocess import Preprocessor
from rules.rules.question_generation_rules import QuestionGenerationRules

# load computation-intensive classes only once
nlp = en_core_web_sm.load()
preprocessor = Preprocessor(EnglishLemmatizer(nlp), nlp)

class QuestionGenerationRulesTest(unittest.TestCase):

    def setUp(self) -> None:
        # the preprocessor is needed for pronoun replacement only, but this is tested in question_generation_rules and
        # therefore we mock the preprocessor (and also the pronoun replacement method in the below tests)
        self.preprocessor = MagicMock()

    def test_generate_highlight_not_who_not_what(self):
        answer = Answer("Dr. Mayer told me to take Aspirin", 1)
        answer.content_in_2nd_pers = "Dr. Mayer told you to take Aspirin"
        self.question_generation_rules = QuestionGenerationRules(answer, self.preprocessor, nlp)
        self.question_generation_rules.generate_highlight()
        self.assertFalse('who' in self.question_generation_rules.allowed_pronouns)
        self.assertFalse('what' in self.question_generation_rules.allowed_pronouns)
        self.assertNotEqual(answer.content_with_hl, 'My doctor')
        self.assertNotEqual(answer.content_with_hl, 'My jaw')

    def test_generate_highlight_not_when(self):
        answer = Answer("It often hurts in the morning", 1)
        answer.content_in_2nd_pers = "It often hurts in the morning"
        self.question_generation_rules = QuestionGenerationRules(answer, self.preprocessor, nlp)
        highlight = self.question_generation_rules.generate_highlight()
        self.assertFalse('when' in self.question_generation_rules.allowed_pronouns)
        self.assertNotEqual(answer.content_with_hl, 'during')

    def test_generate_highlight_all_pronouns_allowed(self):
        answer = Answer("When I am at home I feel better.", 1)
        answer.content_in_2nd_pers = "When I am at home I feel better."
        self.question_generation_rules = QuestionGenerationRules(answer, self.preprocessor, nlp)
        self.question_generation_rules.generate_highlight()
        self.assertEqual(['why', 'when', 'where', 'what', 'who', 'how', 'how often', 'how many', 'since'],
                         self.question_generation_rules.allowed_pronouns)

    def test_create_2nd_person_sentence_pers_pronoun_and_verb_b(self):
        answer = Answer("When I am at home I feel better.", 1)
        question_generation_rules = QuestionGenerationRules(answer, preprocessor, nlp)
        question_generation_rules.create_2nd_person_sentence_from_1st_person()
        self.assertEqual('When you are at home you feel better .', answer.content_in_2nd_pers)
        # assert that original content is still there
        self.assertEqual("When I am at home I feel better.", answer.content)

    def test_create_2nd_person_sentence_short_forms(self):
        answer = Answer("When I'm at home, my health gets better.", 1)
        question_generation_rules = QuestionGenerationRules(answer, preprocessor, nlp)
        question_generation_rules.create_2nd_person_sentence_from_1st_person()
        self.assertEqual("When you 're at home , your health gets better .", answer.content_in_2nd_pers)
        self.assertEqual("When I'm at home, my health gets better.", answer.content)

    def test_create_2nd_person_sentence_false_friend_have(self):
        answer = Answer("I often have headache.", 1)
        question_generation_rules = QuestionGenerationRules(answer, preprocessor, nlp)
        question_generation_rules.create_2nd_person_sentence_from_1st_person()
        self.assertEqual("you often have headache .", answer.content_in_2nd_pers)
        self.assertEqual("I often have headache.", answer.content)

    def test_create_2nd_person_sentence_multiple_sentences(self):
        answer = Answer("I often have headache. Sometimes I also have jaw tension. Especially during the night.", 1)
        question_generation_rules = QuestionGenerationRules(answer, preprocessor, nlp)
        question_generation_rules.create_2nd_person_sentence_from_1st_person()
        self.assertEqual("you often have headache . Sometimes you also have jaw tension . Especially during the night ."
                         , answer.content_in_2nd_pers)
        self.assertEqual("I often have headache. Sometimes I also have jaw tension. Especially during the night."
                         , answer.content)


