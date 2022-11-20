# -*- coding: utf-8 -*-

# topic.py

"""
Bachelor-Thesis: Conversational agent for querying orofacial pain patients

Salome Wildermuth
Matrikel-Nr: 10-289-544
University of Zurich
Institute for Computational Linguistics

- Class for topic inference

"""
#import little_mallet_wrapper as lmw
import os
import re
import numpy as np

from conversation_turn.conversation_turn.conversation_element import Answer

class TopicInferencer:
    def __init__(self, path_to_model, model_checkpoint):
        #self.path_to_model = path_to_model
        self.path_to_mallet = 'mallet-2.0.8/bin/mallet'
        #self.model_checkpoint = model_checkpoint
        self.number_of_topics = 10
        self.topic_distributions = self.__load_topic_distributions('model/mallet.topic_distributions.10')
        #self.topic_distributions_for_answer = None
        #self.topic_keys_for_answer = None
        #self.topic_keys = self.load_topic_keys('model/mallet.topic_keys.10')

    def infer_topic(self, answer: Answer):
        text = [answer.content_preprocessed]
        #text = answer.content.split('.')
        #self.print_dataset_stats(text)
        self.__prepare_input_file(text)
        #self.__create_topic_model_for_answer(text, 1)
        self.__infer_topics(self.path_to_mallet,
                         'model/mallet.model.10',
                         'model_new/training',
                         'model_new/mallet.topic_distributions')
        #topic = self.__get_topic_with_highest_probability(text)
        #print(topic)
        #answer.topic = topic

    def __create_topic_model_for_answer(self, text, number_of_topics):
        self.__train_topic_model(self.path_to_mallet,
                                 'model_new/training',
                                 'model_new/mallet.model.' + str(number_of_topics),
                                 'model_new/mallet.topic_keys.' + str(number_of_topics),
                                 'model_new/mallet.topic_distributions.' + str(number_of_topics),
                                 'model_new/mallet.word_weights.' + str(number_of_topics),
                                 'model_new/mallet.diagnostics.xml' + str(number_of_topics),
                                 number_of_topics)

    def __prepare_input_file(self, text):
        training_data_file = open('model_new/training.txt', 'w')
        for i, d in enumerate(text):
            training_data_file.write(str(i) + ' no_label ' + d + '\n')
        training_data_file.close()

        os.system(self.path_to_mallet + ' import-file --input "' + 'model_new/training.txt' + '"'
                                             + ' --output "' + 'model_new/training' + '"' \
                                             + ' --keep-sequence'
                                             + ' --preserve-case')
    """
    def __get_topic_with_highest_probability(self):
        sorted_data = sorted([(_distribution[topic_index], _document)
                              for _distribution, _document
                              in zip(topic_distributions, training_data)], reverse=True)
        return sorted_data[:n]
    

    def __train_topic_model(self, path_to_mallet,
                            path_to_formatted_training_data,
                            path_to_model,
                            path_to_topic_keys,
                            path_to_topic_distributions,
                            path_to_word_weights,
                            path_to_diagnostics,
                            num_topics):

        os.system(path_to_mallet + ' train-topics --input "' + path_to_formatted_training_data + '"' \
                  + ' --num-topics ' + str(num_topics) \
                  + ' --inferencer-filename "' + path_to_model + '"' \
                  + ' --output-topic-keys "' + path_to_topic_keys + '"' \
                  + ' --output-doc-topics "' + path_to_topic_distributions + '"' \
                  + ' --topic-word-weights-file "' + path_to_word_weights + '"' \
                  + ' --diagnostics-file "' + path_to_diagnostics + '"' \
                  + ' --optimize-interval 10')

    def __load_topic_keys(self, topic_keys_path):
        return [line.split('\t')[2].split() for line in open(topic_keys_path, 'r')]
    """

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
