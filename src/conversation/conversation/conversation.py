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
from src.model.model.translation import TranslatorDeEn, TranslatorEnDe
from src.model.model.sentiment_detection import SentimentDetector
from src.model.model.question_generation import QuestionGenerator
from src.repository.repository.load_data_into_repo import DataLoader, Repository
from src.repository.repository.conversation_archive import ConversationArchival
from .patient import Patient
from src.preprocess.preprocess.lemmatize import EnglishLemmatizer
from src.preprocess.preprocess.preprocess import Preprocessor


class Conversation:
    def __init__(self):
        self.english_lemmatizer = EnglishLemmatizer()
        # preprocessing parameters are maintained centrally, to ensure the same are used for both questions and answers
        self.preprocessing_parameters = ['lemmatize', 'tokenize', 'remove_punctuation', 'remove_stopwords']
        self.preprocessor = Preprocessor(lemmatizer=self.english_lemmatizer)
        # lemmatizer is needed when loading questions (original and preprocessed format) from file into repository
        self.data_loader = DataLoader(self.preprocessing_parameters, self.preprocessor)
        self.translator_de_en: TranslatorDeEn = None
        self.translator_en_de: TranslatorEnDe = None
        self.sentiment_detector: SentimentDetector = None
        self.question_generator: QuestionGenerator = None
        self.patient = Patient()
        self.conversation_archive = ConversationArchival(self.patient.creation_timestamp_formatted)

    def load_repositories(self):
        self.data_loader.load_data_into_repository(Repository.QUESTIONS)
        self.data_loader.load_data_into_repository(Repository.TOPICS)
        self.data_loader.load_data_into_repository(Repository.MENTALSTATES)

    def load_models(self):
        self.translator_de_en = TranslatorDeEn()
        self.translator_en_de = TranslatorEnDe()
        self.sentiment_detector = SentimentDetector([mental_state
                                                     for mental_state in self.data_loader.mental_state_repo])
        self.question_generator = QuestionGenerator()

    def ask_questions_for_patient_instantiation(self):
        for question in self.data_loader.profile_question_repo.questions:
            answer = print(question.content_in_german)
