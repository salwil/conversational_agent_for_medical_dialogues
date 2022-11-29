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

from transformers import pipeline

class SentimentDetector:
    def __init__(self, candidate_labels):
        self.candidate_labels = candidate_labels
        # we don't want to predict the neutral state, this is only a default state, if no other fits
        if 'neutral' in self.candidate_labels:
            self.candidate_labels.remove('neutral')
        self.classifier = pipeline("zero-shot-classification",
                              model="facebook/bart-large-mnli")

    def predict_mental_state(self, sentence) -> str:
        mental_states = self.classifier(sentence, self.candidate_labels)
        scores = mental_states['scores']
        mx = max(scores)
        scores_2nd = mental_states['scores']
        if len(scores) > 4 and mx > 3/len(scores) or len(scores) < 5 and mx > 0.8:
            scores_2nd.remove(mx)
            if mx-max(scores_2nd) > 1/(len(scores)*7):
                max_index = [index for index, item in enumerate(scores) if item == max(scores)]
                return mental_states['labels'][max_index[0]]
            else:
                return 'neutral'
        else:
            return 'neutral'
