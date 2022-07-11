from otree.api import *



doc = """
Justification and demographic questions
"""


class C(BaseConstants):
    NAME_IN_URL = 'Questionnaire'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1



class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    justification =  models.LongStringField(label='Please justify briefly your decision in the task you just completed:')
    
    age = models.StringField(
        choices=[
            '18-24 years old', 
            '25-34 years old',
            '35-44 years old',
            '45-54 years old',
            '55-64 years old',
            '65-74 years old',
            '75 years or older'
        ]
    )

    gender = models.StringField(label='What gender do you identify as?',
        choices=[
                'Female',
                'Male',
                'Other',
                'Prefer not to answer'
        ]
    )
    
    education_level = models.StringField(label= 'Please choose the level of completed education that best applies to your case:',
        choices=[
            'No schooling completed',
            'High school graduate',
            'Trade/technical/vocational training',
            'Bachelor degree',
            'Master degree',
            'Professional degree',
            'Doctorate degree'

        ]
    )
    
    education_field = models.StringField(label= 'What is/was your primary field of studies if any?')

    optimism = models.StringField(label= 'I have an optimistic view of life.',
        choices=[
            'Extremely',
            'Very',
            'Moderately',
            'Slightly',
            'Not at all' 
        ]
    )

    risk_taking = models.StringField(label= 'I consider myself a risk-taking person.',
        choices=[
            'Extremely',
            'Very',
            'Moderately',
            'Slightly',
            'Not at all' 
        ]
    )

    disappointment = models.StringField(label= 'I find it easy to overcome disappointment.',
        choices=[
            'Extremely',
            'Very',
            'Moderately',
            'Slightly',
            'Not at all' 
        ]
    )

    counterfactual = models.StringField(label= 'I tend to engage often in counterfactual thinking (thinking of what could have been).',
        choices=[
            'Extremely',
            'Very',
            'Moderately',
            'Slightly',
            'Not at all' 
        ]
    )


    self_blame = models.StringField(label= 'I engage in self-blame rather often, even in situations where I know I did the best I could given the situation.',
        choices=[
            'Extremely',
            'Very',
            'Moderately',
            'Slightly',
            'Not at all' 
        ]
    )


# PAGES
class Justification(Page):
    form_model  = 'player'
    form_fields = ['justification']


class Personality(Page):
    form_model  = 'player'
    form_fields = ['optimism', 'risk_taking', 'disappointment', 'counterfactual', 'self_blame']



class Demographics(Page):
    form_model = 'player'
    form_fields = ['age', 'gender', 'education_level', 'education_field']
    


page_sequence = [Justification, Personality, Demographics]
