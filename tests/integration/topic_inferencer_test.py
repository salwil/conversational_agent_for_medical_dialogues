import pathlib
import unittest
from unittest.mock import patch

import src.helpers.helpers.helpers as helpers
from model.model.topic_inference import TopicInferencer

path = helpers.get_project_path() + '/src/model/language_models/'
path_to_pretrained_mallet_model = path + 'mallet_topics/'
path_to_mallet = path + 'mallet-2.0.8/bin/mallet'
path_to_new_mallet_model = path + 'mallet_inferred_topics/'

class TopicInferencerTest(unittest.TestCase):

    def setUp(self) -> None:

        self.topic_inferencer = TopicInferencer(10)

    @unittest.skipIf(not pathlib.Path(path_to_pretrained_mallet_model + 'mallet.training').exists(),
                     "Please add the training file to the model/language_models/mallet_topics folder.")
    @unittest.skipIf(not pathlib.Path(path_to_pretrained_mallet_model + 'mallet.topic_distributions.10').exists(),
                     "Please add the mallet.topic_distributions.10 file to the model/language_models/mallet_topics "
                     "folder.")
    @unittest.skipIf(not pathlib.Path(path_to_pretrained_mallet_model + 'mallet.topic_keys.10').exists(),
                     "Please add the mallet.topic_keys.10 file to the model/language_models/mallet_topics folder.")
    def test_infer_topic_for_sentence(self):
        paths = [pathlib.Path(path_to_new_mallet_model + 'training.txt'),
                 pathlib.Path(path_to_new_mallet_model + 'training'),
                 pathlib.Path(path_to_new_mallet_model + 'mallet.topic_distributions.1')]
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
        relative_topic_weights = [0.01, 0.1, 0.02, 0.3, 0.05, 0.45, 0.035, 0.01, 0.016, 0.009]
        # check preconditions
        self.assertEqual(10, len(relative_topic_weights))
        with patch.object(TopicInferencer, '_TopicInferencer__compute_relative_topic_weights', return_value=relative_topic_weights) as __compute_relative_topic_weights:
            topic_list = self.topic_inferencer.get_best_topics(3)
            self.assertTrue(3, len(topic_list))
            self.assertTrue('mouth' in topic_list[0].topic_keys)
            self.assertTrue('chew' in topic_list[0].topic_keys)
            self.assertTrue('crack' in topic_list[0].topic_keys)
            self.assertEqual(0.45, topic_list[0].probability)
            self.assertEqual(0.3, topic_list[1].probability)
            self.assertEqual(0.1, topic_list[2].probability)
            self.assertEqual(5, topic_list[0].topic_number)
