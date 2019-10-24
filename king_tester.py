import csv
import king_calculator as kc
import king_tester_helper as helper
import requests
from lxml import html
from datetime import datetime
from decimal import Decimal

def calculate_winnings(bet, game):
    '''
    Return is a list of 5 elements:
    1- Actual return
    2- Amount of money wagered
    3- 1 for win, 0 for no win
    4- 1 for loss, 0 for no loss
    5- profit
    '''
    homeTeam = game.home_team_city
    awayTeam = game.away_team_city
    
    betTeam = bet[0]
    betAmount = float(bet[1])
    betLine = bet[2]
    if betAmount < 0:
        return [0, 0, 0, 0, 0]
    possibleWinningsDog = betAmount * betLine / 100.0
    possibleWinningsFav = betAmount / (-betLine/100.0)
    possibleWinnings = 0
    possibleProfit = 0
    if betLine > 0:
        possibleWinnings = possibleWinningsDog + betAmount
        possibleProfit = betLine / 100.0
    else:
        possibleWinnings = possibleWinningsFav + betAmount
        possibleProfit = possibleWinningsFav
    
    betString = "Betting $" + str(betAmount) + " on " + str(betTeam) + " to beat " + str(bet[4]) + "..."
    #print (betString)
    aBetString = str(betAmount) + " on " + str(betTeam) + " at " + str(betLine)
    # print(aBetString)
    # print(game.home_points, game.away_points, awayTeam)
    if int(game.home_points) > int(game.away_points):
        if betTeam == homeTeam:
            #print("Win1")
            return [possibleWinnings, -betAmount, 1, 0, possibleProfit]
        else:
            #print("Loss")
            return [0, -betAmount, 0, 1, 0, 0]
    else:
        if betTeam == awayTeam:
            #print("Win2")
            return [possibleWinnings, -betAmount, 1, 0, possibleProfit]
        else:
            #print("Loss")
            return [0, -betAmount, 0, 1, 0, 0]

def placeBet(leagueState, game, bankroll, weights):
    if game.home_moneyLine == "NL" or game.home_moneyLine == "NL":
        return [0, 0, 0, 0, 0]
    homeTeam = game.home_team_city
    awayTeam = game.away_team_city
    homePointsFor = leagueState[homeTeam].pointsFor
    homePointsAgainst = leagueState[homeTeam].pointsAgainst
    homeTeamRecord = leagueState[homeTeam].record
    homeTeamHomeRecord = leagueState[homeTeam].homeWins
    homeLine = int(game.home_moneyLine)
    awayPointsFor = leagueState[awayTeam].pointsFor
    awayPointsAgainst = leagueState[awayTeam].pointsAgainst
    awayTeamRecord = leagueState[awayTeam].record
    awayTeamAwayRecord = leagueState[awayTeam].awayWins
    awayLine = int(game.away_moneyLine)
    
    bet = (kc.get_model_lines_plus_kelly(weights,
                                        homeTeam,
                                        homePointsFor, 
                                        homePointsAgainst, 
                                        homeTeamRecord,
                                        homeTeamHomeRecord, 
                                        homeLine, 
                                        awayTeam,
                                        awayPointsFor, 
                                        awayPointsAgainst, 
                                        awayTeamRecord,
                                        awayTeamAwayRecord, 
                                        awayLine,
                                        bankroll))
    winnings = calculate_winnings(bet, game)
    return winnings

def the_main(weights):
    years = helper.read_years()
    #years = [1819]
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
            #if count >= 14:
                break
            slate = schedule_dict[date]
            
            if count > 12:
                slateWinnings = 0
                slateCost = 0
                for g in slate:
                    resettableBankroll = 100

                    # wager = placeBet(leagueState, g, bankroll)
                    # payout = wager[0]
                    # risk = wager[1]
                    # WINS += wager[2]
                    # LOSSES += wager[3]
                    # slateProfit = wager[4]
                    # if risk == 0:
                    #     continue
                    # slateWinnings += payout
                    # bankroll += risk
        
                    resettableWager = placeBet(leagueState, g, resettableBankroll, weights)
                    payout = resettableWager[0]
                    risk = resettableWager[1]
                    if risk == 0:
                        continue
                    numWagers += 1

                    resettableBankroll += risk
                    resettableBankroll += payout
                    #print(resettableBankroll)
                    additiveEdge += resettableBankroll

                    #reset bankroll to 100 everytime
                
                
            leagueState = helper.timestep(leagueState, slate)
            count += 1
     
        
        totalLosses += LOSSES
        totalWins += WINS
        totalNumWagers += numWagers
        
        
        totalEdge += additiveEdge

    # print("******************")
    # print("Total wins over", str(len(years)), "years:", totalWins)
    # print("Total losses over", str(len(years)), "years:", totalLosses)
    ev = (totalEdge / totalNumWagers)
    #print("Average expected growth over", str(len(years)), "years:", totalGrowth / len(years))
    #print("Average expected value over", str(len(years)), "years:", ev)
    return ev