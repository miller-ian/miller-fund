import csv
import backtester_helper as helper
import requests
from lxml import html
from datetime import datetime
from decimal import Decimal
import matplotlib.pyplot as plt
import numpy as np

def run_main(weights, start):
    years = helper.read_years()
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
            
            if count > start:
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
    print(ev)
    return ev

def draw_best_fit_line(x, y):
    coef = np.polyfit(x, y, 1)
    poly1d_fn = np.poly1d(coef)
    plt.plot(x, y, 'yo', x, poly1d_fn(x), '--k')

if __name__ == '__main__':
    #weightsFirst = [47, 44, 8.8, 0.2]     # WEIGHTS FOR DAY 40 - 60
    #weightsSecond = [40, 33, 25, 2]          # WEIGHTS FOR DAY 61 - 90
    #weightsThird = [32, 32, 32, 4]                   # WEIGHTS FOR DAY 91 - 110
    #weightsFourth = [34, 27, 37, 2]          #WEIGHTS FOR DAY 111 - 140    
    #weightsFifth = [43.5, 26, 28, 2.5]           #WEIGHTS FOR DAY 141 - 160
    weightsSixth = [22, 50, 25, 3]         #WEIGHTS FOR DAY 161 - 195
    # weightsSeventh = [20, 35, 37.5, 7.5]    #WEIGHTS FOR DAY 180 - 200
    
    weightsIncumbent = [50, 40, 9.5, 0.5]
    weightsPE = [100, 0, 0, 0]
    weights2 = [0, 100, 0, 0]
    weights3 = [0.1, 0, 100, 0]
    weights4 = [0, 0, 0, 100]
   
    # fig, axes = plt.subplots(3)
    # axes[0].set_title('pythagorean expectation')
    # axes[1].set_title('record heavy')
    # axes[2].set_title('working weights')
    
    total = 0
    lastTotal = 0
    x = []
    y = []
    for i in range(161, 196):
        localTotalIncumbent = run_main(weightsIncumbent, i)

        localTotalProposed = run_main(weightsSixth, i)
        # localTotalPE = run_main(weightsPE, i)
        # localTotal2 = run_main(weights2, i)
        # localTotal3 = run_main(weights3, i)
        # localTotal4 = run_main(weights4, i)
        
        # if i <= 60:
        #     localTotalProposed = run_main(weightsFirst, i)
        # elif i <= 100:
        #     localTotalProposed = run_main(weightsSecond, i)
        # elif i <= 120:
        #     localTotalProposed = run_main(weightsThird, i)
        # elif i <= 135:
        #     localTotalProposed = run_main(weightsFourth, i)
        # elif i <= 155:
        #     localTotalProposed = run_main(weightsFifth, i)
        # elif i <= 180:
        #     localTotalProposed = run_main(weightsSixth, i)
        # else:
        #     localTotalProposed = run_main(weightsSeventh, i)
        

        plt.plot(i, localTotalIncumbent, 'ro')
        plt.plot(i, localTotalProposed, 'go')
        # plt.plot(i, localTotalPE, 'bo')
        # plt.plot(i, localTotal2, 'mo')
        # plt.plot(i, localTotal3, 'ko')
        # plt.plot(i, localTotal4, 'yo')
        # x.append(i)
        # y.append(localTotalProposed)
        lastTotal += localTotalIncumbent
        total += localTotalProposed
        #total += localTotalReal
        #otherTotal += localTotalProposed


    #draw_best_fit_line(x, y)
    print("*****************************")
    print("time-variant average edge: ", total/35)
    #print("non time-variant weights: ", otherTotal/160)
    print("incumbent avg edge: ", lastTotal/35)

    plt.show()