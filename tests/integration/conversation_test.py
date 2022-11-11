import unittest
import csv

from conversation_turn.conversation_turn.conversation_element import ProfileQuestion, Question, QuestionType
from util.conversation_builder import ConversationBuilder
import src.conversation.conversation.main as main


class ConversationTest(unittest.TestCase):
    def setUp(self) -> None:
        self.profile_question = ProfileQuestion('Was ist dein Vorname?', 1, 'What is your first name?', QuestionType.PROFILE)
        self.profile_question.content_preprocessed = 'Vorname'
        self.mandatory_question = Question('What is your chief complaint?', 1, QuestionType.MANDATORY)
        self.mandatory_question.content_preprocessed = 'Chief complaint'
        self.conversation = ConversationBuilder()\
            .with_profile_question(self.profile_question)\
            .with_mandatory_question(self.mandatory_question)\
            .conversation()

    def tearDown(self) -> None:
        # Includes archive files closing
        self.conversation.conversation_archive.terminate()

    def test_maintain_conversation(self):
        main.maintain_conversation(self.conversation)
