import csv
#import kings_scrape as ks
import requests
from lxml import html

<<<<<<< HEAD
=======

>>>>>>> d21ded2dc00af072fceb105101f5f3ef51d1dee5
class Game:
    def __init__(self, date, home_team_city, away_team_city, home_moneyLine, away_moneyLine):
        self.date = date
        self.home_team_city = home_team_city
        self.away_team_city = away_team_city
        self.home_moneyLine = home_moneyLine
        self.away_moneyLine = away_moneyLine
<<<<<<< HEAD
    
listOfGames = []

with open('C:/Users/imaxm/Desktop/mitSophomore/sportsBetting/miller-fund/historical_odds/1617.csv') as csv_file:
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


    
print("home line for 1st game is", listOfGames[0].home_moneyLine)
=======

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
        
print(get_point_total(team, 5))
>>>>>>> d21ded2dc00af072fceb105101f5f3ef51d1dee5
