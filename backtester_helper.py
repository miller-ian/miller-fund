import csv
import backtester_calculator as kc
import requests
from lxml import html
from datetime import datetime
from decimal import Decimal
from datetime import date


class Team:
    def __init__(self, name, games, record, homeWins, awayWins, pointsFor, pointsAgainst, daysRest=0):
        self.name = name
        self.games = games
        self.record = record
        self.homeWins = homeWins
        self.awayWins = awayWins
        self.pointsFor = pointsFor
        self.pointsAgainst = pointsAgainst
        self.daysRest = daysRest


class Game:
    def __init__(self, date, home_team_city, away_team_city, home_points, away_points, home_moneyLine, away_moneyLine, year):
        self.date = date
        self.home_team_city = home_team_city
        self.away_team_city = away_team_city
        self.home_points = home_points
        self.away_points = away_points
        self.home_moneyLine = home_moneyLine
        self.away_moneyLine = away_moneyLine
        self.year = year

def get_teams():
    return{
        'GSW' : 'GoldenState',
        'MIL' : 'Milwaukee',
        'PHI' : 'Philadelphia',
        'NOP' : 'NewOrleans',
        'OKC' : 'OklahomaCity',
        'TOR' : 'Toronto',
        'LAC' : 'LAClippers',
        'WAS' : 'Washington',
        'SAC' : 'Sacramento',
        'POR' : 'Portland',
        'HOU' : 'Houston',
        'BOS' : 'Boston',
        'SAS' : 'SanAntonio',
        'BRK' : 'Brooklyn',
        'LAL' : 'LALakers',
        'DEN' : 'Denver',
        'MIN' : 'Minnesota',
        'CHO' : 'Charlotte',
        'ATL' : 'Atlanta',
        'UTA' : 'Utah',
        'DAL' : 'Dallas',
        'IND' : 'Indiana',
        'DET' : 'Detroit',
        'PHO' : 'Phoenix',
        'ORL' : 'Orlando',
        'NYK' : 'NewYork',
        'MIA' : 'Miami',
        'CHI' : 'Chicago',
        'CLE' : 'Cleveland',
        'MEM' : 'Memphis',
        'NJY' : 'NewJersey',
        'SEA' : 'Seattle'
    }

def instantiateTeams():
    leagueState = {}
    teamsDict = get_teams()
    teams = teamsDict.values()
    for team in teams:
        leagueState[team] = Team(team, [], [], [], [], 0, 0)
    return leagueState

def read_years():
    years = ["0708",
            "0809",
            "0910",
            "1011",
            "1112",
            "1213",
            "1314",
            "1415",
            "1516",
            "1617",
            "1718",
            "1819"]
    
    return years

