import unittest
from unittest.mock import patch, MagicMock

import en_core_web_sm

from conversation_turn.conversation_turn.conversation_element import Answer
from rules.rules.interrogative_pronouns import Position
from rules.rules.question_generation_rules import QuestionGenerationRules
from src.model.model.question_generation import QuestionGenerator

# load computation-intensive classes only once
nlp = en_core_web_sm.load()

class QuestionGenerationTest(unittest.TestCase):
    """
    This test class demonstrates how the defined triggers perfectly work for generating a question starting with the
    desired interrogative pronoun.
    Note that the we mock the interrogative pronoun, because in the real method it's chosen on a random base what would
    make it impossible to make meaningful assertions.
    Consequently THIS TEST DOES NOT TEST THE SELECTION OF THE INTERROGATIVE PRONOUN, but the method is tested in
    question_generation_rules_test.py
    """

    def setUp(self) -> None:
        # the preprocessor is needed for pronoun replacement only, but this is tested in question_generation_rules and
        # therefore we mock the preprocessor (and also the pronoun replacement method in the below tests)
        self.preprocessor = MagicMock()

    def test_generate_why_question(self):
        answer = Answer("In the night I can't sleep ", 1)
        answer.content_in_2nd_pers = "In the night you can't sleep"
        question_generator = QuestionGenerator(self.preprocessor, nlp, answer)
        hl = "[HL] because [HL]."
        with patch.object(QuestionGenerationRules,
                          '_QuestionGenerationRules__select_interrogative_pronoun_for_next_question',
                          return_value="why")\
                as __select_interrogative_pronoun_for_next_question:
            # we set the content in 2nd person manually (above) and patch the below method as we only have a mocked
            # preprocessor (the tokenization method call would not work)
            with patch.object(QuestionGenerationRules, 'create_2nd_person_sentence_from_1st_person'):
                self.assertTrue(question_generator.generate_with_highlight().startswith("Why"))
                self.assertTrue(hl in answer.content_with_hl)

    def test_generate_when_question(self):
        answer = Answer("I often have ear pain, ", 1)
        answer.content_in_2nd_pers = "You often have ear pain"
        question_generator = QuestionGenerator(self.preprocessor, nlp, answer)
        hl = "[HL] during [HL]."
        with patch.object(QuestionGenerationRules,
                          '_QuestionGenerationRules__select_interrogative_pronoun_for_next_question',
                          return_value="when")\
                as __select_interrogative_pronoun_for_next_question:
            # we set the content in 2nd person manually (above) and patch the below method as we only have a mocked
            # preprocessor (the tokenization method call would not work)
            with patch.object(QuestionGenerationRules, 'create_2nd_person_sentence_from_1st_person'):
                self.assertTrue(question_generator.generate_with_highlight().startswith("When"))
                self.assertTrue(hl in answer.content_with_hl)

    def test_generate_where_question(self):
        answer = Answer("I often have pain, ", 1)
        answer.content_in_2nd_pers = "You often have pain, "
        question_generator = QuestionGenerator(self.preprocessor, nlp, answer)
        hl = "[HL] at the University Hospital [HL]."
        with patch.object(QuestionGenerationRules,
                          '_QuestionGenerationRules__select_interrogative_pronoun_for_next_question',
                          return_value="where")\
                as __select_interrogative_pronoun_for_next_question:
            # we set the content in 2nd person manually (above) and patch the below method as we only have a mocked
            # preprocessor (the tokenization method call would not work)
            with patch.object(QuestionGenerationRules, 'create_2nd_person_sentence_from_1st_person'):
                self.assertTrue(question_generator.generate_with_highlight().startswith("Where"))
                self.assertTrue(hl in answer.content_with_hl)

    def test_generate_how_question(self):
        answer = Answer("I often have pain, ", 1)
        answer.content_in_2nd_pers = "You often have pain"
        question_generator = QuestionGenerator(self.preprocessor, nlp, answer)
        hl = "[HL] in form of [HL]."
        with patch.object(QuestionGenerationRules,
                          '_QuestionGenerationRules__select_interrogative_pronoun_for_next_question',
                          return_value="how")\
                as __select_interrogative_pronoun_for_next_question:
            # we set the content in 2nd person manually (above) and patch the below method as we only have a mocked
            # preprocessor (the tokenization method call would not work)
            with patch.object(QuestionGenerationRules, 'create_2nd_person_sentence_from_1st_person'):
                self.assertTrue(question_generator.generate_with_highlight().startswith("How"))
                self.assertTrue(hl in answer.content_with_hl)

    def test_generate_who_question(self):
        answer = Answer(" says that I have to stay in bed.", 1)
        answer.content_in_2nd_pers = "says that you have to stay in bed."
        question_generator = QuestionGenerator(self.preprocessor, nlp, answer)
        hl = "[HL] Your Doctor [HL]"
        with patch.object(QuestionGenerationRules,
                          '_QuestionGenerationRules__select_interrogative_pronoun_for_next_question',
                          return_value="who")\
                as __select_interrogative_pronoun_for_next_question:
            # we set the content in 2nd person manually (above) and patch the below method as we only have a mocked
            # preprocessor (the tokenization method call would not work)
            with patch.object(QuestionGenerationRules, 'create_2nd_person_sentence_from_1st_person'):
                self.assertTrue(question_generator.generate_with_highlight().startswith("Who"))
                self.assertTrue(hl in answer.content_with_hl)

    def test_generate_what_question(self):
        answer = Answer(" hurts when I eat food.", 1)
        answer.content_in_2nd_pers = " hurts when you eat food"
        question_generator = QuestionGenerator(self.preprocessor, nlp, answer)
        hl = "[HL] Your jaw [HL]"
        with patch.object(QuestionGenerationRules,
                          '_QuestionGenerationRules__select_interrogative_pronoun_for_next_question',
                          return_value="what")\
                as __select_interrogative_pronoun_for_next_question:
            # we set the content in 2nd person manually (above) and patch the below method as we only have a mocked
            # preprocessor (the tokenization method call would not work)
            with patch.object(QuestionGenerationRules, 'create_2nd_person_sentence_from_1st_person'):
                self.assertTrue(question_generator.generate_with_highlight().startswith("What"))
                self.assertTrue(hl in answer.content_with_hl)

    def test_generate_how_long_question(self):
        answer = Answer(" my jaw hurts when I eat food.", 1)
        answer.content_in_2nd_pers = " your jaw hurts when you eat food"
        question_generator = QuestionGenerator(self.preprocessor, nlp, answer)
        hl = "[HL] since one year [HL]"
        with patch.object(QuestionGenerationRules,
                          '_QuestionGenerationRules__select_interrogative_pronoun_for_next_question',
                          return_value="since")\
                as __select_interrogative_pronoun_for_next_question:
            # we set the content in 2nd person manually (above) and patch the below method as we only have a mocked
            # preprocessor (the tokenization method call would not work)
            with patch.object(QuestionGenerationRules, 'create_2nd_person_sentence_from_1st_person'):
                self.assertTrue(question_generator.generate_with_highlight().startswith('How long'))
                self.assertTrue(hl in answer.content_with_hl)

    def test_generate_how_often_question(self):
        answer = Answer(" my jaw hurts.", 1)
        answer.content_in_2nd_pers = " your jaw hurts"
        question_generator = QuestionGenerator(self.preprocessor, nlp, answer)
        hl = "[HL] once a day [HL]"
        with patch.object(QuestionGenerationRules,
                          '_QuestionGenerationRules__select_interrogative_pronoun_for_next_question',
                          return_value="how often")\
                as __select_interrogative_pronoun_for_next_question:
            # we set the content in 2nd person manually (above) and patch the below method as we only have a mocked
            # preprocessor (the tokenization method call would not work)
            with patch.object(QuestionGenerationRules, 'create_2nd_person_sentence_from_1st_person'):
                self.assertTrue(question_generator.generate_with_highlight().startswith('How often'))
                self.assertTrue(hl in answer.content_with_hl)

    def test_generate_how_m_question(self):
        answer = Answer(" my teeth hurt.", 1)
        answer.content_in_2nd_pers = " your teeth hurt"
        question_generator = QuestionGenerator(self.preprocessor, nlp, answer)
        hl = "[HL] 5 of [HL]"
        with patch.object(QuestionGenerationRules,
                          '_QuestionGenerationRules__select_interrogative_pronoun_for_next_question',
                          return_value="how many")\
                as __select_interrogative_pronoun_for_next_question:
            # we set the content in 2nd person manually (above) and patch the below method as we only have a mocked
            # preprocessor (the tokenization method call would not work)
            with patch.object(QuestionGenerationRules, 'create_2nd_person_sentence_from_1st_person'):
                self.assertTrue(question_generator.generate_with_highlight().startswith('How m'))
                self.assertTrue(hl in answer.content_with_hl)

    # open: whom, whose, which
    # Note: When sentence is very short (e.g. [HL] My jaw [HL] hurts.) the highlighted part may not be "strong" enough
    # to trigger the desired wh-question.