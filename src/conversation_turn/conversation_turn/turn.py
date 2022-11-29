# -*- coding: utf-8 -*-

# question.py

"""
Bachelor-Thesis: Conversational agent for querying orofacial pain patients

Salome Wildermuth
Matrikel-Nr: 10-289-544
University of Zurich
Institute for Computational Linguistics

- Data class for conversation turn
- Important: this class is nearly untested, as the effort for writing integration tests for the
 process_answer_and_create_follow_up_question method is far too big compared to what it helps.
"""
import random

from conversation.conversation import Conversation, Language
from conversation_turn.conversation_element import Answer, Question, QuestionType, PredefinedQuestion

class ConversationTurn:
    def __init__(self, turn_number:int, conversation: Conversation, patient_input: str):
        self.turn_number = turn_number
        self.patient_input = patient_input
        self.generated_question: str = None
        self.answer: Answer = None
        self.question: Question or PredefinedQuestion = None
        self.topic_number: int = None
        self.more_detail: bool = None
        self.conversation = conversation
        self.preprocessor = conversation.preprocessor
        self.nlp = conversation.nlp
        # the question generation object requires access to the question intro repository
        self.conversation.question_generator.update_question_intro_repository(
            self.conversation.data_loader.question_intro_repo)

    def process_answer_and_profile_question(self, question: str):
        """
        Here the questions are predefined, so the sentiment analysis and question generation steps can be skipped,
        also the question must not be stored in the question repository, it was already loaded when the application
        started.
        """
        self.__create_answer_object()
        self.__store_answer()
        self.generated_question = question
        self.__write_turn_to_archive()

    def process_answer_and_create_follow_up_question(self):
        if self.conversation.language is Language.GERMAN:
            self.__translate_patient_input_from_german_to_english()
        self.__create_answer_object()
        self.__store_answer()
        self.__predict_mental_state()
        self.__infer_topics()
        self.__generate_question()
        self.__create_question_object()
        self.__store_question()
        if self.more_detail:
            self.__set_more_detail_question()
        self.__update_question_generation_object_with_newest_data()
        self.__write_turn_to_archive()
        # if we have detected a highly correlating topic, we use a predefined question for that topic and don't need to
        # translate, but just assign the german text of the question to the generated_question variable.
        if self.conversation.language is Language.GERMAN:
            if self.topic_number or self.more_detail:
                self.generated_question = self.question.content_in_german
            else:
                self.__translate_question_from_english_to_german()


    def __create_answer_object(self):
        self.answer = Answer(self.patient_input, 1, self.turn_number)
        # as soon as we have created the answer object, we have to update the QuestionGenerator object with it
        self.conversation.question_generator.set_answer(self.answer)
        self.conversation.preprocessor.preprocess(self.answer, self.conversation.preprocessing_parameters)


    def __store_answer(self):
        """
        Stores an object of type Answer in the corresponding repository.
        """
        self.conversation\
            .data_loader\
            .store_conversation_element('answer_repo', self.answer)

    def __create_question_object(self):
        # The topic questions are available objects of type PredefinedQuestion, no Question object has to be created.
        if self.topic_number:
            pass
        else:
            self.question = Question(self.generated_question, 1, QuestionType.GENERATED)

    def __store_question(self):
        """
        Stores an object of type Question in the corresponding repository.
        """
        if self.topic_number:
            # The topic questions are available in the topic question repository. No need for storing them again.
            pass
        else:
            self.conversation.preprocessor.preprocess(self.question, self.conversation.preprocessing_parameters)
            self.question.content_preprocessed += self.question.content[0]
            try:
                self.conversation\
                    .data_loader\
                    .store_conversation_element('question_repo', self.question)
            except ValueError:
                # we can't ask the generated question again, it was already asked
                self.more_detail = True


    def __translate_patient_input_from_german_to_english(self):
        self.patient_input = self.conversation.translator_de_en.translate(self.patient_input)

    def __translate_question_from_english_to_german(self):
        self.generated_question = self.conversation.translator_en_de.translate(self.generated_question)

    def __predict_mental_state(self):
        mental_state = self.conversation.sentiment_detector.predict_mental_state(self.patient_input)
        self.mental_state = mental_state
        self.answer.mental_state = mental_state

    def __infer_topics(self):
        self.conversation.topic_inferencer.infer_topic(self.answer.content_preprocessed)
        self.answer.topic_list = self.conversation.topic_inferencer.get_best_topics(3)
        #print(self.answer.topic_list)
        topic_question_repo = self.conversation.data_loader.mandatory_question_repo.questions
        for topic in self.answer.topic_list:
            # when this condition is false all the questions associated to one of the three topics have already been covered
            if topic.probability > 5 and \
                    topic_question_repo[topic.topic_number][0].number_of_usage == 0:
                self.topic_number = topic.topic_number
                break
        if self.topic_number: # at some point we won't find an unused topic question
            topic_question_repo[self.topic_number][0].number_of_usage += 1
            self.question = self.conversation.data_loader.mandatory_question_repo.questions[self.topic_number][0]
            # we sort the mandatory questions so that the ones that have not been used come first. This allows us to
            # simply check the first question if it has been used so far and if yes, we can pick it, and if not we know,
            # that there is no more question to pick for this topic.
            topic_question_repo[self.topic_number].sort(key=lambda x: x.number_of_usage, reverse=False)
            self.generated_question = self.question.content

    def __generate_question(self):
        if self.topic_number:
            # we use a mandatory question
            pass
        elif self.turn_number % 3 == 0:
            self.generated_question = self.conversation.question_generator.generate()
        else:
            # for variety we enforce one of our preferred interrogative pronouns, in some turns
            self.generated_question = self.conversation.question_generator.generate_with_highlight()

    def __german_to_english(self, text):
        self.conversation.translator_de_en.translate(text)

    def __english_to_german(self, text):
        self.conversation.translator_en_de.translate(text)

    def __write_turn_to_archive(self):
        archive_record = {'answer': self.patient_input, 'question': self.generated_question}
        self.conversation.conversation_archive.write(archive_record)

    def __update_question_generation_object_with_newest_data(self):
        # only generated questions are stored in this repository, the mandatory questions that derive from a topic are
        # maintained in the mandatory_question_repository
        if not self.topic_number and not self.more_detail:
            self.conversation.question_generator.update_generated_questions_repository(
                self.conversation.data_loader.generated_question_repo)
            self.conversation.question_generator.update_question_intro_repository(
                self.conversation.data_loader.question_intro_repo)

    def __set_more_detail_question(self):
        random_question_key = random.choice(list(self.conversation.data_loader.more_detail_question_repo.questions.keys()))
        self.question = self.conversation.data_loader.more_detail_question_repo.questions[random_question_key]
        self.generated_question = self.question.content