# -*- coding: utf-8 -*-

# conversation.py

"""
Bachelor-Thesis: Conversational agent for querying orofacial pain patients

Salome Wildermuth
Matrikel-Nr: 10-289-544
University of Zurich
Institute for Computational Linguistics

- Class for maintaining conversation with patient

"""
import sys
import traceback
import datetime
from enum import Enum

import en_core_web_sm

from model.model.topic_inference import TopicInferencer
from src.model.model.translation import TranslatorDeEn, TranslatorEnDe
from src.model.model.sentiment_detection import SentimentDetector
from src.model.model.question_generation import QuestionGenerator
from src.repository.repository.load_data_into_repo import DataLoader, Repository
from src.repository.repository.conversation_archive import ConversationArchival
from src.preprocess.preprocess.lemmatize import EnglishLemmatizer
from src.preprocess.preprocess.preprocess import Preprocessor

class Language(Enum):
    ENGLISH = 'E',
    GERMAN = 'D'

class Conversation:
    def __init__(self, test_mode = False):
        self.language: Language = Language.ENGLISH
        self.preprocessing_parameters = ['lemmatize', 'tokenize', 'remove_punctuation', 'remove_stopwords']
        try:
            self.nlp = en_core_web_sm.load()
        except(IOError):
            traceback.print_exc()
            sys.exit("Have you downloaded en_core_web_sm to your environment?")
        self.english_lemmatizer = EnglishLemmatizer(self.nlp)
        self.preprocessor = Preprocessor(lemmatizer=self.english_lemmatizer, nlp=self.nlp)
        # lemmatizer is needed when loading questions (original and preprocessed format) from file into repository
        self.data_loader = DataLoader(self.preprocessing_parameters, self.preprocessor)
        self.translator_de_en: TranslatorDeEn = None
        self.translator_en_de: TranslatorEnDe = None
        self.sentiment_detector: SentimentDetector = None
        self.question_generator: QuestionGenerator = None
        self.topic_inferencer: TopicInferencer = None
        self.creation_timestamp: datetime = datetime.datetime.now()
        self.creation_timestamp_formatted: str = self.creation_timestamp.strftime("%m-%d-%Y-%H-%M-%S")
        self.conversation_archive = ConversationArchival(self.creation_timestamp_formatted, test_mode)

    def load_repositories(self):
        self.data_loader.load_data_into_repository(Repository.QUESTIONS)
        self.data_loader.load_data_into_repository(Repository.TOPICS)
        self.data_loader.load_data_into_repository(Repository.INTRO)
        self.data_loader.load_data_into_repository(Repository.MOREDETAIL)

    def load_models(self):
        self.translator_de_en = TranslatorDeEn()
        self.translator_en_de = TranslatorEnDe()
        self.sentiment_detector = SentimentDetector([mental_state
                                                     for mental_state
                                                     in self.data_loader.question_intro_repo.mental_states])
        self.question_generator = QuestionGenerator(self.preprocessor, self.nlp, None)
        self.topic_inferencer = TopicInferencer(number_of_pretrained_topics=10)

    def ask_questions_for_patient_instantiation(self):
        for question in self.data_loader.profile_question_repo.questions:
            answer = print(question.content_in_german)
