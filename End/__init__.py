from otree.api import *


doc = """
Goodbye page
"""


class C(BaseConstants):
    NAME_IN_URL = 'EndPage'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    pass


# PAGES

class EndPage(Page):
    pass


page_sequence = [EndPage]

