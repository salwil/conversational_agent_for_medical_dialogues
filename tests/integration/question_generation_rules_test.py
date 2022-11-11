import unittest

from rules.rules.question_generation_rules import QuestionGenerationRules



class QuestionGenerationRulesTest(unittest.TestCase):

    def setUp(self) -> None:
        self.question_generation_rules = QuestionGenerationRules()

    def test_data_loader_profile_question(self):
        text = 'European authorities fined Google a record $5.1 billion on Wednesday for abusing its power in the ' \
               'mobile phone market and ordered the company to alter its practices'
        self.question_generation_rules.determine_sentence_adverbiale(text)




