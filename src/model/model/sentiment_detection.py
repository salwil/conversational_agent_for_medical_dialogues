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

from transformers import AutoTokenizer, AutoModelForSequenceClassification

class SentimentDetector:
    def __init__(self):
        self.tokenizer = AutoTokenizer.from_pretrained('facebook/bart-large-mnli')
        self.model = AutoModelForSequenceClassification.from_pretrained('facebook/bart-large-mnli')

