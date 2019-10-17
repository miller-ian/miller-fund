import csv
#import kings_scrape as ks
import king_calculator as kc
import requests
from lxml import html
from datetime import datetime
from decimal import Decimal

class Team:
    def __init__(self, name, games, record, homeWins, awayWins, pointsFor, pointsAgainst):
        self.name = name
        self.games = games
        self.record = record
        self.homeWins = homeWins
        self.awayWins = awayWins
        self.pointsFor = pointsFor
        self.pointsAgainst = pointsAgainst

class Game:
    def __init__(self, date, home_team_city, away_team_city, home_points, away_points, home_moneyLine, away_moneyLine):
        self.date = date
        self.home_team_city = home_team_city
        self.away_team_city = away_team_city
        self.home_points = home_points
        self.away_points = away_points
        self.home_moneyLine = home_moneyLine
        self.away_moneyLine = away_moneyLine

def read_years():
    years = [708,
            809,
            910,
            1011,
            1112,
            1213,
            1314,
            1415,
            1516,
            1617,
            1718,
            1819]
    return years

def read_data(year):
    listOfGames = []
    with open('C:/Users/imaxm/Desktop/mitSophomore/sportsBetting/miller-fund/historical_odds/' + str(year) + '.csv') as csv_file:
    #with open('C:/Users/imaxm/Desktop/mitSophomore/sportsBetting/miller-fund/historical_odds/test.csv') as csv_file:

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
                    newGame = Game(row[0], home_team_city, away_team_city, home_points, away_points, home_moneyLine, away_moneyLine)
                    listOfGames.append(newGame)
        return listOfGames



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

def timestep(leagueState, slate):
    
    for game in slate:
        
        homeTeam = game.home_team_city
        homePoints = game.home_points

        awayTeam = game.away_team_city
        awayPoints = game.away_points
        
        homeWin = 1
        awayWin = 0

        if int(awayPoints) > int(homePoints):
            awayWin = 1
            homeWin = 0
        homeTeamObject = leagueState[homeTeam]
        homeGames = homeTeamObject.games
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

        updatedHomeTeam = Team(homeTeam, homeGames, homeTeamRecord, homeWins, homeWinsAway, updatedHomePointsFor, updatedHomePointsAgainst)
        
        
        awayTeamObject = leagueState[awayTeam]
        awayGames = awayTeamObject.games
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

        updatedAwayTeam = Team(awayTeam, awayGames, awayTeamRecord, awayWinsHome, awayWins, updatedAwayPointsFor, updatedAwayPointsAgainst)
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
    #print(bet)
    betTeam = bet[0]
    betAmount = bet[1]
    betLine = bet[2]
    if betAmount < 0:
        return [0, 0, 0, 0, 0]
    possibleWinningsDog = betAmount * betLine / 100.0
    possibleWinningsFav = betAmount / (-betLine/100.0)
    possibleWinnings = 0
    possibleProfit = 0
    if betLine > 0:
        possibleWinnings = possibleWinningsDog + betAmount
        possibleProfit = possibleWinningsDog
    else:
        possibleWinnings = possibleWinningsFav + betAmount
        possibleProfit = possibleWinningsFav
    
    betString = "Betting $" + str(betAmount) + " on " + str(betTeam) + " to beat " + str(bet[4]) + "..."
    print (betString)
    if game.home_points > game.away_points:
        if betTeam == homeTeam:
            return [possibleWinnings, -betAmount, 1, 0, possibleProfit]
        else:
            return [0, -betAmount, 0, 1, 0, 0]
    else:
        if betTeam == awayTeam:
            
            return [possibleWinnings, -betAmount, 1, 0, possibleProfit]
        else:
            return [0, -betAmount, 0, 1, 0, 0]

def placeBet(leagueState, game, bankroll):
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
    
    bet = (kc.get_model_lines_plus_kelly(homeTeam,
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


if __name__ == '__main__':
    years = read_years()
    #years = [1819]
    totalWins = 0
    totalLosses = 0
    totalGrowth = 0
    totalNumWagers = 0
    totalWagered = 0
    totalMade = 0
    totalEdge = 0
    for year in years:
        WINS = 0
        LOSSES = 0
        leagueState = instantiateTeams()
        schedule_dict = create_schedule_dict(read_data(year))
        datesWithGames = create_daily_slate(set(schedule_dict.keys()))
        bankroll = 100
        wageredMoney = 0
        profits = 0
        count = 0
        numWagers = 0
        additiveEdge = 0
        for date in datesWithGames:
            if count >= len(datesWithGames) - 1:
            #if count >= 100:
                break

            slate = schedule_dict[date]
            
            if count > 10:
                slateWinnings = 0
                slateCost = 0
                for g in slate:
                    wager = placeBet(leagueState, g, bankroll)
                    slateWinnings += wager[0]
                    slateProfit = wager[4]
                    slateCost = wager[1]
                    bankroll += slateCost
                    
                    numWagers += 1
                    WINS += wager[2]
                    LOSSES += wager[3]
                    wageredMoney -= slateCost
                    try:
                        additiveEdge += (slateProfit/-slateCost)
                    except:
                        additiveEdge += (slateProfit/1)

                    
               
                profits += slateWinnings
                bankroll += slateWinnings
            leagueState = timestep(leagueState, slate)

            count += 1
        expectedGrowth = 100.0* (((bankroll/100.0)**(1/numWagers))-1)
        expectedGrowth = str(expectedGrowth)
        expectedGrowth = expectedGrowth[:5]
        totalLosses += LOSSES
        totalWins += WINS
        totalGrowth += float(expectedGrowth)
        totalNumWagers += numWagers
        totalWagered += wageredMoney
        totalMade += bankroll-100
        yearlyEdge = additiveEdge/numWagers
        totalEdge += yearlyEdge
    #     print("year:", year)
    #     print("ending bankroll:", bankroll)
    #     print("expected growth:", expectedGrowth, "percent")
    #     print("number of wagers simulated:", numWagers)
    #     print("number of wins:", WINS)
    #     print("number of losses:", LOSSES)
    #     print(" ")
    #     print("total money wagered:", wageredMoney)
    #     print("total profit:", bankroll - 100)
    #     print("average expected value:", (bankroll-100)/wageredMoney)
    #     print("______________")

    print("******************")
    print("Total wins over", str(len(years)), "years:", totalWins)
    print("Total losses over", str(len(years)), "years:", totalLosses)
    print("Average expected growth", str(len(years)), "years:", totalGrowth / len(years))
    print("Average expected value:", totalEdge/len(years))

