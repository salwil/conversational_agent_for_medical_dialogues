# -*- coding: utf-8 -*-

# qusetion_generation.py

"""
Bachelor-Thesis: Conversational agent for querying orofacial pain patients

Salome Wildermuth
Matrikel-Nr: 10-289-544
University of Zurich
Institute for Computational Linguistics

- Class for question generation

"""

from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import torch

from conversation_turn.conversation_turn.conversation_element import Answer
from preprocess.preprocess.preprocess import Preprocessor
from rules.rules.interrogative_pronouns import Position
from rules.rules.question_generation_rules import QuestionGenerationRules


class QuestionGenerator:
    def __init__(self, preprocessor: Preprocessor, nlp, answer: Answer = None):
        self.tokenizer = AutoTokenizer.from_pretrained('p208p2002/bart-squad-qg-hl')
        self.model = AutoModelForSeq2SeqLM.from_pretrained('p208p2002/bart-squad-qg-hl')
        self.answer = answer
        self.rules = QuestionGenerationRules(nlp, preprocessor, answer)

    def generate(self):
        self.rules.create_2nd_person_sentence_from_1st_person()
        input_ids = self.tokenizer.encode(self.answer.content_in_2nd_pers)
        question_ids = self.model.generate(torch.tensor([input_ids]))
        decode = self.tokenizer.decode(question_ids.squeeze().tolist(), skip_special_tokens=True)
        return decode

    def generate_with_highlight(self):
        self.rules.create_2nd_person_sentence_from_1st_person()
        self.rules.generate_highlight()
        input_ids = self.tokenizer.encode(self.answer.content_with_hl)
        question_ids = self.model.generate(torch.tensor([input_ids]))
        decode = self.tokenizer.decode(question_ids.squeeze().tolist(), skip_special_tokens=True)
        return decode

    def set_answer(self, answer):
        # meanwhile the QuestionGeneration object is instantiated once during the conversation lifecycle, this object
        # as well as the QuestionGenerationRules object have to be updated, for every conversation turn with the new
        # answer
        self.answer = answer
        self.rules.answer = answer

"""
    def __generate_highlight(self):
        trigger = self.rules.generate_highlight()
        if trigger[1] is Position.BOS:
            self.answer.content_with_hl = self.answer.content_in_2nd_pers + '[HL] ' + trigger[0] + ' [HL]'
        else:
            self.answer.content_with_hl = '[HL] ' + trigger[0] + ' [HL]' + self.answer.content_in_2nd_pers

    def __replace_pronouns_first_person(self):
        self.rules.replace_pronouns()
        """

