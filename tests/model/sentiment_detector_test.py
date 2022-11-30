import unittest

from model.sentiment_detection import SentimentDetector


class SentimentDetectionTest(unittest.TestCase):

    def setUp(self) -> None:
        self.sentiment_detector = SentimentDetector(['sad', 'happy'])

    def test_predict_mental_state(self):
        sad_sentence = 'I feel really bad.'
        happy_sentence = 'My life is great.'
        self.assertEqual(self.sentiment_detector.predict_mental_state(sentence=sad_sentence), 'sad')
        self.assertEqual(self.sentiment_detector.predict_mental_state(sentence=happy_sentence), 'happy')

    def test_predict_mental_state_neutral(self):
        neutral_sentence = "I work as a carpenter."
        self.assertEqual('neutral', self.sentiment_detector.predict_mental_state(sentence=neutral_sentence))
"""
    def test_predict_mental_state(self):
        answer = Answer("I don't feel good.", 1)
        answer.content_preprocessed = "feel good"
        self.conversation_turn = ConversationTurn(1, self.conversation, answer.content)
        # test conversation turn with mental state prediction
        with patch.object(self.conversation.sentiment_detector, 'predict_mental_state', return_value='sad'):
            # self.conversation_turn.question = Question('What is your chief complaint?', 0, QuestionType.GENERATED)
            self.conversation_turn.predict_mental_state()
            # print(self.conversation_turn.generated_question)
            # self.assertTrue(self.conversation_turn.generated_question > ' ')
            """

