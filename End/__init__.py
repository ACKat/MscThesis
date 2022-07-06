from otree.api import *
from pyparsing import ParseSyntaxException


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
    ParseSyntaxException


# PAGES

class EndPage(Page):
    pass


page_sequence = [EndPage]

