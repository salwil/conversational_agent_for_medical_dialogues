# -*- coding: utf-8 -*-

# main.py

"""
Bachelor-Thesis: Conversational agent for querying orofacial pain patients

Salome Wildermuth
Matrikel-Nr: 10-289-544
University of Zurich
Institute for Computational Linguistics

- main module for maintaining conversation with user

"""
import time
import warnings

with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    from .termination_criterion import TerminationCriterionForConversation
    from conversation_turn.turn import ConversationTurn
    from .conversation import Conversation, Language

    """
    from src.conversation.conversation.termination_criterion import TerminationCriterionForConversation
    from src.conversation_turn.conversation_turn.turn import ConversationTurn
    from src.conversation.conversation.conversation import Conversation, Language
    """


def main():
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        conversation = Conversation()
        cli = CLI(conversation)
        cli.say_hello()
        language = cli.select_language()
        conversation.language = language
        cli.introduce_user(language)
        conversation.load_repositories()
        # this could be done in a separate thread, meanwhile the conversation is started with profile questions.
        conversation.load_models()
        cli.maintain_conversation(conversation)
        cli.say_goodbye(language)


class CLI:
    def __init__(self, conversation: Conversation):
        self.conversation = conversation
        self.termination_criterion = TerminationCriterionForConversation()
        self.current_conversation_turn: ConversationTurn = None

    def maintain_conversation(self, conversation):
        turn_number = 1
        if conversation.language is Language.GERMAN:
            print("Starten wir mit ein paar allgemeinen Fragen.")
        else:
            print("Let's start with some general information about you.")
        answer = 'Start'
        for profile_question in conversation.data_loader.profile_question_repo.questions.values():
            if not self.termination_criterion.given():
                self.current_conversation_turn = ConversationTurn(turn_number, conversation, answer)
                if conversation.language is Language.GERMAN:
                    print(profile_question.content_in_german)
                else:
                    print(profile_question.content)
                self.current_conversation_turn.process_answer_and_profile_question(profile_question.content)
                answer = input()
                answer = self.__validate(answer)
                turn_number += 1
        if not self.termination_criterion.given():
            if conversation.language is Language.GERMAN:
                next_question = 'Wie möchten Sie gerne angesprochen werden?'
            else:
                next_question = 'How would you like to be addressed?'
            print(next_question)
            salutation = input()
            salutation = self.__validate(salutation)
            self.conversation.set_patient_salutation(salutation)
            turn_number += 1
        if not self.termination_criterion.given():
            if conversation.language is Language.GERMAN:
                next_question = 'Würden Sie mir kurz erklären, warum Sie hier sind?'
            else:
                next_question = 'Would you introduce me briefly, why you seek consultation?'
            print(next_question)
            answer = input()
            answer = self.__validate(answer)
        while not self.termination_criterion.given():
            self.current_conversation_turn = ConversationTurn(turn_number, conversation, answer)
            self.current_conversation_turn.process_answer_and_create_follow_up_question()
            next_question = self.current_conversation_turn.generated_question
            print(next_question)
            answer = input()
            answer = self.__validate(answer)
            turn_number += 1

    def say_hello(self):
        local_time = time.localtime()
        if local_time.tm_hour < 7:
            print('Guten Morgen, Sie Frühaufsteher.')
            print('Good morning, early bird.')
        elif local_time.tm_hour < 10:
            print('Guten Morgen.')
            print('Good morning.')
        elif local_time.tm_hour < 13:
            print('Guten Tag.')
            print('Good day.')
        elif local_time.tm_hour < 17:
            print('Guten Tag.')
            print('Good afternoon.')
        elif local_time.tm_hour < 23:
            print('Guten Abend.')
            print('Good evening.')
        else:
            print('Hello. ')
        input()

    def select_language(self):
        print("Wenn Sie deutsch bevorzugen, geben Sie bitte 'D' ein.")
        print("If you prefer an English conversation, please enter 'E'")
        language = input()
        while language.upper() != 'D' and language.upper() != 'E':
            print('Bitte geben Sie an, in welcher Sprache Sie die Unterhaltung führen wollen, bevor wir loslegen.')
            print('Before we start, please indicate, which language you prefer for the conversation.')
            print("Deutsch: D, English: E")
            language = input()
        if language.upper() == Language.GERMAN.value:
            return Language.GERMAN
        else:
            return Language.ENGLISH

    def introduce_user(self, language):
        if language is Language.GERMAN:
            print('Bitte warten Sie einen Moment, das System startet...')
            print('Inzwischen gebe ich Ihnen einige Vorinformationen:')
            print("Wenn immer Sie die Unterhaltung verlassen wollen, geben Sie bitte 'q!' oder 'quit!' ein.")
        else:
            print('Please wait a moment, the system is starting...')
            print('In the meantime I give you some introductions:')
            print("Whenever you want to stop and quit the conversation, enter 'q!' or 'quit!'")

    def say_goodbye(self, language):
        if language is Language.GERMAN:
            print('Vielen Dank für das Gespräch.')
            print('Die Ärztin wird sich bald bei Ihnen melden.')
            print('Bis da hin wünsche ich Ihnen gute Besserung.')
        else:
            print('Thank you for the conversation.')
            print('The doctor will get back to you soon')
            print('Until then, get well soon.')

    def __validate(self, user_input):
        while not user_input:
            user_input = input()
        self.termination_criterion.check_user_terminate(user_input)
        self.termination_criterion.update(current_turn=self.current_conversation_turn)
        return user_input


if __name__ == "__main__":
    main()
