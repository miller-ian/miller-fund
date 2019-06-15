import csv

class Game:
    def __init__(self, date, home_team_city, away_team_city, home_moneyLine, away_moneyLine):
        self.date = date
        self.home_team_city = home_team_city
        self.away_team_city = away_team_city
        self.home_moneyLine = home_moneyLine
        self.away_moneyLine = away_moneyLine
    
listOfGames = []

with open('C:/Users/imaxm/Desktop/mitSophomore/sportsBetting/historical_odds/1617.csv') as csv_file:
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
    
print(listOfGames[0].home_moneyLine)