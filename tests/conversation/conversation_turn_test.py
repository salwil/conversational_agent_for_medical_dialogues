import unittest
from unittest.mock import patch, MagicMock

import mock.mock

from conversation.conversation.conversation import Conversation
from conversation_turn.conversation_turn.topic import Topic
from conversation_turn.conversation_turn.turn import ConversationTurn
from model.model.question_generation import QuestionGenerator
from model.model.translation import Translator, TranslatorDeEn
from repository.repository.conversation_archive import ConversationArchival
from util.conversation_builder import ConversationBuilder

class ConversationTurnTest(unittest.TestCase):
#    def with_answer(self, content_en: str, number_of_usage = None, content_in_2nd_pers = None, content_with_hl = None, mental_state = None, turn_number = None):


    def setUp(self) -> None:
        self.conversation: Conversation = None
        #self.conversation.question_generator = MagicMock()
        #self.conversation.sentiment_detector = MagicMock()

    def tearDown(self) -> None:
        pass
        # Includes archive files closing
        #self.conversation.conversation_archive.terminate()

    def test_process_answer_and_profile_follow_up_question(self):
        next_profile_question = 'Was ist Ihr Vorname?'
        last_answer = "Mein Nachname ist Wildermuth"
        self.conversation = ConversationBuilder() \
            .with_question_generator()\
            .with_profile_question(next_profile_question, 'What is your first name?', 'first name')\
            .conversation()
        self.conversation_turn = ConversationTurn(1, self.conversation, last_answer)
        with patch.object(self.conversation.conversation_archive,
                          'write',
                          return_value=None) as mock_write_to_archive:
            with patch.object(self.conversation.question_generator, 'set_answer'):
                self.conversation_turn.process_answer_and_profile_question(next_profile_question)
                self.assertEqual(self.conversation_turn.answer.content, self.conversation.data_loader.answer_repo.answers[1].content)
                self.assertEqual(next_profile_question, self.conversation_turn.generated_question)
                mock_write_to_archive.assert_called_once_with({'question': next_profile_question,
                                                               'answer': last_answer})

    # This test is one of the hugest tests, it tests one entire conversation turn. It is mainly for verification, if
    # the interaction between objects works as expected. Whenever there is a fundamental change in the conversation
    # class or in activities of a conversation turn, this test should crash and has to be updated with the new
    # behavior such that it does not fail anymore.
    def test_process_answer_and_mandatory_follow_up_question(self):
        conversation = ConversationBuilder()\
            .with_repositories()\
            .with_question_generator()\
            .with_sentiment_detector()\
            .with_topic_inferencer()\
            .with_answer(content_en="I have jaw tension all the time.")\
            .conversation()
        conversation_turn = ConversationTurn(1, conversation, conversation.question_generator.answer.content)
        conversation_turn.process_answer_and_create_follow_up_question()
        self.assertTrue(conversation_turn.topic_number in conversation.data_loader.mandatory_question_repo.questions)
        topic_questions = conversation.data_loader.mandatory_question_repo.questions[conversation_turn.topic_number]
        self.assertTrue(conversation_turn.generated_question in [q.content for q in topic_questions])
        # assert that the questions are sorted according to their number of usage (those that have not been used yet
        # come first and those that have been used are in the back of the list
        #que = topic_questions[:len(topic_questions)-1]
        #self.assertEqual(1, topic_questions[:len(topic_questions)-1].number_of_usage)
        #self.assertTrue(topic_questions[0].number_of_usage <= topic_questions[:len(topic_questions)-1].number_of_usage)
        self.assertTrue(conversation_turn.answer.mental_state)
        self.assertTrue(conversation_turn.topic_number)
        self.assertTrue(conversation_turn.answer.topic_list)
        #self.assertTrue(conversation_turn.generated_question in conversation.question_generator.generated_questions_repository.questions)



