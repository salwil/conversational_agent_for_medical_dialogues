import unittest

import src.helpers.helpers.helpers as helpers
from conversation_turn.conversation_turn.conversation_element import Answer
from model.model.load_model import Model
from model.model.topic import TopicInferencer


class TopicInferencerTest(unittest.TestCase):

    def setUp(self) -> None:
        self.path = helpers.get_project_path() +  '/src/model/model/'
        self.model_checkpoint = Model.TOPIC.value
        self.topic_inferencer = TopicInferencer(self.path, self.model_checkpoint)

    def test_infer_topic_for_sentence(self):
        text = "I have toothache every day and I feel bad. Sometimes my jaw hurts and sometimes I have jaw tension." \
               "Often I ask myself if that will ever go away again. In the night I have problems falling asleep" \
               ". In the evening the pain is worse than in the morning. They get worse during the day. Sometimes " \
               "my entire head hurts."
        answer = Answer(text, 0)
        answer.content_preprocessed = "I have toothache every day and I feel bad. Sometimes my jaw hurts and sometimes I have jaw tension." \
               "Often I ask myself if that will ever go away again. In the night I have problems falling asleep" \
               ". In the evening the pain is worse than in the morning. They get worse during the day. Sometimes " \
               "my entire head hurts."
        answer.content_preprocessed = "Stress, either physiological, biological or psychological, is an organism's response to a stressor such as an environmental condition.[1] Stress is the body's method of reacting to a condition such as a threat, challenge or physical and psychological barrier. There are two hormones that an individual produces during a stressful situation, these are well known as adrenaline and cortisol.[2] Stimuli that alter an organism's environment are responded to by multiple systems in the body.[3] In humans and most mammals, the autonomic nervous system and hypothalamic-pituitary-adrenal (HPA) axis are the two major systems that respond to stress.[4] "
        self.topic_inferencer.infer_topic(answer)
        self.assertTrue('jaw' in answer.topic.topic_keys)
        self.assertTrue('food' in answer.topic.topic_keys)
        self.assertTrue('pain' in answer.topic.topic_keys)