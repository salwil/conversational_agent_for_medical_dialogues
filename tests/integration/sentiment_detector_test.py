import unittest

from src.model.model.sentiment_detection import SentimentDetector


class SentimentDetectionTest(unittest.TestCase):

    def setUp(self) -> None:
        self.sentiment_detector = SentimentDetector(['sad', 'happy'])
        self.sentence_sad = 'I feel really bad.'
        self.sentence_happy = 'My life is great.'

    def test_determine_mental_state(self):
        self.assertEqual(self.sentiment_detector.determine_mental_state(sentence=self.sentence_sad), 'sad')
        self.assertEqual(self.sentiment_detector.determine_mental_state(sentence=self.sentence_happy), 'happy')