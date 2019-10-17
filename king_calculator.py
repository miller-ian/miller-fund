import math
import json
from datetime import datetime
import sys

def create_triangle_num_list(numGamesPlayed):
    denom = 0
    recencyList = []
    for i in range(numGamesPlayed + 1):
        denom += i
    for i in range(1, numGamesPlayed+1):
        recencyList.append(i/denom)
    return recencyList

def trailing_weighted_average(S, W):
    total = 0
    for i in range(len(S)):
        total += S[i] * W[i]
    return total

def calculate_moving_team_record(toDateWins):
    listOfRecord = []
    nthGame = 0
    for i in range(0, len(toDateWins)):
        nthGame += 1
        listOfRecord.append(int(toDateWins[i])/nthGame)
    return trailing_weighted_average(listOfRecord, create_triangle_num_list(len(toDateWins)))

def calculate_moving_awaygame_record(awayRecord):
    awayGames = len(awayRecord)
    listOfRecord = []
    nthGame = 0
    for i in range(0, awayGames):
        nthGame += 1        
        listOfRecord.append(awayRecord[i]/(nthGame))
    return trailing_weighted_average(listOfRecord, create_triangle_num_list(awayGames))

def calculate_moving_homegame_record(homeRecord):
    homeGames = len(homeRecord)
    listOfRecord = []
    nthGame = 0
    for i in range(0, homeGames):
        nthGame += 1
        listOfRecord.append(homeRecord[i]/nthGame)
    return trailing_weighted_average(listOfRecord, create_triangle_num_list(homeGames))

def calculate_pythagorean_expectation(pointsFor, pointsAgainst):
    """
    Final value will be a weighted average of pythagorean expectation over the season and
    the last 3 games.

    season- 70%
    last3 - 30%
    """
    power = .8
    expectation = (pow(pointsFor, power))/(pow(pointsFor, power) + pow(pointsAgainst, power))
    return expectation


def normalize(p1, p2):
    regular = True
    greater = 0
    smaller = 0
    if p1 > p2:
        greater = p1
        smaller = p2
        regular = True
    else:
        greater = p2
        smaller = p1
        regular = False
    greaterScaled = (greater**2)/smaller
    smallerScaled = (smaller**2)/greater
    scaledTotal = greaterScaled + smallerScaled
    prob1 = greaterScaled/scaledTotal
    prob2 = smallerScaled/scaledTotal
    if regular:
        return (prob1, prob2)
    else:
        return (prob2, prob1)

def convert_to_moneyline(confidence):
    if confidence > 50:
        differential = confidence/(100-(confidence))
        return differential * (-100)
    else:
        differential = (100-(confidence))/confidence
        return differential*100

def kelly_compute(winProb, odds, bankroll):
    winProb *= (1/100)
    odds = float(odds)
    if odds > 0:
        b = (odds / 100.0) + 1

    else:
        b = (100.0 / -odds) + 1
    b -= 1
    q = 1-winProb
    edge = (b*winProb-q) / b
    return edge*bankroll

def get_model_lines_plus_kelly(homeTeam, homePointsFor, homePointsAgainst, homeTeamRecord, homeTeamHomeRecord, homeLine, awayTeam, awayPointsFor, awayPointsAgainst, awayTeamRecord, awayTeamAwayRecord, awayLine, bankroll):
    weights = [70, 15, 15] #pythagorean, record, home/away record
    
    homeConfidence = (weights[0] * calculate_pythagorean_expectation(homePointsFor, homePointsAgainst)) + (weights[1] * calculate_moving_team_record(homeTeamRecord)) + (weights[2] * calculate_moving_homegame_record(homeTeamHomeRecord))

    awayConfidence = (weights[0] * calculate_pythagorean_expectation(awayPointsFor, awayPointsAgainst)) + (weights[1] * calculate_moving_team_record(awayTeamRecord)) + (weights[2] * calculate_moving_awaygame_record(awayTeamAwayRecord))

    normalizedHome = (normalize(homeConfidence, awayConfidence)[0]*100) 
    normalizedAway = (normalize(homeConfidence, awayConfidence)[1]*100)
    try:
        awayWager = kelly_compute(normalizedAway, awayLine, bankroll)
        homeWager = kelly_compute(normalizedHome, homeLine, bankroll)
        if awayWager > 0:
            return (awayTeam, awayWager, awayLine, normalizedAway, homeTeam)
        else:
            return (homeTeam, homeWager, homeLine, normalizedHome, awayTeam)
    except:
        today = datetime.today()
        d1 = datetime.strptime("10-22-2019", '%m-%d-%Y')
        delta = (d1 - today).days
        
        return ("No listings for this game yet! The NBA season starts in " + str(delta) + " days")
