from otree.api import *
from otree.api import models

doc = """
Your app description
"""


class C(BaseConstants):
    NAME_IN_URL = 'pubgoods'
    PLAYERS_PER_GROUP = 2
    NUM_ROUNDS = 5
    ENDOWMENT = 100
    MPCR_1 = 0.4
    MPCR_2 = 0.6


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    MPCR = models.FloatField(initial=.6)   # Declaring a variable on oTree (floating type); depending on the period will take the value of MPCR_1 or MPCR_2


class Player(BasePlayer):
    contribution = models.IntegerField(
        min=0,
        max=C.ENDOWMENT,  # we use the variable so we don't have to change the numbers every time
        label= "How much will you contribute?" # label is what is being displayed for the player
    ) # capturing the contributions from each player
#this does not accrue across periods

# PAGES
class MyPage(Page):
    form_model = 'player' # this is already built in otree, it adds the input
    form_fields = ['contribution']  # this is the variables that we want


class ResultsWaitPage(WaitPage):
    after_all_players_arrive = 'setPayoffs'
    body_text = 'You are too fast! Slow Down!'

class Results(Page):
    pass


page_sequence = [MyPage, ResultsWaitPage, Results]


# We need to add functions for the calculations

def creating_session(subsession): # this is a built-in otree function that loops subsessions (every round, etc)
    print("in creating session...") # add print statements to debug

    #establish a total earnings variable for each participant and initialize to 0 at beginning of session

    for p in subsession.get_players():
        if subsession.round_number == 1:
            p.participant.vars["totalEarnings"] = 0

    #Assign varying MPCR (first half of periods one value and second half the other)

    for g in subsession.get_groups():  # p for player and g for groups
        print('round ', subsession.round_number)
        print('num_rounds/2', C.NUM_ROUNDS / 2)
        if subsession.round_number <= C.NUM_ROUNDS / 2:  # in first half of the periods
            g.MPCR = C.MPCR_1
        else:
            g.MPCR = C.MPCR_2
        print('MPCR: ', g.MPCR)


def setPayoffs(g: Group): #loop to get the value of all submissions
    # calculate total group contribution
    total_contribution = 0

    for p in g.get_players(): # built otree function called get players
        total_contribution += p.contribution
        # total_contribution = total_contribution + p.contribution

    # calculate individual earnings

    for p in g.get_players():
        p.participant.payoff = C.ENDOWMENT - p.contribution + total_contribution * g.MPCR
        p.participant.vars['totalEarnings'] += p.participant.payoff

