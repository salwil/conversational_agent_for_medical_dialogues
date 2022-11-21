import unittest
from unittest.mock import patch, MagicMock

from conversation_turn.conversation_turn.turn import ConversationTurn
from util.conversation_builder import ConversationBuilder

class ConversationTurnTest(unittest.TestCase):

    def setUp(self) -> None:
        self.last_answer = "Mein Nachname ist Wildermuth"
        self.next_profile_question = 'Was ist Ihr Vorname?'
        self.next_mandatory_question = 'Was sind Ihre Hauptbeschwerden?'
        self.conversation = ConversationBuilder()\
            .with_profile_question(self.next_profile_question, 'What is your first name?', 'Vorname')\
            .with_mandatory_question(self.next_mandatory_question, 'What is your chief complaint?', 'Hauptbeschwerden')\
            .with_question_intro('sad', 'Es tut mir leid, das zu hören', 'I am sorry to hear that.')\
            .conversation()
        self.conversation.question_generator = MagicMock()
        self.conversation.sentiment_detector = MagicMock()

    def tearDown(self) -> None:
        # Includes archive files closing
        self.conversation.conversation_archive.terminate()

    def test_process_question_and_answer_for_patient_profile(self):
        self.conversation_turn = ConversationTurn(1, self.conversation, self.last_answer)
        with patch.object(self.conversation.conversation_archive,
                          'write',
                          return_value=None) as mock_write_to_archive:
            with patch.object(self.conversation.question_generator, 'set_answer'):
                self.conversation_turn.process_question_and_answer_for_patient_profile(self.next_profile_question)
                self.assertEqual(self.conversation_turn.answer.content, self.conversation.data_loader.answer_repo.answers[1].content)
                self.assertEqual(self.next_profile_question, self.conversation_turn.generated_question)
                mock_write_to_archive.assert_called_once_with({'question': self.next_profile_question,
                                                               'answer': self.last_answer})

    def test_process_question_and_answer_for_mandatory_question(self):
        self.conversation_turn = ConversationTurn(1, self.conversation, self.last_answer)
        with patch.object(self.conversation.conversation_archive,
                          'write',
                          return_value=None) as mock_write_to_archive:
            with patch.object(self.conversation.question_generator, 'set_answer'):
                self.conversation_turn.process_question_and_answer_for_patient_profile(self.next_mandatory_question)
                self.assertEqual(self.conversation_turn.answer.content, self.conversation.data_loader.answer_repo.answers[1].content)
                self.assertEqual(self.next_mandatory_question, self.conversation_turn.generated_question)
                mock_write_to_archive.assert_called_once_with({'question': self.next_mandatory_question,
                                                               'answer': self.last_answer})



