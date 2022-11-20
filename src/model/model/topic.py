# -*- coding: utf-8 -*-

# topic.py

"""
Bachelor-Thesis: Conversational agent for querying orofacial pain patients

Salome Wildermuth
Matrikel-Nr: 10-289-544
University of Zurich
Institute for Computational Linguistics

- Class for topic inference
- Some functions that encapsulate Mallet calls have been inspired by the maria-antioniak's little-mallet-wrapper:
  https://github.com/maria-antoniak/little-mallet-wrapper, namely:
    * __load_topic_keys
    * __load_topic_distributions
    * __prepare_input_file
    * __infer_topics

"""
import os

from conversation_turn.conversation_turn.conversation_element import Answer
from conversation_turn.conversation_turn.topic import Topic


class TopicInferencer:
    def __init__(self, path_to_mallet, path_to_pretrained_mallet_model, path_to_new_model):
        self.path_to_mallet = path_to_mallet
        self.path_to_original_model = path_to_pretrained_mallet_model
        self.path_to_new_model = path_to_new_model
        self.number_of_topics = 1
        self.answer: Answer = None
        self.topic_keys = self.__load_topic_keys(self.path_to_original_model + 'mallet.topic_keys.10')
        self.topic_distributions = None

    def infer_topic(self, answer: Answer):
        self.answer = answer
        text = [self.answer.content_preprocessed]
        self.__prepare_input_data(text)
        self.__infer_topics(self.path_to_mallet,
                            self.path_to_original_model + 'mallet.model.10',
                            self.path_to_new_model + 'training',
                            self.path_to_new_model + 'mallet.topic_distributions.' + str(self.number_of_topics))
        self.topic_distributions = self.__load_topic_distributions(self.path_to_new_model +
                                                                   'mallet.topic_distributions.' +
                                                                   str(self.number_of_topics))
        best_topic, probability = self.get_best_topic()
        self.answer.topic = Topic(best_topic, probability)

    def __load_topic_keys(self, topic_keys_path):
        return [line.split('\t')[2].split() for line in open(topic_keys_path, 'r')]

    def __prepare_input_data(self, text):
        training_data_file = open(self.path_to_new_model + 'training.txt', 'w')
        for i, d in enumerate(text):
            training_data_file.write(str(i) + ' no_label ' + d + '\n')
        training_data_file.close()

        os.system(self.path_to_mallet + ' import-file --input "' + self.path_to_new_model + 'training.txt' + '"'
                                             + ' --output "' + self.path_to_new_model + 'training' + '"' \
                                             + ' --keep-sequence'
                                             + ' --preserve-case')

    def __load_topic_distributions(self, topic_distributions_path):
        topic_distributions = []
        for line in open(topic_distributions_path, 'r'):
            if line.split()[0] != '#doc':
                instance_id, distribution = (line.split('\t')[1], line.split('\t')[2:])
                distribution = [float(p) for p in distribution]
                topic_distributions.append(distribution)
        return topic_distributions

    def __infer_topics(self, path_to_mallet,
                       path_to_original_model,
                       path_to_new_formatted_training_data,
                       path_to_new_topic_distributions):
        # num-iterations tbd
        os.system(path_to_mallet + ' infer-topics --input "' + path_to_new_formatted_training_data + '"' \
                  + ' --num-iterations 10' \
                  + ' --inferencer "' + path_to_original_model + '"' \
                  + ' --output-doc-topics "' + path_to_new_topic_distributions + '"')

    def __get_n_most_relevant_keywords(self, number):
        for i, t in enumerate(self.topic_keys):
            print(i, '\t', ' '.join(t[:number]))

    def get_best_topic(self):
        if not self.topic_distributions:
            self.topic_distributions = self.__load_topic_distributions(self.path_to_new_model + 'mallet.topic_distributions.1')
        max_index = self.topic_distributions[0].index(max(self.topic_distributions[0]))
        return self.topic_keys[max_index], max(self.topic_distributions[0])
