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
    def __init__(self, preprocessor: Preprocessor, nlp):
        self.tokenizer = AutoTokenizer.from_pretrained('p208p2002/bart-squad-qg-hl')
        self.model = AutoModelForSeq2SeqLM.from_pretrained('p208p2002/bart-squad-qg-hl')
        self.rules = QuestionGenerationRules(preprocessor, nlp)

    def generate(self, answer: Answer):
        answer_with_replaced_pronouns = self.__replace_pronouns_first_person(answer)
        answer_with_hl = self.__generate_highlight(answer_with_replaced_pronouns)
        input_ids = self.tokenizer.encode(answer_with_hl)
        question_ids = self.model.generate(torch.tensor([input_ids]))
        decode = self.tokenizer.decode(question_ids.squeeze().tolist(), skip_special_tokens=True)
        return decode

    # this method has to remain public because it is mocked in question_generator_test
    def __generate_highlight(self, text: str):
        trigger = self.rules.generate_highlight(text)
        if trigger[1] is Position.BOS:
            return  text + '[HL] ' + trigger[0] + ' [HL]'
        else:
            return '[HL] ' + trigger[0] + ' [HL]' + text

    def __replace_pronouns_first_person(self, answer: Answer):
        return self.rules.replace_pronouns(answer)

