import csv
import backtester_helper as helper
import requests
from lxml import html
from datetime import datetime
from decimal import Decimal

'''
-This file is set up to test on historical csv data in the historical_odds directory,
using the model as prescribed in king_calculator.py.

-This file outputs an average return on a bet of $100. For example, when this file is run, 
if the printed value is $99.50, each bet loses 0.5% on average.
'''

if __name__ == '__main__':
    years = helper.read_years()
    weights = [50, 40, 9.5, 0.5]
    totalWins = 0
    totalLosses = 0
    totalGrowth = 0
    totalNumWagers = 0
    totalEdge = 0
    for year in years:
        WINS = 0
        LOSSES = 0
        leagueState = helper.instantiateTeams()
        schedule_dict = helper.create_schedule_dict(helper.read_data(year))
        datesWithGames = helper.create_daily_slate(set(schedule_dict.keys()))
        wageredMoney = 0
        count = 0
        numWagers = 0
        additiveEdge = 0
        resettableBankroll = 100
        for date in datesWithGames:
            if count >= (len(datesWithGames) - 1):
                break
            slate = schedule_dict[date]
            
            if count > 42:
                slateWinnings = 0
                slateCost = 0
                for g in slate:
                    resettableBankroll = 100
                    resettableWager = helper.placeBet(leagueState, g, resettableBankroll, weights)
                    payout = resettableWager[0]
                    risk = resettableWager[1]
                    if risk == 0:
                        continue
                    numWagers += 1
                    resettableBankroll += risk
                    resettableBankroll += payout
                    additiveEdge += resettableBankroll                
            leagueState = helper.timestep(leagueState, slate)
            count += 1
     
        totalLosses += LOSSES
        totalWins += WINS
        totalNumWagers += numWagers
        totalEdge += additiveEdge

    ev = (totalEdge / totalNumWagers)
    print(" ")
    print("******************")
    print(ev)