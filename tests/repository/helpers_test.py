import unittest
import src.helpers.helpers.helpers as helpers

class HelpersTest(unittest.TestCase):

    def setUp(self) -> None:
        pass

    def test_get_project_path(self):
        self.assertTrue(helpers.get_project_path().endswith('conversational_agent_for_medical_dialogues'))