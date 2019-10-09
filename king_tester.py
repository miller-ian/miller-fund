import csv
import kings_scrape as ks
import requests
from lxml import html
from datetime import datetime



class Team:
    def __init__(self, name, games, homeWins, awayWins, pointsFor, pointsAgainst):
        self.name = name
        self.games = games
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
        leagueState[team] = Team(team, [], [], [], 0, 0)
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
    newLeagueState = leagueState

    for game in slate:
        homeTeam = game.home_team_city
        homePoints = game.home_points

        awayTeam = game.away_team_city
        awayPoints = game.away_points

        homeWin = 1
        awayWin = 0
        if awayPoints > homePoints:
            awayWin = 1
            homeWin = 0
        homeTeamObject = leagueState[homeTeam]
        homeGames = homeTeamObject.games
        homePointsFor = homeTeamObject.pointsFor
        homePointsAgainst = homeTeamObject.pointsAgainst
        homeWinsAway = homeTeamObject.awayWins  #will remainn constant
        homeWins = homeTeamObject.homeWins

        homeGames.append(game)
        updatedHomePointsFor = homePointsFor + int(homePoints)
        updatedHomePointsAgainst = homePointsAgainst + int(awayPoints)
        if len(homeWins) > 0:
            updatedHomeWinTotal = homeWins[-1] + homeWin
            homeWins.append(updatedHomeWinTotal)
        else:
            homeWins.append(homeWin)

        updatedHomeTeam = Team(homeTeam, homeGames, homeWins, homeWinsAway, updatedHomePointsFor, updatedHomePointsAgainst)
        
        awayTeamObject = leagueState[awayTeam]
        awayGames = awayTeamObject.games
        awayPointsFor = awayTeamObject.pointsFor
        awayPointsAgainst = awayTeamObject.pointsAgainst
        awayWinsHome = awayTeamObject.homeWins  #will remain constant
        awayWins = awayTeamObject.awayWins

        awayGames.append(game)
        updatedAwayPointsFor = awayPointsFor + int(awayPoints)
        updatedAwayPointsAgainst = awayPointsAgainst + int(homePoints)
        if len(awayWins) > 0:
            updatedAwayWinTotal = awayWins[-1] + awayWin
            awayWins.append(updatedAwayWinTotal)
        else:
            awayWins.append(awayWin)

        updatedAwayTeam = Team(awayTeam, awayGames, awayWinsHome, awayWins, awayPointsFor, awayPointsAgainst)

        leagueState[awayTeam] = updatedAwayTeam
        leagueState[homeTeam] = updatedHomeTeam        

    return newLeagueState

def placeBets(leagueState, date):
    return None


if __name__ == '__main__':
    # date = None
    # teams = instantiateTeams()
    leagueState = instantiateTeams()
    schedule_dict = create_schedule_dict(read_data(1617))
    datesWithGames = create_daily_slate(set(schedule_dict.keys()))
    
    count = 0
    for date in datesWithGames:
        if count >= 1:
            break
        slate = schedule_dict[date]

        for g in slate:
            placeBets(leagueState, slate)
            leagueState = timestep(leagueState, slate)

        
        count += 1