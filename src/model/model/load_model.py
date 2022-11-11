# -*- coding: utf-8 -*-

# load_data_into_repo.py

"""
Bachelor-Thesis: Conversational agent for querying orofacial pain patients

Salome Wildermuth
Matrikel-Nr: 10-289-544
University of Zurich
Institute for Computational Linguistics

- Class for loading language representation models

"""
from enum import Enum
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, AutoModelForSequenceClassification

class Model(Enum):
    TRANSLATION_DE_EN = 'translation-de-en' #replace with real model name / path to model?
    TRANSLATION_EN_DE = 'translation-en-de' # replace with real model name / path to model?
    QUESTION_GENERATION = 'p208p2002/bart-squad-qg-hl' # https://huggingface.co/p208p2002/bart-squad-qg-hl
    SENTIMENT_DETECTION = 'facebook/bart-large-mnli' # https://huggingface.co/facebook/bart-large-mnli


class ModelLoader:
    def __init__(self):
        pass

    def load_tokenizer(self, model_checkpoint: Model):
        return AutoTokenizer.from_pretrained(model_checkpoint.value)

class Seq2SeqModelLoader(ModelLoader):
    def load_model(self, model_checkpoint: Model):
        print("Loading " + model_checkpoint.value + "...")
        return AutoModelForSeq2SeqLM.from_pretrained(model_checkpoint.value)


class SequenceClassificationModelLoader(ModelLoader):
    def load_model(self, model_checkpoint: Model):
        print("Loading " + model_checkpoint.value + "...")
        return AutoModelForSequenceClassification.from_pretrained(model_checkpoint.value)



