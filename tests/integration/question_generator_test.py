import unittest

from src.model.model.question_generation import QuestionGenerator

class QuestionGenerationTest(unittest.TestCase):

    def setUp(self) -> None:
        self.question_generator = QuestionGenerator()

    def test_generate_why_question(self):
        answer = "In the night you can't sleep, [HL]because ... [HL]."
        self.assertTrue(self.question_generator.generate(answer).startswith("Why"))

    def test_generate_when_question(self):
        answer = "I often have ear pain, [HL]during ... [HL]."
        self.assertTrue(self.question_generator.generate(answer).startswith("When"))

    def test_generate_where_question(self):
        answer = "I often have pain, [HL]in London ... [HL]."
        self.assertTrue(self.question_generator.generate(answer).startswith("Where"))

    def test_generate_how_question(self):
        answer = "I often have pain, [HL] in form of ... [HL]."
        self.assertTrue(self.question_generator.generate(answer).startswith("How"))

    def test_generate_who_question(self):
        answer = "[HL] My doctor [HL] says that I have to stay in bed."
        self.assertTrue(self.question_generator.generate(answer).startswith("Who"))

    def test_generate_what_question(self):
        answer = "[HL] My jaw [HL] hurts when I eat food."
        self.assertTrue(self.question_generator.generate(answer).startswith("What"))

    def test_generate_since_question(self):
        answer = "[HL] Since one year [HL] my jaw hurts when I eat food."
        self.assertTrue('since' in self.question_generator.generate(answer).lower())


    # open: whom, whose, which
    # Note: When sentence is very short (e.g. [HL] My jaw [HL] hurts.) the highlighted part may not be "strong" enough
    # to trigger the desired wh-question.