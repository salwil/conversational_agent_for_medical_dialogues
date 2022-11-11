import unittest
from unittest.mock import patch

from conversation_turn.conversation_turn.conversation_element import ProfileQuestion, QuestionType, Question, Answer
from conversation_turn.conversation_turn.turn import ConversationTurn
from util.conversation_builder import ConversationBuilder

class ConversationTurnTest(unittest.TestCase):

    def setUp(self) -> None:
        self.last_answer = "Mein Nachname ist Wildermuth"
        self.next_profile_question = ProfileQuestion('Was ist dein Vorname?', 1, 'What is your first name?', QuestionType.PROFILE)
        self.next_profile_question.content_preprocessed = 'Vorname'
        self.next_mandatory_question = Question('Was sind deine Hauptbeschwerden?', 1, QuestionType.MANDATORY)
        self.next_mandatory_question.content_preprocessed = 'Hauptbeschwerden'
        self.conversation = ConversationBuilder()\
            .with_profile_question(self.next_profile_question)\
            .with_mandatory_question(self.next_mandatory_question)\
            .conversation()
        self.conversation_turn = ConversationTurn(1, self.conversation, self.last_answer)

    def tearDown(self) -> None:
        # Includes archive files closing
        self.conversation.conversation_archive.terminate()

    def test_process_question_and_answer_for_patient_profile(self):
        answer = Answer('Mein Nachname ist Wildermuth', 1)
        with patch.object(self.conversation.conversation_archive,
                          'write',
                          return_value=None) as mock_write_to_archive:
            self.conversation_turn.process_question_and_answer_for_patient_profile(self.next_profile_question.content)
            self.assertTrue(self.last_answer in self.conversation.data_loader.answer_repo.answers)
            self.assertEqual(self.next_profile_question.content, self.conversation_turn.generated_question)
            mock_write_to_archive.assert_called_once_with({'question': self.next_profile_question.content,
                                                           'answer': self.last_answer})

    def test_process_question_and_answer_for_mandatory_question(self):
        with patch.object(self.conversation.conversation_archive,
                          'write',
                          return_value=None) as mock_write_to_archive:
            self.conversation_turn.process_question_and_answer_for_patient_profile(self.next_mandatory_question.content)
            self.assertTrue(self.last_answer in self.conversation.data_loader.answer_repo.answers)
            self.assertEqual(self.next_mandatory_question.content, self.conversation_turn.generated_question)
            mock_write_to_archive.assert_called_once_with({'question': self.next_mandatory_question.content,
                                                           'answer': self.last_answer})

    """
    def test_process_answer_and_create_follow_up_question(self):
        self.conversation_turn.process_answer_and_create_follow_up_question()
        print(self.conversation_turn.generated_question)
        self.assertTrue(self.conversation_turn.generated_question > ' ')
        """

