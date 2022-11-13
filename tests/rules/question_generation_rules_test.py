import unittest

from rules.rules.question_generation_rules import QuestionGenerationRules

class QuestionGenerationRulesTest(unittest.TestCase):

    def setUp(self) -> None:
        self.question_generation_rules = QuestionGenerationRules()

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
        highlight = self.question_generation_rules.generate_highlight("When I am at home I feel better.")
        self.assertEqual(['why', 'when', 'where', 'what', 'who', 'how', 'how often', 'how many', 'since'],
                         self.question_generation_rules.allowed_pronouns)
