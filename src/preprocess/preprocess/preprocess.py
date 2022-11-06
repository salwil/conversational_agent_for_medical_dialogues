# -*- coding: utf-8 -*-

# preprocess.py

"""
Bachelor-Thesis: Conversational agent for querying orofacial pain patients

Salome Wildermuth
Matrikel-Nr: 10-289-544
University of Zurich
Institute for Computational Linguistics

- Knowledge Discovery on base of medical surveys in the context of orofacial pain.
- Module contains the class Preprocessor
- Preprocessor preprocesses on a very basic level the data, that is available in format of a list.
  Possible preprocessor step are:
    - Tokenization
    - Removal of punctuation and CR/LF
    - Removal of stopwords
    - Lemmatization

"""

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, RegexpTokenizer
from src.conversation_turn.conversation_turn.conversation_element import ConversationElement

class Preprocessor:
    def __init__(self, lemmatizer):
        self.data_record = None
        # if tokenization is required, the values of every column (small texts) are tokenized,
        # meaning word, punctuation separation

        #Preprocessing Steps
        self.tokenized = False
        self.remove_punctuation = False
        self.remove_stopwords = False
        self.lemmatized = False

        #Preprocessor is instantiated once, the following instances / methods only need to be created / called once
        self.regexp_tokenizer = RegexpTokenizer(r'\w+')
        # elif number_of_features is parameters.NumberOfFeatures.MAIN
        self.lemmatizer = lemmatizer
        self.stop_words = set(stopwords.words('english'))

    def preprocess(self, data_record: ConversationElement, preprocessing_arguments: list) -> None:
        self.data_record = data_record

        if 'lemmatize' in preprocessing_arguments:
            self.lemmatize()
            self.lemmatized = True
        if 'remove_punctuation' in preprocessing_arguments:
            self.removePunctuation()
            self.remove_punctuation = True
        if 'remove_stopwords' in preprocessing_arguments:
            self.removeStopwords()
            self.remove_stopwords = True
        if 'tokenize' in preprocessing_arguments:
            self.tokenize()
            self.tokenized = True

    def lemmatize(self):
        data_record_lemmatized=self.lemmatizer.lemmatize(self.data_record.content)
        self.data_record.content_preprocessed = data_record_lemmatized

    def tokenize(self):
        self.data_record.content_tokenized = word_tokenize(self.data_record.content_preprocessed)

    # Note: if we apply this method, values of date / time attributes will be hardly readable
    # CR/LF are also removed with this method
    def removePunctuation(self):
        self.data_record.content_preprocessed = ' '.join(self.regexp_tokenizer.tokenize(self.data_record.content_preprocessed))

    def removeStopwords(self):
        # Tokenization is precondition for stopwords removal
        self.tokenize()
        self.data_record.content_preprocessed = ' '.join(w for w in self.data_record.content_tokenized if not w.lower() in self.stop_words)

    def getTokenizedRecord(self):
        if self.tokenized:
            return self.data_record.content_tokenized()
        else:
            raise RuntimeWarning('Tokenization was not required')

    def getPreprocessedRecord(self):
        return self.data_record.content_preprocessed()
