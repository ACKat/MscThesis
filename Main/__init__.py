from otree.api import *
import numpy as np
import time 


doc = """
Create the two-stage investment task
"""


class C(BaseConstants):
    NAME_IN_URL = 'InvestTask_NA'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1

    # Parameters
    initial_endowment = 10 
    initial_inv_cost = [12,8]
    prob_success= [0.75, 0.25]
    revenue_gained = 8
    additional_revenue_if_success = 8
    additional_cost = 4


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    Prolific_ID       = models.StringField()

    # Project selection decision
    project           = models.StringField(
        choices= ['Project A', 'Project B'],
        widget= widgets.RadioSelectHorizontal,
        label= 'You have been endowed with $10. Please select a project to invest in: '  
    )

    # Decision on whether to continue the investment
    additional_invest = models.BooleanField(
        widget= widgets.RadioSelectHorizontal,
        choices=[
            [True, 'Yes'],
            [False, 'No']
            ],
        label= 'Do you want to pay the additional investment cost to finalize the project?'
            )

    start_1          = models.IntegerField(blank=True)
    end_1            = models.IntegerField(blank=True)
    start_2          = models.IntegerField(blank=True)
    end_2            = models.IntegerField(blank=True)
    RT1              = models.IntegerField(blank=True)
    RT2              = models.IntegerField(blank=True)

    # Attributes of the treatment to be saved for each player
    sunk_cost        = models.IntegerField(blank=True)
    prob_chosen      = models.FloatField(blank=True)
    prob_unchosen    = models.FloatField(blank=True)

# FUNCTIONS

# Create project details by randomly selecting a cost and probability of success
def investment(sc, p): 
    investment = np.ones((2,))    # create a vector of ones 
    rand_num = np.random.randn(2) # create two random numbers from the [0,1) interval
    if rand_num[0] > 0.5:         # if the first random number exceeds 0.5 the cost will be 8 and 12 otherwise
        investment[0] = sc[0]
    else:
        investment[0] = sc[1]
    if rand_num[1] > 0.5:         # if the second random number exceeds 0.5 the probability will be 0.25 and 0.75 otherwise
        investment[1] = p[0]
    else:
        investment[1] = p[1]
    return investment

def project_creation(player):
    inv_A = investment(C.initial_inv_cost, C.prob_success)
    inv_B = investment(C.initial_inv_cost, C.prob_success)
    if  player.project == 'Project A':
        player.sunk_cost     = inv_A[0]
        player.prob_chosen   = inv_A[1]
        player.prob_unchosen = inv_B[1]
    elif player.project == 'Project B':
        player.sunk_cost     = inv_B[0]
        player.prob_chosen   = inv_B[1]
        player.prob_unchosen = inv_A[1]


# Calculate the payoff depending on participant's choice on whether to carry on with the project and 
# the outcome of the chosen lottery
def calculate_payoff(player):
    if player.additional_invest:
        rand_num = np.random.randn()
        if rand_num <= player.prob_chosen:
            player.payoff = C.initial_endowment - player.sunk_cost + C.revenue_gained - C.additional_cost + C.additional_revenue_if_success
        else:
            player.payoff = C.initial_endowment - player.sunk_cost + C.revenue_gained - C.additional_cost
    else:
           player.payoff = C.initial_endowment - player.sunk_cost + C.revenue_gained       
    return player.payoff   

# Save at the participant level
def custom_export(players):
    # header row
    yield ['session', 'additional_invest', 'sunk_cost', 'prob_chosen', 'prob_unchosen', 'RT1', 'RT2', 'payoff']
    for p in players:
        participant = p.participant
        session = p.session
        yield [session.code, participant.additional_invest, participant.sunk_cost, participant.prob_chosen, participant.prob_unchosen, participant.RT1, participant.RT2, participant.payoff]

# PAGES
class Project_selection(Page):
    form_model  = 'player'
    form_fields = ['project']

    # Reaction times
    def vars_for_template(player):
        player.start_1   = int(time.time())
        return dict( 
            start_1 = player.start_1 
        )

    # Create information for each project and allocate it to the right variables based on player's choice
    @staticmethod
    def before_next_page(player, timeout_happened):
        project_creation(player)

        player.end_1 = int(time.time())
        player.RT1   = player.end_1 - player.start_1
        return dict(
            end_1 = player.end_1,
            RT1   = player.RT1
        )
  
        
class Project_continuation(Page):
    form_model  = 'player'
    form_fields = ['additional_invest']

    @staticmethod
    def vars_for_template(player):
        player.start_2            = int(time.time())
        return dict(
            sunk_cost             = player.sunk_cost,
            prob_success_chosen   = player.prob_chosen,
            prob_success_unchosen = player.prob_unchosen,
            current_balance       = C.initial_endowment - player.sunk_cost + C.revenue_gained,
            start_2               = player.start_2
        )

    @staticmethod
    def before_next_page(player, timeout_happened):
        player.end_2 = int(time.time())
        player.RT2   = player.end_2 - player.start_2
        return dict(
            end_2 = player.end_2,
            RT2   = player.RT2
        )
  

class Results(Page):
    @staticmethod
    def vars_for_template(player):
        payoff = calculate_payoff(player)
        return dict(
            payoff = payoff
        )

    
page_sequence = [Project_selection, Project_continuation, Results]
