import unittest

import en_core_web_sm

from conversation_turn.conversation_element import QuestionIntro
from preprocess.lemmatize import EnglishLemmatizer
from preprocess.preprocess import Preprocessor
from repository.repositories import QuestionIntroRepository

# load computation-intensive classes only once
from tests.util.conversation_builder import ConversationBuilder

nlp = en_core_web_sm.load()
preprocessor = Preprocessor(EnglishLemmatizer(nlp), nlp)

class QuestionGenerationRulesTest(unittest.TestCase):

    def setUp(self) -> None:
        # the preprocessor is needed for pronoun replacement only, but this is tested in question_generation_rules and
        # therefore we mock the preprocessor (and also the pronoun replacement method in the below tests)
        self.conversation_builder = ConversationBuilder()\
            .with_question_intro_repository()\
            .with_question_intro('sad', "I'm sorry.", "Das tut mir leid.")\
            .with_question_generator(preprocessor, nlp)
        #self.current_turn_last = ConversationTurn(21, self.conversation, 'When have you been to the doctor?')

    def test_generate_highlight_not_who_not_what(self):
        conversation = self.conversation_builder.with_answer("Dr. Mayer told me to take Aspirin",
                                                             1,
                                                             content_in_2nd_pers="Dr. Mayer told you to take Aspirin")\
            .conversation()
        conversation.question_generator.rules.generate_highlight()
        self.assertGreater(len(conversation.question_generator.rules.allowed_pronouns),0)
        self.assertFalse('who' in conversation.question_generator.rules.allowed_pronouns)
        self.assertFalse('what' in conversation.question_generator.rules.allowed_pronouns)
        self.assertTrue("[HL]" in conversation.question_generator.answer.content_with_hl)
        self.assertNotEqual(conversation.question_generator.answer.content_with_hl, 'My doctor')
        self.assertNotEqual(conversation.question_generator.answer.content_with_hl, 'My jaw')

    def test_generate_highlight_not_when(self):
        conversation = self.conversation_builder.with_answer("It often hurts in the morning",
                                                             1,
                                                             content_in_2nd_pers="It often hurts in the morning")\
            .conversation()
        conversation.question_generator.rules.generate_highlight()
        self.assertGreater(len(conversation.question_generator.rules.allowed_pronouns),0)
        self.assertFalse('when' in conversation.question_generator.rules.allowed_pronouns)
        self.assertTrue("[HL]" in conversation.question_generator.answer.content_with_hl)

        self.assertNotEqual(conversation.question_generator.answer.content_with_hl, 'during')

    def test_generate_highlight_all_pronouns_allowed(self):
        conversation = self.conversation_builder.with_answer("When I am at home I feel better.",
                                                             1,
                                                             content_in_2nd_pers="When you are at home you feel better")\
            .conversation()
        conversation.question_generator.rules.generate_highlight()
        self.assertEqual(['when', 'where', 'what', 'who', 'how', 'how often', 'how many', 'since'],
                         conversation.question_generator.rules.allowed_pronouns)

    def test_create_2nd_person_sentence_pers_pronoun_and_verb_b(self):
        conversation = self.conversation_builder.with_answer("When I am at home I feel better.",
                                                             1).conversation()
        conversation.question_generator.rules.create_2nd_person_sentence_from_1st_person()
        self.assertEqual('When you are at home you feel better .',
                         conversation.question_generator.rules.answer.content_in_2nd_pers)
        # assert that original content is still there
        self.assertEqual("When I am at home I feel better.", conversation.question_generator.rules.answer.content)

    def test_create_2nd_person_sentence_short_forms(self):
        conversation = self.conversation_builder.with_answer("When I'm at home, my health gets better.",
                                                             1).conversation()
        conversation.question_generator.rules.create_2nd_person_sentence_from_1st_person()
        self.assertEqual("When you 're at home , your health gets better .",
                         conversation.question_generator.rules.answer.content_in_2nd_pers)
        self.assertEqual("When I'm at home, my health gets better.",
                         conversation.question_generator.rules.answer.content)

    def test_create_2nd_person_sentence_false_friend_have(self):
        conversation = self.conversation_builder.with_answer("I often have headache.",
                                                             1).conversation()
        conversation.question_generator.rules.create_2nd_person_sentence_from_1st_person()
        self.assertEqual("you often have headache .", conversation.question_generator.rules.answer.content_in_2nd_pers)
        self.assertEqual("I often have headache.", conversation.question_generator.rules.answer.content)

    def test_create_2nd_person_sentence_multiple_sentences(self):
        conversation = self.conversation_builder.with_answer("I often have headache. Sometimes I also have jaw tension."
                                                             " Especially during the night.",
                                                             1).conversation()
        conversation.question_generator.rules.create_2nd_person_sentence_from_1st_person()
        self.assertEqual("you often have headache . Sometimes you also have jaw tension . Especially during the night ."
                         , conversation.question_generator.rules.answer.content_in_2nd_pers)
        self.assertEqual("I often have headache. Sometimes I also have jaw tension. Especially during the night."
                         , conversation.question_generator.rules.answer.content)

    def test_select_question_intro(self):
        conversation = self.conversation_builder.with_answer("I often have headache. Sometimes I also have jaw tension."
                                                             " Especially during the night.",
                                                             1).conversation()
        self.create_question_intro_repository(conversation.question_generator.rules)
        self.assertEqual("I am sorry about how you feel", conversation.question_generator
                                                         .rules
                                                         .question_intro_repository
                                                         .mental_states['sad'][0]
                                                         .content)
        conversation.question_generator.rules.answer.mental_state = 'sad'
        conversation.question_generator.rules.select_question_intro()
        self.assertEqual("Don't worry.", conversation.question_generator
                                         .rules.question_intro_repository
                                         .mental_states['sad'][0]
                                         .content)
        self.assertEqual("I am sorry about how you feel", conversation.question_generator.rules.question_intro.content)

    def test_select_question_intro_with_salutation(self):
        conversation = self.conversation_builder.with_answer(
            "I often have headache. I also have jaw tension.", 1).conversation()
        self.create_question_intro_repository(conversation.question_generator.rules)
        self.assertEqual("I agree with you, [salutation].", conversation.question_generator
                                                         .rules
                                                         .question_intro_repository
                                                         .mental_states['neutral'][0]
                                                         .content)
        conversation.question_generator.rules.answer.mental_state = 'neutral'
        salutation = 'Andrea'
        conversation.question_generator.rules.select_question_intro(salutation)
        self.assertEqual("I agree with you, Andrea.", conversation.question_generator.rules.question_intro.content)

    def test_select_question_intro_mental_state_not_found(self):
        conversation = self.conversation_builder.with_answer("I often have headache. Sometimes I also have jaw tension."
                                                             " Especially during the night.",
                                                             1).conversation()
        self.create_question_intro_repository(conversation.question_generator.rules)
        conversation.question_generator.rules.answer.mental_state = 'confused'
        conversation.question_generator.rules.select_question_intro()
        self.assertIsNone(conversation.question_generator.rules.question_intro)

    # Helper
    def create_question_intro_repository(self, question_generation_rules):
        intro_sad_1 = QuestionIntro("I am sorry about how you feel",
                                    0,
                                    "Es tut mir leid, wie Sie sich fühlen.",
                                    'sad')
        intro_sad_2 = QuestionIntro("Don't worry.",
                                    0,
                                    "Machen Sie sich keine Sorgen.",
                                    'sad')
        intro_happy = QuestionIntro("I'm happy that you feel better.",
                                    0,
                                    "Es freut mich, dass es Ihnen besser geht.",
                                    'happy')
        intro_neutral = QuestionIntro("I agree with you, [salutation].",
                                      0,
                                      "Ich bin mit Ihnen einverstanden, [salutation].",
                                      'neutral')
        question_generation_rules.question_intro_repository = QuestionIntroRepository({})
        question_generation_rules.question_intro_repository.mental_states['sad'] = [intro_sad_1]
        question_generation_rules.question_intro_repository.mental_states['sad'].append(intro_sad_2)
        question_generation_rules.question_intro_repository.mental_states['happy'] = [intro_happy]
        question_generation_rules.question_intro_repository.mental_states['neutral'] = [intro_neutral]