def read_data(year):
    listOfGames = []
    with open('C:/Users/imaxm/Desktop/mitSophomore/sportsBetting/miller-fund/historical_odds/' + year + '.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=",")
        line_count = 1
        for row in csv_reader:
            if line_count == 1:
                line_count += 1
            else:

                if line_count % 2 == 0:
                    away_team_city = row[3]
                    away_moneyLine = row[11]
                    away_points = row[8]
                    line_count += 1
                else:
                    home_team_city = row[3]
                    home_moneyLine = row[11]
                    home_points = row[8]
                    line_count += 1
                    newGame = Game(row[0], home_team_city, away_team_city, home_points, away_points, home_moneyLine, away_moneyLine, year)
                    listOfGames.append(newGame)
        return listOfGames

def create_schedule_dict(data):
    returnDict = {}
    for game in data:
        date = game.date
        if date in returnDict.keys():
            listOfGames = returnDict[date]
            listOfGames.append(game)
            returnDict[date] = listOfGames
        else:
            returnDict[date] = [game]
    return returnDict

def create_daily_slate(all_dates_with_games):
    prev = []
    after = []
    for date in all_dates_with_games:
        if int(date) > 1000:
            prev.append(date)
        else:
            after.append(date)

    datesWithGames = sorted(prev) + sorted(after)
    return datesWithGames

def calculate_days_rest(lastDate, today, year):
    
    homeLastGameDay = lastDate[-2] + lastDate[-1]
    if len(lastDate) > 3:
        homeLastGameMonth = lastDate[:2]
        lastYear = "20" + year[:2]
    else:
        homeLastGameMonth = lastDate[:1]
        lastYear = "20" + year[2:]
    
    d1 = date(int(lastYear), int(homeLastGameMonth), int(homeLastGameDay))
    

    homeToday = today[-2] + today[-1]
    if len(today) > 3:
        homeTodayMonth = today[:2]
        todayYear = "20" + year[:2]
    else:
        homeTodayMonth = today[:1]
        todayYear = "20" + year[2:]
    
    d2 = date(int(todayYear), int(homeTodayMonth), int(homeToday))

    delta = d2 - d1
    return delta.days



def timestep(leagueState, slate):
    
    for game in slate:
        today = game.date

        homeTeam = game.home_team_city
        homePoints = game.home_points
        homeTeamDaysRest = 0

        awayTeam = game.away_team_city
        awayPoints = game.away_points
        awayTeamDaysRest = 0

        homeWin = 1
        awayWin = 0

        if int(awayPoints) > int(homePoints):
            awayWin = 1
            homeWin = 0
        homeTeamObject = leagueState[homeTeam]
        homeGames = homeTeamObject.games
        if len(homeGames) > 0:
            homeTeamDaysRest = calculate_days_rest(homeGames[-1].date, today, game.year)
        homePointsFor = homeTeamObject.pointsFor
        homePointsAgainst = homeTeamObject.pointsAgainst
        homeWinsAway = homeTeamObject.awayWins  #will remain constant
        homeTeamRecord = homeTeamObject.record
        homeWins = homeTeamObject.homeWins

        homeTeamRecord.append(homeWin)
        homeGames.append(game)
        updatedHomePointsFor = homePointsFor + int(homePoints)
        updatedHomePointsAgainst = homePointsAgainst + int(awayPoints)
        if len(homeWins) > 0:
            updatedHomeWinTotal = homeWins[-1] + homeWin
            homeWins.append(updatedHomeWinTotal)
        else:
            if homeWin == 0:
                homeWins = [0]
            else:
                homeWins = [1]

        updatedHomeTeam = Team(homeTeam, homeGames, homeTeamRecord, homeWins, homeWinsAway, updatedHomePointsFor, updatedHomePointsAgainst, homeTeamDaysRest)        
        awayTeamObject = leagueState[awayTeam]
        awayGames = awayTeamObject.games

        if len(awayGames) > 0:
            awayTeamDaysRest = calculate_days_rest(awayGames[-1].date, today, game.year)
        awayPointsFor = awayTeamObject.pointsFor
        awayPointsAgainst = awayTeamObject.pointsAgainst
        awayWinsHome = awayTeamObject.homeWins  #will remain constant
        awayTeamRecord = awayTeamObject.record
        awayWins = awayTeamObject.awayWins

        awayTeamRecord.append(awayWin)
        awayGames.append(game)
        updatedAwayPointsFor = awayPointsFor + int(awayPoints)
        updatedAwayPointsAgainst = awayPointsAgainst + int(homePoints)
        if len(awayWins) > 0:
            updatedAwayWinTotal = awayWins[-1] + awayWin
            awayWins.append(updatedAwayWinTotal)
        else:
            
            if awayWin == 0:

                awayWins = [0]
            else:
                awayWins = [1]

        updatedAwayTeam = Team(awayTeam, awayGames, awayTeamRecord, awayWinsHome, awayWins, updatedAwayPointsFor, updatedAwayPointsAgainst, awayTeamDaysRest)
        leagueState[awayTeam] = updatedAwayTeam
        leagueState[homeTeam] = updatedHomeTeam   
    return leagueState

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
    
    betString = "Betting $" + str(betAmount) + " on " + str(betTeam) + " at " + str(betLine) + " to beat " + str(bet[4]) + "..."
    # print(betString)
    
    if int(game.home_points) > int(game.away_points):
        if betTeam == homeTeam:
            return [possibleWinnings, -betAmount, 1, 0, possibleProfit, betLine]
        else:
            return [0, -betAmount, 0, 1, 0, betLine]
    else:
        if betTeam == awayTeam:
            return [possibleWinnings, -betAmount, 1, 0, possibleProfit, betLine]
        else:
            return [0, -betAmount, 0, 1, 0, betLine]

def placeBet(leagueState, game, bankroll, weights):
    if game.home_moneyLine == "NL" or game.home_moneyLine == "NL":
        return [0, 0, 0, 0, 0]
    homeTeam = game.home_team_city
    awayTeam = game.away_team_city
    homePointsFor = leagueState[homeTeam].pointsFor
    homePointsAgainst = leagueState[homeTeam].pointsAgainst
    homeTeamRecord = leagueState[homeTeam].record
    homeTeamHomeRecord = leagueState[homeTeam].homeWins
    homeTeamDaysRest = leagueState[homeTeam].daysRest
    homeLine = int(game.home_moneyLine)
    awayPointsFor = leagueState[awayTeam].pointsFor
    awayPointsAgainst = leagueState[awayTeam].pointsAgainst
    awayTeamRecord = leagueState[awayTeam].record
    awayTeamAwayRecord = leagueState[awayTeam].awayWins
    awayTeamDaysRest = leagueState[awayTeam].daysRest
    awayLine = int(game.away_moneyLine)


    
    bet = (kc.get_model_lines_plus_kelly(weights,
                                        homeTeam,
                                        homePointsFor, 
                                        homePointsAgainst, 
                                        homeTeamRecord,
                                        homeTeamHomeRecord, 
                                        homeTeamDaysRest,
                                        homeLine, 
                                        awayTeam,
                                        awayPointsFor, 
                                        awayPointsAgainst, 
                                        awayTeamRecord,
                                        awayTeamAwayRecord, 
                                        awayTeamDaysRest,
                                        awayLine,
                                        bankroll))
    winnings = calculate_winnings(bet, game)
    return winnings