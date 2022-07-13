from otree.api import *


doc = """
Your app description
"""


class C(BaseConstants):
    NAME_IN_URL = 'Early_exit'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1
    Early_exit_link = "https://app.prolific.co/submissions/complete?cc=9414AA2A"


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    pass


# PAGES

class Early_exit(Page):
    pass

page_sequence = [Early_exit]
