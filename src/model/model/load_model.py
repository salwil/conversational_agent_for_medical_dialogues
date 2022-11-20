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
import src.helpers.helpers.helpers as helpers
from model.model.topic import TopicInferencer


class Model(Enum):
    TRANSLATION_DE_EN = 'translation-de-en' #replace with real mallet_topics name / path to mallet_topics?
    TRANSLATION_EN_DE = 'translation-en-de' # replace with real mallet_topics name / path to mallet_topics?
    QUESTION_GENERATION = 'p208p2002/bart-squad-qg-hl' # https://huggingface.co/p208p2002/bart-squad-qg-hl
    SENTIMENT_DETECTION = 'facebook/bart-large-mnli' # https://huggingface.co/facebook/bart-large-mnli
    TOPIC = 'mallet.mallet_topics.10'


class ModelLoader:
    def __init__(self):
        self.path = helpers.get_project_path() + '/src/repository/data/'

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

class TopicModelLoader(ModelLoader):
    def load_model(self, model_checkpoint: Model):
        path_to_mallet = self.path + 'topic/'
        print("Loading " + model_checkpoint.value + "...")
        return TopicInferencer(path_to_mallet, model_checkpoint.value)




