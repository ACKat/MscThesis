from otree.api import *


doc = """
This app includes the introduction page, consent form and instructions of the experiment plus a checkup question.
"""


class C(BaseConstants):
    NAME_IN_URL = 'Instructions'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    consent        = models.BooleanField(
        choices= [
            [True, 'I agree'],
            [False, 'I do not agree']
        ],
        label = ' '
    )

    # Check up questions
    check_1 = models.BooleanField(
        choices=[
            [True, 'After selecting a project to invest in.'],
            [False, 'Before selecting a project to invest in.']
        ],
        label = 'You will receive information regarding your project options:'
    )

    timeout = models.BooleanField(blank=True)

# PAGES
class Introduction(Page):

    timeout_seconds = 300
   
    def before_next_page(player, timeout_happened):
        if timeout_happened:
            player.timeout = True
        else:
            player.timeout = False

    def app_after_this_page(player, upcoming_apps):
        if player.timeout:
            return 'Early_exit'

    
class Consent(Page):

    timeout_seconds = 120

    form_model = 'player'
    form_fields = ['consent']

    def before_next_page(player, timeout_happened):
        if timeout_happened:
            player.timeout = True
        else:
            player.timeout = False

    def app_after_this_page(player, upcoming_apps):
        if player.timeout or (player.consent!=True):
            return 'Early_exit'

class Instructions(Page):

    timeout_seconds = 300

    @staticmethod
    def is_displayed(player):
        return player.consent 

    @staticmethod
    def before_next_page(player, timeout_happened):
        if timeout_happened:
            player.timeout = True
        else:
            player.timeout = False

    @staticmethod
    def app_after_this_page(player, upcoming_apps):
        if player.timeout or (player.consent!=True):
            return 'Early_exit'
    

class Checks(Page):

    timeout_seconds = 120

    form_model  = 'player'
    form_fields = ['check_1']

    @staticmethod
    def is_displayed(player):
        return player.consent 

    @staticmethod
    def error_message(player, values):
        if values['check_1'] != True:
            return 'Wrong! Please answer correcly and press "Next" to proceed.'

    @staticmethod
    def before_next_page(player, timeout_happened):
        if timeout_happened:
            player.timeout = True
        else:
            player.timeout = False

    @staticmethod
    def app_after_this_page(player, upcoming_apps):
        if player.timeout or (player.consent!=True):
            return 'Early_exit'

page_sequence = [Introduction, Consent, Instructions, Checks ]
