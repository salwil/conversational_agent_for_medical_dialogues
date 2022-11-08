import unittest

from src.model.model.translation import TranslatorDeEn, TranslatorEnDe

class QuestionGenerationTest(unittest.TestCase):

    def setUp(self) -> None:
        self.de_en_translator = TranslatorDeEn()
        self.en_de_translator = TranslatorEnDe()
        self.sentence_german = ["Kiefer tut weh, Kopfschmerzen"]
        self.sentence_english = ["After which accident did your chief complaint start?"]

    def test_translate_from_german_to_english(self):
        translation = self.de_en_translator.translate(self.sentence_german).lower()
        self.assertTrue('jaw' in translation)
        self.assertTrue('hurt' in translation)
        self.assertTrue('head' in translation)

    def test_translate_from_english_to_german(self):
        translation = self.en_de_translator.translate(self.sentence_english).lower()
        self.assertTrue('nach' in translation)
        self.assertTrue('unfall' in translation)
        self.assertTrue('hauptbeschwerde' in translation)
