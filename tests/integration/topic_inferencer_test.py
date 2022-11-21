import pathlib
import unittest
from unittest.mock import patch

import src.helpers.helpers.helpers as helpers
from model.model.topic import TopicInferencer


class TopicInferencerTest(unittest.TestCase):

    def setUp(self) -> None:
        self.path = helpers.get_project_path() + '/src/model/language_models/'
        self.path_to_mallet = self.path + 'mallet-2.0.8/bin/mallet'
        self.path_to_pretrained_mallet_model = self.path + 'mallet_topics/'
        self.path_to_new_mallet_model = self.path + 'mallet_inferred_topics/'
        self.topic_inferencer = TopicInferencer(self.path_to_mallet, self.path_to_pretrained_mallet_model,
                                                self.path_to_new_mallet_model)

    def test_infer_topic_for_sentence(self):
        paths = [pathlib.Path(self.path_to_new_mallet_model + 'training.txt'),
                 pathlib.Path(self.path_to_new_mallet_model + 'training'),
                 pathlib.Path(self.path_to_new_mallet_model + 'mallet.topic_distributions.1')]
        for path in paths:
            pathlib.Path.unlink(path, missing_ok=True)
            # make sure, file is really deleted
            self.assertFalse(path.exists())
        text_preprocessed = "toothache every day feel bad sometimes jaw hurts sometimes jaw tension often ask myself " \
                            "if will ever go away again night problems falling asleep evening the pain worse morning " \
                            "they get worse during day head hurts."
        text_preprocessed = "job very stressful need urgently relax"
        text_preprocessed = "work 10 hour day since 2 year job annoying "
        text_preprocessed = "doctor treatment tooth since dentist year dental implant see take clarification remove xxx problem still inflammation result crown nerve"
        self.topic_inferencer.infer_topic(text_preprocessed)
        for path in paths:
            self.assertTrue(path.exists())

    def test_get_3_best_topics(self):
        """
        The preprocessed input is treated as one single document, therefore we always expect only one line of topic
        distributions --> one list element in list.
        """
        topic_distributions = [[0.01, 0.1, 0.02, 0.3, 0.05, 0.45, 0.035, 0.01, 0.016, 0.009]]
        # check preconditions
        self.assertEqual(1, sum(topic_distributions[0]))
        self.assertEqual(10, len(topic_distributions[0]))
        with patch.object(TopicInferencer, '_TopicInferencer__load_topic_distributions',
                          return_value=topic_distributions) \
                as __load_topic_distributions:
            topic_list = topic = self.topic_inferencer.get_best_topics(3)
            self.assertTrue(3, len(topic_list))
            self.assertTrue('tongue' in topic_list[0].topic_keys)
            self.assertTrue('throat' in topic_list[0].topic_keys)
            self.assertTrue('dry' in topic_list[0].topic_keys)
            self.assertEqual(0.45, topic_list[0].probability)
            self.assertEqual(0.3, topic_list[1].probability)
            self.assertEqual(0.1, topic_list[2].probability)