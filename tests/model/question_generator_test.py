import unittest
from unittest.mock import patch, MagicMock

import en_core_web_sm

from rules.question_generation_rules import QuestionGenerationRules

# load computation-intensive classes only once
from tests.util.conversation_builder import ConversationBuilder

nlp = en_core_web_sm.load()

class QuestionGenerationTest(unittest.TestCase):
    """
    This test class demonstrates how the defined triggers perfectly work for generating a question starting with the
    desired interrogative pronoun.
    Note that the we mock the interrogative pronoun, because in the real method it's chosen on a random base what would
    make it impossible to make meaningful assertions.
    Consequently THIS TEST DOES NOT TEST THE SELECTION OF THE INTERROGATIVE PRONOUN, but the method is tested in
    question_generation_rules_test.py
    """

    def setUp(self) -> None:
        # the preprocessor is needed for pronoun replacement only, but this is tested in question_generation_rules and
        # therefore we mock the preprocessor (and also the pronoun replacement method in the below tests)
        self.preprocessor = MagicMock()
        self.conversation_builder = ConversationBuilder()\
            .with_empathic_phrase_repository()\
            .with_empathic_phrase('sad', "I'm sorry.", "Das tut mir leid.")\
            .with_question_generator()

    """Why is temporarily removed from interrogative pronouns, as it is already generated quite often by the QG
    def test_generate_why_question(self):
        conversation = self.conversation_builder.with_answer("In the night I can't sleep ",
                                                             1,
                                                             content_in_2nd_pers="In the night you can't sleep",
                                                             mental_state='angry')\
            .conversation()
        hl = "[HL] because [HL]."
        with patch.object(QuestionGenerationRules,
                          '_QuestionGenerationRules__select_interrogative_pronoun_for_next_question',
                          return_value="why")\
                as __select_interrogative_pronoun_for_next_question:
            # we set the content in 2nd person manually (above) and patch the below method as we have only a mock
            # of preprocessor (the tokenization method call would not work)
            with patch.object(QuestionGenerationRules, 'create_2nd_person_sentence_from_1st_person'):
                self.assertTrue(conversation.question_generator.generate_with_highlight().startswith("Why"))
                self.assertTrue(hl in conversation.question_generator.answer.content_with_hl)
    """

    def test_generate_when_question(self):
        conversation = self.conversation_builder.with_answer("I often have ear pain",
                                                             1,
                                                             content_in_2nd_pers="You often have ear pain",
                                                             mental_state='afraid')\
            .conversation()
        hl = "[HL] during [HL]."
        with patch.object(QuestionGenerationRules,
                          '_QuestionGenerationRules__select_interrogative_pronoun_for_next_question',
                          return_value="when")\
                as __select_interrogative_pronoun_for_next_question:
            # we set the content in 2nd person manually (above) and patch the below method as we have only a mock
            # of preprocessor (the tokenization method call would not work)
            with patch.object(QuestionGenerationRules, 'create_2nd_person_sentence_from_1st_person'):
                self.assertTrue(conversation.question_generator.generate_with_highlight().startswith("When"))
                self.assertTrue(hl in conversation.question_generator.answer.content_with_hl)

    def test_generate_where_question(self):
        conversation = self.conversation_builder.with_answer("I often have pain",
                                                             1,
                                                             content_in_2nd_pers="You often have pain",
                                                             mental_state='afraid')\
            .conversation()
        hl = "[HL] at the hospital [HL]."
        with patch.object(QuestionGenerationRules,
                          '_QuestionGenerationRules__select_interrogative_pronoun_for_next_question',
                          return_value="where")\
                as __select_interrogative_pronoun_for_next_question:
            # we set the content in 2nd person manually (above) and patch the below method as we have only a mock
            # of preprocessor (the tokenization method call would not work)
            with patch.object(QuestionGenerationRules, 'create_2nd_person_sentence_from_1st_person'):
                self.assertTrue(conversation.question_generator.generate_with_highlight().startswith("Where"))
                self.assertTrue(hl in conversation.question_generator.answer.content_with_hl)

    def test_generate_how_question(self):
        conversation = self.conversation_builder.with_answer("I often have pain",
                                                             1,
                                                             content_in_2nd_pers="You often have pain",
                                                             mental_state='afraid')\
            .conversation()
        hl = "[HL] in form of [HL]."
        with patch.object(QuestionGenerationRules,
                          '_QuestionGenerationRules__select_interrogative_pronoun_for_next_question',
                          return_value="how")\
                as __select_interrogative_pronoun_for_next_question:
            # we set the content in 2nd person manually (above) and patch the below method as we have only a mock
            # of preprocessor (the tokenization method call would not work)
            with patch.object(QuestionGenerationRules, 'create_2nd_person_sentence_from_1st_person'):
                self.assertTrue(conversation.question_generator.generate_with_highlight().startswith("How"))
                self.assertTrue(hl in conversation.question_generator.answer.content_with_hl)

    def test_generate_who_question(self):
        conversation = self.conversation_builder.with_answer(" says that I have to stay in bed.",
                                                             1,
                                                             content_in_2nd_pers="says that you have to stay in bed",
                                                             mental_state='afraid')\
            .conversation()
        hl = "[HL] Somebody [HL]"
        with patch.object(QuestionGenerationRules,
                          '_QuestionGenerationRules__select_interrogative_pronoun_for_next_question',
                          return_value="who")\
                as __select_interrogative_pronoun_for_next_question:
            # we set the content in 2nd person manually (above) and patch the below method as we have only a mock
            # of preprocessor (the tokenization method call would not work)
            with patch.object(QuestionGenerationRules, 'create_2nd_person_sentence_from_1st_person'):
                self.assertTrue(conversation.question_generator.generate_with_highlight().startswith("Who"))
                self.assertTrue(hl in conversation.question_generator.answer.content_with_hl)

    def test_generate_what_question(self):
        conversation = self.conversation_builder.with_answer(" hurts when I eat food",
                                                             1,
                                                             content_in_2nd_pers=" hurts when you eat food",
                                                             mental_state='afraid')\
            .conversation()
        hl = "[HL] Something [HL]"
        with patch.object(QuestionGenerationRules,
                          '_QuestionGenerationRules__select_interrogative_pronoun_for_next_question',
                          return_value="what")\
                as __select_interrogative_pronoun_for_next_question:
            # we set the content in 2nd person manually (above) and patch the below method as we have only a mock
            # of preprocessor (the tokenization method call would not work)
            with patch.object(QuestionGenerationRules, 'create_2nd_person_sentence_from_1st_person'):
                self.assertTrue(conversation.question_generator.generate_with_highlight().startswith("What"))
                self.assertTrue(hl in conversation.question_generator.answer.content_with_hl)

    def test_generate_how_long_question(self):
        conversation = self.conversation_builder.with_answer(" my jaw hurts when I eat food",
                                                             1,
                                                             content_in_2nd_pers=" your jaw hurts when you eat food",
                                                             mental_state='dispaired')\
            .conversation()
        hl = "[HL] since one year [HL]"
        with patch.object(QuestionGenerationRules,
                          '_QuestionGenerationRules__select_interrogative_pronoun_for_next_question',
                          return_value="since")\
                as __select_interrogative_pronoun_for_next_question:
            # we set the content in 2nd person manually (above) and patch the below method as we have only a mock
            # of preprocessor (the tokenization method call would not work)
            with patch.object(QuestionGenerationRules, 'create_2nd_person_sentence_from_1st_person'):
                self.assertTrue(conversation.question_generator.generate_with_highlight().startswith('How long'))
                self.assertTrue(hl in conversation.question_generator.answer.content_with_hl)

    def test_generate_how_often_question(self):
        conversation = self.conversation_builder.with_answer(" my jaw hurts.",
                                                             1,
                                                             content_in_2nd_pers=" your jaw hurts",
                                                             mental_state='afraid')\
            .conversation()
        hl = "[HL] once a day [HL]"
        with patch.object(QuestionGenerationRules,
                          '_QuestionGenerationRules__select_interrogative_pronoun_for_next_question',
                          return_value="how often")\
                as __select_interrogative_pronoun_for_next_question:
            # we set the content in 2nd person manually (above) and patch the below method as we have only a mock
            # of preprocessor (the tokenization method call would not work)
            with patch.object(QuestionGenerationRules, 'create_2nd_person_sentence_from_1st_person'):
                self.assertTrue(conversation.question_generator.generate_with_highlight().startswith('How often'))
                self.assertTrue(hl in conversation.question_generator.answer.content_with_hl)

    def test_generate_how_m_question(self):
        conversation = self.conversation_builder.with_answer(" my teeth hurt.",
                                                             1,
                                                             content_in_2nd_pers=" your teeth hurt",
                                                             mental_state='afraid')\
            .conversation()
        hl = "[HL] 5 of [HL]"
        with patch.object(QuestionGenerationRules,
                          '_QuestionGenerationRules__select_interrogative_pronoun_for_next_question',
                          return_value="how many")\
                as __select_interrogative_pronoun_for_next_question:
            # we set the content in 2nd person manually (above) and patch the below method as we have only a mock
            # of preprocessor (the tokenization method call would not work)
            with patch.object(QuestionGenerationRules, 'create_2nd_person_sentence_from_1st_person'):
                self.assertTrue(conversation.question_generator.generate_with_highlight().startswith('How m'))
                self.assertTrue(hl in conversation.question_generator.answer.content_with_hl)

    # open: whom, whose, which
    # Note: When sentence is very short (e.g. [HL] My jaw [HL] hurts.) the highlighted part may not be "strong" enough
    # to trigger the desired wh-question.