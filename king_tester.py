import csv
#import kings_scrape as ks
import requests
from lxml import html


class Team:
    def __init__(self, name, games, pointsFor, pointsAgainst):
        self.name = name
        self.games = games
        self.pointsFor = pointsFor
        self.pointsAgainst = pointsAgainst

class Game:
    def __init__(self, date, home_team_city, away_team_city, home_moneyLine, away_moneyLine):
        self.date = date
        self.home_team_city = home_team_city
        self.away_team_city = away_team_city
        self.home_moneyLine = home_moneyLine
        self.away_moneyLine = away_moneyLine

year = str(input("Enter year:"))
team = input("Enter 3 letter abbreviation for team:")
def read_data(year):
    listOfGames = []

    with open('C:/Users/imaxm/Desktop/mitSophomore/sportsBetting/historical_odds/' + year + '.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=",")
        line_count = 1
        for row in csv_reader:
            if line_count == 1:
                print(row)
                line_count += 1
            else:

                if line_count % 2 == 0:
                    away_team_city = row[3]
                    away_moneyLine = row[11]
                    line_count += 1
                else:
                    home_team_city = row[3]
                    home_moneyLine = row[11]
                    line_count += 1
                    newGame = Game(row[0], home_team_city, away_team_city, home_moneyLine, away_moneyLine)
                    listOfGames.append(newGame)
        return listOfGames

def get_point_total(homeTeam, n):
    total = 0
    page = requests.get('https://www.basketball-reference.com/teams/' + str(homeTeam) + '/20' + year[2:] + '_games.html#games_link')
    tree = html.fromstring(page.content)
    print(tree)
    for i in range(1, n+1):
        stuff = tree.xpath('//*[@id="games"]/tbody/tr[' + str(i) + ']/td[9]/text()')
        total += int(stuff[0])
    return total

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
        leagueState[team] = Team(team, None, 0, 0)
    return leagueState


if __name__ == '__main__':
    # date = None
    # teams = instantiateTeams()
    print(instantiateTeams())