# -*- coding: utf-8 -*-

# qusetion_generation_rules.py

"""
Bachelor-Thesis: Conversational agent for querying orofacial pain patients

Salome Wildermuth
Matrikel-Nr: 10-289-544
University of Zurich
Institute for Computational Linguistics

- Class for all the rules that are involved into the rulebased part of question generation

"""
import random
from pprint import pprint
import en_core_web_sm

from conversation_turn.conversation_turn.conversation_element import Answer
from preprocess.preprocess.preprocess import Preprocessor
from rules.rules.interrogative_pronouns import InterrogativePronoun

class QuestionGenerationRules:
    def __init__(self, preprocessor: Preprocessor, nlp):
        self.interrogative_pronouns = InterrogativePronoun()
        self.found_named_entities = None
        # class variable only for test purposes
        self.allowed_pronouns = None
        self.preprocessor = preprocessor
        self.nlp = nlp

    def generate_highlight(self, last_answer) -> str:
        pronoun = self.__select_interrogative_pronoun_for_next_question(last_answer)
        return self.interrogative_pronouns.interrogative_pronouns_with_trigger[pronoun]

    def replace_pronouns(self, last_answer: Answer) -> Answer:
        doc = self.nlp(last_answer.content)
        self.preprocessor.preprocess(last_answer, ['tokenize'])
        index = 0
        forms = {'am': 'are', 'i': 'you', 'mine': 'yours', 'me': 'you', 'my': 'your', 'm': 're'}  # More?
        for token in doc:
            if len(token.morph.get("PronType")) > 0 and token.morph.get("Person") == ['1'] or \
                    len(token.morph.get("VerbForm")) > 0 and token.morph.get("Mood") == ['Ind']:
                pronoun = last_answer.content_tokenized[index].lower()
                last_answer.content_tokenized[index] = forms[pronoun]
            index += 1
        last_answer.content_in_2nd_pers = " ".join(last_answer.content_tokenized)
        return last_answer

    def __determine_sentence_ne(self, text):
        doc = self.nlp(text)
        named_entity_types = self.interrogative_pronouns.ne_type_for_interrogative_pronouns
        found_entities = []
        for label in doc.ents:
            if label.label_ in named_entity_types:
                found_entities.append(label.label_)
        if len(found_entities) > 0:
            self.found_named_entities = found_entities
        print(self.found_named_entities)

    def __select_interrogative_pronoun_for_next_question(self, last_answer: str) -> str:
        self.__determine_sentence_ne(last_answer)
        if self.found_named_entities is None:
            # all pronouns allowed
            self.allowed_pronouns = [p for p in self.interrogative_pronouns.interrogative_pronouns_with_trigger.keys()]
        else:
            not_allowed_pronouns = [self.interrogative_pronouns.ne_type_for_interrogative_pronouns[ne]
                                    for ne in self.interrogative_pronouns.ne_type_for_interrogative_pronouns
                                    if ne in self.found_named_entities]
            not_allowed_pronouns_flat = [item for sublist in not_allowed_pronouns for item in sublist]
            print(not_allowed_pronouns_flat)
            self.allowed_pronouns = [p for p in self.interrogative_pronouns.interrogative_pronouns_with_trigger.keys()
                                     if p not in not_allowed_pronouns_flat]
        print("Allowed pronouns: ")
        print(self.allowed_pronouns)
        return random.choice(self.allowed_pronouns)

