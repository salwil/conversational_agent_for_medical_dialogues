import unittest

from conversation.termination_criterion import TerminationCriterionForConversation
from conversation_turn.turn import ConversationTurn
from tests.util.conversation_builder import ConversationBuilder

class TerminationCriterionTest(unittest.TestCase):

    def setUp(self) -> None:
        self.termination_criterion = TerminationCriterionForConversation()
        self.conversation = ConversationBuilder()\
            .with_empathic_phrase_repository()\
            .with_empathic_phrase('sad', 'Es tut mir leid, das zu hören', 'I am sorry to hear that.')\
            .with_question_generator()\
            .conversation()
        self.current_turn_last = ConversationTurn(21, self.conversation, 'When have you been to the doctor?')
        self.current_turn_not_last = ConversationTurn(15, self.conversation, 'When have you been to the doctor?')

    def test_termination_criterion_is_given_because_max_turns(self):
        self.termination_criterion.update(self.current_turn_last)
        self.assertTrue(self.termination_criterion.given())

    def test_termination_criterion_is_given_because_user_quits(self):
        self.termination_criterion.check_user_terminate('quit!')
        self.assertTrue(self.termination_criterion.given())
        self.termination_criterion.check_user_terminate('q!')
        self.assertTrue(self.termination_criterion.given())

    def test_termination_criterion_not_given_with_turns(self):
        self.termination_criterion.update(self.current_turn_not_last)
        self.assertFalse(self.termination_criterion.given())

    def test_termination_criterion_not_given_by_user(self):
        self.termination_criterion.check_user_terminate('I have headache')
        self.assertFalse(self.termination_criterion.given())