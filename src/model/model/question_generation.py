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

from conversation_turn.conversation_element import Answer
from preprocess.preprocess import Preprocessor
from rules.question_generation_rules import QuestionGenerationRules

class QuestionGenerator:
    def __init__(self, preprocessor: Preprocessor, nlp, answer: Answer = None):
        self.tokenizer = AutoTokenizer.from_pretrained('p208p2002/bart-squad-qg-hl')
        self.model = AutoModelForSeq2SeqLM.from_pretrained('p208p2002/bart-squad-qg-hl')
        self.answer = answer
        self.rules = QuestionGenerationRules(preprocessor, nlp, answer)
        self.generated_questions_repository = None
        self.question_intro_repository = None
        self.patient_salutation = None

    def generate(self):
        self.rules.create_2nd_person_sentence_from_1st_person()
        self.rules.select_question_intro(self.patient_salutation)
        input_ids = self.tokenizer.encode(self.answer.content_in_2nd_pers)
        question_ids = self.model.generate(torch.tensor([input_ids]))
        decode = self.tokenizer.decode(question_ids.squeeze().tolist(), skip_special_tokens=True)
        if self.rules.question_intro:
            question = self.rules.question_intro.content + ' ' + decode
        else:
            question = decode
        return question

    def generate_with_highlight(self):
        self.rules.create_2nd_person_sentence_from_1st_person()
        self.rules.generate_highlight()
        self.rules.select_question_intro(self.patient_salutation)
        input_ids = self.tokenizer.encode(self.answer.content_with_hl)
        question_ids = self.model.generate(torch.tensor([input_ids]))
        decode = self.tokenizer.decode(question_ids.squeeze().tolist(), skip_special_tokens=True)
        if self.rules.question_intro:
            question = self.rules.question_intro.content + ' ' + decode
        else:
            question = decode
        return question

    def set_answer(self, answer):
        # meanwhile the QuestionGeneration object is instantiated once during the conversation lifecycle, this object
        # as well as the QuestionGenerationRules object have to be updated, for every conversation turn with the new
        # answer
        self.answer = answer
        self.rules.answer = answer

    def update_generated_questions_repository(self, generated_question_repository: {}):
        # meanwhile the QuestionGeneration object is instantiated once during the conversation lifecycle, the repo
        # has to be replaced by the updated repository for every conversation turn in this object as well as in the
        # QuestionGenerationRules object.
        self.generated_questions_repository = generated_question_repository
        self.rules.generated_questions_repository = generated_question_repository

    def update_question_intro_repository(self, question_intro_repository: {}):
        # meanwhile the QuestionGeneration object is instantiated once during the conversation lifecycle, the repo
        # has to be replaced by the updated repository for every conversation turn in this object as well as in the
        # QuestionGenerationRules object.
        self.question_intro_repository = question_intro_repository
        self.rules.question_intro_repository = question_intro_repository

    def set_patient_salutation(self, salutation: str):
        self.patient_salutation = salutation

