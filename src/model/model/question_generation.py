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

class QuestionGenerator:
    def __init__(self):
        self.tokenizer = AutoTokenizer.from_pretrained('p208p2002/bart-squad-qg-hl')
        self.model = AutoModelForSeq2SeqLM.from_pretrained('p208p2002/bart-squad-qg-hl')

    def generate(self, text):
        input_ids = self.tokenizer.encode(text)
        question_ids = self.model.generate(torch.tensor([input_ids]))
        decode = self.tokenizer.decode(question_ids.squeeze().tolist(), skip_special_tokens=True)
        #print(decode)
        return decode
