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

from conversation_turn.conversation_turn.conversation_element import Answer
from preprocess.preprocess.preprocess import Preprocessor
from rules.rules.interrogative_pronouns import InterrogativePronoun, Position

class QuestionGenerationRules:
    def __init__(self, preprocessor: Preprocessor, nlp, answer: Answer = None):
        self.interrogative_pronouns = InterrogativePronoun()
        self.found_named_entities = None
        # class variable only for test purposes
        self.allowed_pronouns = None
        self.answer = answer
        self.preprocessor = preprocessor
        self.nlp = nlp
        self.generated_questions_repository = None
        self.question_intro_repository = None

    def generate_highlight(self) -> str:
        pronoun = self.__select_interrogative_pronoun_for_next_question()
        trigger = self.interrogative_pronouns.interrogative_pronouns_with_trigger[pronoun]
        if trigger[1] is Position.BOS:
            self.answer.content_with_hl = '[HL] ' + trigger[0] + ' [HL] ' + self.answer.content_in_2nd_pers
        else:
            self.answer.content_with_hl = self.answer.content_in_2nd_pers + ' [HL] ' + trigger[0] + ' [HL].'

    def create_2nd_person_sentence_from_1st_person(self) -> None:
        doc = self.nlp(self.answer.content)
        self.preprocessor.preprocess(self.answer, ['tokenize'])
        index = 0
        # we need the entry are: are for the first person plural: if someone writes
        forms = {'am': 'are', 'i': 'you', 'mine': 'yours', 'me': 'you', 'my': 'your', "'m": "'re", "ours": "yours", "our": "your", "we": "you", "us": "you"}  # More?
        for token in doc:
            if len(token.morph.get("PronType")) > 0 and token.morph.get("Person") == ['1'] or \
                    len(token.morph.get("VerbForm")) > 0 and token.morph.get("Mood") == ['Ind']:
                pronoun = self.answer.content_tokenized[index].lower()
                try:
                    self.answer.content_tokenized[index] = forms[pronoun]
                except KeyError:
                    # verbs except 'be' can remain as is, and also the plural form of be (we are --> you are)
                    pass
            index += 1
        self.answer.content_in_2nd_pers = " ".join(self.answer.content_tokenized)

    def select_question_intro(self):
        try:
            matching_intros = self.question_intro_repository.mental_states[self.answer.mental_state]
            self.question_intro = matching_intros[0]
            matching_intros[0].number_of_usage += 1
            # sort list of intros ascending by their usage --> we can just always pick the first one, which has been the
            # one not used for the longest time.
            matching_intros.sort(key=lambda x: x.number_of_usage, reverse=False)
        except KeyError:
            self.question_intro = None

    def __determine_sentence_ne(self, text: str) -> None:
        doc = self.nlp(text)
        named_entity_types = self.interrogative_pronouns.ne_type_for_interrogative_pronouns
        found_entities = []
        for label in doc.ents:
            if label.label_ in named_entity_types:
                found_entities.append(label.label_)
        if len(found_entities) > 0:
            self.found_named_entities = found_entities

    def __select_interrogative_pronoun_for_next_question(self) -> str:
        self.__determine_sentence_ne(self.answer.content)
        if self.found_named_entities is None:
            # all pronouns allowed
            self.allowed_pronouns = [p for p in self.interrogative_pronouns.interrogative_pronouns_with_trigger.keys()]
        else:
            not_allowed_pronouns = [self.interrogative_pronouns.ne_type_for_interrogative_pronouns[ne]
                                    for ne in self.interrogative_pronouns.ne_type_for_interrogative_pronouns
                                    if ne in self.found_named_entities]
            not_allowed_pronouns_flat = [item for sublist in not_allowed_pronouns for item in sublist]
            self.allowed_pronouns = [p for p in self.interrogative_pronouns.interrogative_pronouns_with_trigger.keys()
                                     if p not in not_allowed_pronouns_flat]
        return random.choice(self.allowed_pronouns)

