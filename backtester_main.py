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
def get_weights(count):
    weightsFirst = [47, 44, 8.8, 0.2]     # WEIGHTS FOR DAY 40 - 60
    weightsSecond = [40, 33, 25, 2]          # WEIGHTS FOR DAY 61 - 90
    weightsThird = [32, 32, 32, 4]                   # WEIGHTS FOR DAY 91 - 110
    weightsFourth = [34, 27, 37, 2]          #WEIGHTS FOR DAY 111 - 140    
    weightsFifth = [43.5, 26, 28, 2.5]           #WEIGHTS FOR DAY 141 - 160
    weightsSixth = [22, 50, 25, 3]         #WEIGHTS FOR DAY 161 - 195
    
    weightsIncumbent = [50, 40, 9.5, 0.5]

    if count < 61:
        return weightsFirst
    elif count < 91:
        return weightsSecond
    elif count < 111:
        return weightsThird
    elif count < 141:
        return weightsFourth
    elif count < 161:
        return weightsFifth
    elif count < 196:
        return weightsSixth
    else:
        return weightsIncumbent

if __name__ == '__main__':
    years = helper.read_years()
    weights = [50, 40, 9.5, 0.5]    #adding days rest in current weight scheme goes from 100.13835 to 100.19563
    
    totalWins = 0
    totalLosses = 0
    totalGrowth = 0
    totalNumWagers = 0
    totalEdge = 0
    for year in years:
        DOGWINS = 0
        DOGLOSSES = 0
        FAVWINS = 0
        FAVLOSSES = 0
        leagueState = helper.instantiateTeams()
        schedule_dict = helper.create_schedule_dict(helper.read_data(year))
        datesWithGames = helper.create_daily_slate(set(schedule_dict.keys()))
        wageredMoney = 0
        count = 0
        numWagers = 0
        additiveEdge = 0
        resettableBankroll = 100
        for date in datesWithGames:
            if count >= 195:
                break
            slate = schedule_dict[date]
            
            if count > 75:
                weights = get_weights(count)
                slateWinnings = 0
                slateCost = 0
                for g in slate:
                    resettableBankroll = 100
                    resettableWager = helper.placeBet(leagueState, g, resettableBankroll, weights)
                    payout = resettableWager[0]
                    
                    risk = resettableWager[1]
                    if risk == 0:
                        continue
                    if payout > 0:
                        if resettableWager[5] > 0:
                            DOGWINS += 1
                        else:
                            FAVWINS += 1
                    else:
                        if resettableWager[5] > 0:
                            DOGLOSSES += 1
                        else:
                            FAVLOSSES += 1
                    numWagers += 1
                    resettableBankroll += risk
                    resettableBankroll += payout
                    additiveEdge += resettableBankroll                
            leagueState = helper.timestep(leagueState, slate)
            count += 1
     
        totalLosses += DOGLOSSES + FAVLOSSES
        totalWins += DOGWINS + FAVWINS

        totalNumWagers += numWagers
        totalEdge += additiveEdge
        print(totalEdge/totalNumWagers)

    ev = (totalEdge / totalNumWagers)
    print(" ")
    print("******************")
    print(ev)
    print("Total Losses: ", totalLosses)
    print("Total Wins: ", totalWins)
    print("Win percentage: ", totalWins/(totalWins+totalLosses))
    print("Dog win percentage: ", DOGWINS/(DOGWINS + DOGLOSSES))
    print("Fav win percentage: ", FAVWINS/(FAVWINS + FAVLOSSES))
    print("Fav wager percentage: ", (FAVWINS + FAVLOSSES)/(DOGWINS + DOGLOSSES))
