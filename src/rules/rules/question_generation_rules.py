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

from rules.rules.interrogative_pronouns import InterrogativePronoun

class QuestionGenerationRules:
    def __init__(self):
        self.last_answer = None
        self.interrogative_pronouns = InterrogativePronoun()
        self.found_named_entities = None
        # class variable only for test purposes
        self.allowed_pronouns = None
        # inject this!! currently loaded twice (once in preprocessor and again here)
        self.nlp = en_core_web_sm.load()

    def generate_highlight(self, last_answer) -> str:
        pronoun = self.__select_interrogative_pronoun_for_next_question(last_answer)
        return self.interrogative_pronouns.interrogative_pronouns_with_trigger[pronoun]

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
