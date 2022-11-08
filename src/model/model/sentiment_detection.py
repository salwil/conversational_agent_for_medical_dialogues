# -*- coding: utf-8 -*-

# sentiment_detection.py

"""
Bachelor-Thesis: Conversational agent for querying orofacial pain patients

Salome Wildermuth
Matrikel-Nr: 10-289-544
University of Zurich
Institute for Computational Linguistics

- Class for sentiment detection

"""

from transformers import AutoTokenizer, AutoModelForSequenceClassification, pipeline

class SentimentDetector:
    def __init__(self, candidate_labels):
        #self.tokenizer = AutoTokenizer.from_pretrained('facebook/bart-large-mnli')
        #self.model = AutoModelForSequenceClassification.from_pretrained('facebook/bart-large-mnli')
        self.candidate_labels = candidate_labels
        self.classifier = pipeline("zero-shot-classification",
                              model="facebook/bart-large-mnli")

    def determine_mental_state(self, sentence):
        mental_states = self.classifier(sentence, self.candidate_labels)
        scores = mental_states['scores']
        max_index = [index for index, item in enumerate(scores) if item == max(scores)]
        return mental_states['labels'][max_index[0]]

