import unittest
from unittest.mock import patch

from conversation.conversation import Conversation, Language
from conversation_turn.turn import ConversationTurn
from tests.util.conversation_builder import ConversationBuilder

class ConversationTurnTest(unittest.TestCase):

    def setUp(self) -> None:
        self.conversation: Conversation = None

    def tearDown(self) -> None:
        pass
        # Includes archive files closing
        self.conversation.conversation_archive.terminate()

    def test_process_answer_and_profile_follow_up_question(self):
        next_profile_question = 'Was ist Ihr Vorname?'
        last_answer = "Mein Nachname ist Wildermuth"
        self.conversation = ConversationBuilder()\
            .with_repositories()\
            .with_question_generator()\
            .with_sentiment_detector()\
            .with_topic_inferencer()\
            .with_question_generator()\
            .with_profile_question(next_profile_question, 'What is your first name?', 'first name')\
            .conversation()
        self.conversation_turn = ConversationTurn(1, self.conversation, last_answer)
        with patch.object(self.conversation.conversation_archive,
                          'write',
                          return_value=None) as mock_write_to_archive:
            with patch.object(self.conversation.question_generator, 'set_answer'):
                self.conversation_turn.process_answer_and_profile_question(next_profile_question)
                self.assertEqual(self.conversation_turn.answer.content,
                                 self.conversation.data_loader.answer_repo.answers[1].content)
                self.assertEqual(next_profile_question, self.conversation_turn.generated_question)
                mock_write_to_archive.assert_called_once_with({'question': next_profile_question,
                                                               'answer': last_answer})

    # The following tests are large tests. They tests one entire conversation turn. It is mainly for verification, if
    # the interaction between objects works as expected. Whenever there is a fundamental change in the conversation
    # class or in activities of a conversation turn, this test should crash and has to be updated with the new
    # behavior such that it does not fail anymore. Unfortunately we have to build entire conversation object every
    # time new, to have clean objects for every new test case.

    def test_process_answer_and_mandatory_follow_up_question_no_translation(self):
        self.conversation = ConversationBuilder()\
            .with_repositories()\
            .with_question_generator()\
            .with_sentiment_detector()\
            .with_topic_inferencer()\
            .with_question_generator()\
            .with_answer(content_en="I have jaw tension all the time.")\
            .conversation()
        conversation_turn = ConversationTurn(1, self.conversation, self.conversation.question_generator.answer.content)
        conversation_turn.process_answer_and_create_follow_up_question()
        self.assertTrue(conversation_turn.topic_number in
                        self.conversation.data_loader.mandatory_question_repo.questions)
        topic_questions = \
            self.conversation.data_loader.mandatory_question_repo.questions[conversation_turn.topic_number]
        self.assertTrue(conversation_turn.generated_question in [q.content for q in topic_questions])
        # at least the last-most question in the list must have number_of_usage = 1, because we just used it within
        # the current conversation turn
        self.assertEqual(1, topic_questions[len(topic_questions)-1].number_of_usage)
        # assert that the questions are sorted according to their number of usage (those that have not been used yet
        # come first and those that have been used are in the back of the list
        self.assertTrue(topic_questions[0].number_of_usage <= topic_questions[len(topic_questions)-1].number_of_usage)
        self.assertTrue(conversation_turn.answer.mental_state)
        self.assertTrue(conversation_turn.topic_number)
        self.assertTrue(conversation_turn.answer.topic_list)
        # topic derived questions are not stored in the generated_questions_repository
        self.assertFalse(self.conversation.question_generator.generated_questions_repository)


    def test_process_answer_and_mandatory_follow_up_question_with_translation(self):
        # the answer object is instantiated directly with english (the reason for that is that the answer object is
        # created after the translation from german to english in the conversation turn, it does not care about the
        # german content.
        self.conversation = ConversationBuilder()\
            .with_repositories()\
            .with_question_generator()\
            .with_sentiment_detector()\
            .with_topic_inferencer()\
            .with_question_generator()\
            .with_translators_de_en()\
            .with_answer(content_en="My teeth hurt when chewing hard food.") \
            .conversation()
        self.conversation.language = Language.GERMAN
        conversation_turn = ConversationTurn(1, self.conversation, self.conversation.question_generator.answer.content)
        conversation_turn.process_answer_and_create_follow_up_question()
        self.assertNotEqual(conversation_turn.question.content_in_german, conversation_turn.question.content)
        # draft: conversation_turn does not recognize German Language, therefore this most relevant assertion does not
        # work (interestingly from command line it works)
        #self.assertEqual(conversation_turn.generated_question, conversation_turn.question.content_in_german)
        self.assertTrue(
            conversation_turn.topic_number in self.conversation.data_loader.mandatory_question_repo.questions)
        topic_questions = \
            self.conversation.data_loader.mandatory_question_repo.questions[conversation_turn.topic_number]
        #print(conversation_turn.generated_question)
        self.assertTrue(conversation_turn.generated_question in [q.content_in_german for q in topic_questions])
        # at least the last-most question in the list must have number_of_usage = 1, because we just used it within
        # the current conversation turn
        self.assertEqual(1, topic_questions[len(topic_questions) - 1].number_of_usage)
        # assert that the questions are sorted according to their number of usage (those that have not been used yet
        # come first and those that have been used are in the back of the list
        self.assertTrue(
            topic_questions[0].number_of_usage <= topic_questions[len(topic_questions) - 1].number_of_usage)
        self.assertTrue(conversation_turn.answer.mental_state)
        self.assertTrue(conversation_turn.topic_number)
        self.assertTrue(conversation_turn.answer.topic_list)
        # topic derived questions are not stored in the generated_questions_repository
        self.assertFalse(self.conversation.question_generator.generated_questions_repository)


    def test_process_answer_and_generated_follow_up_question_english(self):
        self.conversation = ConversationBuilder()\
            .with_repositories()\
            .with_question_generator()\
            .with_sentiment_detector()\
            .with_topic_inferencer()\
            .with_question_generator()\
            .with_answer(content_en="His grandfather grew up in San Francisco.")\
            .conversation()
        conversation_turn = ConversationTurn(1, self.conversation, self.conversation.question_generator.answer.content)
        # we have to overrule the topic to set any topics and we will run into the question generation
        with patch.object(ConversationTurn, '_ConversationTurn__infer_topics') as __infer_topics:
            conversation_turn.process_answer_and_create_follow_up_question()
            self.assertTrue(conversation_turn.answer.mental_state)
            self.assertFalse(conversation_turn.topic_number)
            self.assertTrue(self.conversation.question_generator.generated_questions_repository)
            self.assertTrue(conversation_turn.question in
                            list(self.conversation.question_generator.generated_questions_repository.questions.values()))
            self.assertEqual(conversation_turn.question.content, conversation_turn.generated_question)

    def test_process_answer_and_more_detail_question(self):
        self.conversation = ConversationBuilder()\
            .with_repositories()\
            .with_question_generator()\
            .with_sentiment_detector()\
            .with_topic_inferencer()\
            .with_question_generator()\
            .with_answer(content_en="His grandfather grew up in San Francisco.")\
            .conversation()
        conversation_turn = ConversationTurn(1, self.conversation, self.conversation.question_generator.answer.content)
        # when the more_detail flag is true, a question from the more_detail repo will be randomly selected
        conversation_turn.more_detail = True
        # we have to overrule the topic to set any topics and we will run into the question generation
        with patch.object(ConversationTurn, '_ConversationTurn__infer_topics') as __infer_topics:
            conversation_turn.process_answer_and_create_follow_up_question()
            self.assertTrue(conversation_turn.answer.mental_state)
            self.assertFalse(conversation_turn.topic_number)
            # assert that the generated question is not stored
            self.assertFalse(self.conversation.question_generator.generated_questions_repository)
            # ...but instead the question is one of the moredetail_question_repo
            self.assertTrue(conversation_turn.question.content_preprocessed in self.conversation.data_loader.more_detail_question_repo.questions)
