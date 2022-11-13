import unittest
from unittest.mock import patch, MagicMock

import en_core_web_sm

from conversation_turn.conversation_turn.conversation_element import Answer
from src.model.model.question_generation import QuestionGenerator

# load computation-intensive classes only once
nlp = en_core_web_sm.load()

class QuestionGenerationTest(unittest.TestCase):
    """
    This test class demonstrates how the defined triggers perfectly work for generating a question starting with the
    desired interrogative pronoun.
    Note that the private __generate_highlight method is not controllable as it generates the highlight on a random
    base. Therefore, the return value of this method is mocked: we rely on a highlight that is always the same for
    making valuable assertions on the interrogative pronoun.
    """

    def setUp(self) -> None:
        # the preprocessor is needed for pronoun replacement only, but this is tested in question_generation_rules and
        # therefore we mock the preprocessor (and also the pronoun replacement method in the below tests)
        self.preprocessor = MagicMock()
        self.question_generator = QuestionGenerator(self.preprocessor, nlp)

    def test_generate_why_question(self):
        answer = Answer("In the night I can't sleep ", 0)
        hl = "[HL]because ... [HL]."
        with patch.object(self.question_generator, '_QuestionGenerator__generate_highlight', return_value=answer.content + hl)\
                as __generate_highlight:
            # no need for replacing the pronoun for these tests, it's only performance overhead
            with patch.object(self.question_generator, '_QuestionGenerator__replace_pronouns_first_person'):
                self.assertTrue(self.question_generator.generate(answer).startswith("Why"))

    def test_generate_when_question(self):
        answer = "I often have ear pain, "
        hl = "[HL]during ... [HL]."
        with patch.object(self.question_generator, '_QuestionGenerator__generate_highlight', return_value=answer + hl)\
                as __generate_highlight:
            with patch.object(self.question_generator, '_QuestionGenerator__replace_pronouns_first_person'):
                self.assertTrue(self.question_generator.generate(answer).startswith("When"))

    def test_generate_where_question(self):
        answer = "I often have pain, "
        hl = "[HL]in London ... [HL]."
        with patch.object(self.question_generator, '_QuestionGenerator__generate_highlight', return_value=answer + hl)\
                as __generate_highlight:
            with patch.object(self.question_generator, '_QuestionGenerator__replace_pronouns_first_person'):
                self.assertTrue(self.question_generator.generate(answer).startswith("Where"))

    def test_generate_how_question(self):
        answer = "I often have pain, "
        hl = "[HL] in form of ... [HL]."
        with patch.object(self.question_generator, '_QuestionGenerator__generate_highlight', return_value=answer + hl)\
                as __generate_highlight:
            with patch.object(self.question_generator, '_QuestionGenerator__replace_pronouns_first_person'):
                self.assertTrue(self.question_generator.generate(answer).startswith("How"))

    def test_generate_who_question(self):
        answer = " says that I have to stay in bed."
        hl = "[HL] Dr. Peter Muller [HL]"
        with patch.object(self.question_generator, '_QuestionGenerator__generate_highlight', return_value=hl + answer)\
                as __generate_highlight:
            with patch.object(self.question_generator, '_QuestionGenerator__replace_pronouns_first_person'):
                self.assertTrue(self.question_generator.generate(answer).startswith("Who"))

    def test_generate_what_question(self):
        answer = " hurts when I eat food."
        hl = "[HL] My jaw [HL]"
        with patch.object(self.question_generator, '_QuestionGenerator__generate_highlight', return_value=hl + answer)\
                as __generate_highlight:
            with patch.object(self.question_generator, '_QuestionGenerator__replace_pronouns_first_person'):
                self.assertTrue(self.question_generator.generate(answer).startswith("What"))

    def test_generate_since_question(self):
        answer = " my jaw hurts when I eat food."
        hl = "[HL] Since one year [HL]"
        with patch.object(self.question_generator, '_QuestionGenerator__generate_highlight', return_value=hl + answer)\
                as __generate_highlight:
            with patch.object(self.question_generator, '_QuestionGenerator__replace_pronouns_first_person'):
                self.assertTrue('since' in self.question_generator.generate(answer))

    def test_generate_how_often_question(self):
        answer = " my jaw hurts."
        hl = "[HL] Once a day [HL]"
        with patch.object(self.question_generator, '_QuestionGenerator__generate_highlight', return_value=hl + answer)\
                as __generate_highlight:
            with patch.object(self.question_generator, '_QuestionGenerator__replace_pronouns_first_person'):
                self.assertTrue(self.question_generator.generate(answer).startswith("How often"))

    def test_generate_how_m_question(self):
        answer = " my teeth hurt."
        hl = "[HL] 5 of [HL]"
        with patch.object(self.question_generator, '_QuestionGenerator__generate_highlight', return_value=hl + answer)\
                as __generate_highlight:
            with patch.object(self.question_generator, '_QuestionGenerator__replace_pronouns_first_person'):
                self.assertTrue(self.question_generator.generate(answer).startswith("How m"))

    # open: whom, whose, which
    # Note: When sentence is very short (e.g. [HL] My jaw [HL] hurts.) the highlighted part may not be "strong" enough
    # to trigger the desired wh-question.