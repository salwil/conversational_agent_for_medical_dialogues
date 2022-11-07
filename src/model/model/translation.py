# -*- coding: utf-8 -*-

# qusetion_generation.py

"""
Bachelor-Thesis: Conversational agent for querying orofacial pain patients

Salome Wildermuth
Matrikel-Nr: 10-289-544
University of Zurich
Institute for Computational Linguistics

- Classes for translation

"""

from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

class TranslatorDeEn:
    def __init__(self):
        self.tokenizer = AutoTokenizer.from_pretrained('translation-de-en') # replace with path to finetuned model
        self.model = AutoModelForSeq2SeqLM.from_pretrained('translation-de-en') # replace with path to finetuned model

class TranslatorEnDe:
    def __init__(self):
        self.tokenizer = AutoTokenizer.from_pretrained('translation-en-de') # replace with path to finetuned model
        self.model = AutoModelForSeq2SeqLM.from_pretrained('translation-en-de') # replace with path to finetuned model
