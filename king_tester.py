import csv
#import kings_scrape as ks
import king_calculator as kc
import requests
from lxml import html
from datetime import datetime



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

def read_data(year):
    listOfGames = []
    with open('C:/Users/imaxm/Desktop/mitSophomore/sportsBetting/miller-fund/historical_odds/' + str(year) + '.csv') as csv_file:
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

def calculate_winnings(betStatement):
    return 15

def placeBets(leagueState, game, bankroll):
    homeTeam = game.home_team_city
    awayTeam = game.away_team_city
    homePointsFor = leagueState[homeTeam].pointsFor
    homePointsAgainst = leagueState[homeTeam].pointsAgainst
    homeTeamRecord = leagueState[homeTeam].record
    homeTeamHomeRecord = leagueState[homeTeam].homeWins
    homeLine = game.home_moneyLine
    awayPointsFor = leagueState[awayTeam].pointsFor
    awayPointsAgainst = leagueState[awayTeam].pointsAgainst
    awayTeamRecord = leagueState[awayTeam].record
    awayTeamAwayRecord = leagueState[awayTeam].awayWins
    awayLine = game.away_moneyLine
    
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
    
    return calculate_winnings(bet)


if __name__ == '__main__':
    
    leagueState = instantiateTeams()
    schedule_dict = create_schedule_dict(read_data(1617))
    datesWithGames = create_daily_slate(set(schedule_dict.keys()))
    bankroll = 100.0
    count = 0
    for date in datesWithGames:
        print(bankroll)
        dateWinnings = 0
        if count >= 4:
            break

        slate = schedule_dict[date]
        
        if count > 2:
            
            
            for g in slate:
                dateWinnings += placeBets(leagueState, g, bankroll)
            bankroll += dateWinnings    
            print("placing bets for", date)

        leagueState = timestep(leagueState, slate)

        count += 1