import unittest

from src.model.model.load_model import Model, Seq2SeqModelLoader, SequenceClassificationModelLoader

class ConversationElementTest(unittest.TestCase):

    def setUp(self) -> None:
        self.seq2seq_loader = Seq2SeqModelLoader()
        self.classification_loader = SequenceClassificationModelLoader()

    def test_model_loader_bart_squad_qg_hl(self):
        self.assertIsNotNone(self.seq2seq_loader.load_model(Model.BART_HLSQQ))
        self.assertIsNotNone(self.seq2seq_loader.load_tokenizer(Model.BART_HLSQQ))

    def test_model_loader_bart_mnli(self):
        self.assertIsNotNone(self.classification_loader.load_model(Model.BART_MNLI))
        self.assertIsNotNone(self.classification_loader.load_tokenizer(Model.BART_MNLI))