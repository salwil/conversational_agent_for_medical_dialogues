import unittest

from model.load_model import Model, Seq2SeqModelLoader, SequenceClassificationModelLoader

class ConversationElementTest(unittest.TestCase):

    def setUp(self) -> None:
        self.seq2seq_loader = Seq2SeqModelLoader()
        self.classification_loader = SequenceClassificationModelLoader()

    def test_model_loader_bart_squad_qg_hl(self):
        self.assertIsNotNone(self.seq2seq_loader.load_model(Model.QUESTION_GENERATION))
        self.assertIsNotNone(self.seq2seq_loader.load_tokenizer(Model.QUESTION_GENERATION))

    def test_model_loader_bart_mnli(self):
        self.assertIsNotNone(self.classification_loader.load_model(Model.SENTIMENT_DETECTION))
        self.assertIsNotNone(self.classification_loader.load_tokenizer(Model.SENTIMENT_DETECTION))