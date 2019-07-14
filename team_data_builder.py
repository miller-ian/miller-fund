import csv

class Team:
    def __init__(self, id, numGamesPlayed, numHomeGames, results, homeResults, awayResults, pointsFor, pointsAgainst, PE, winProbability):
        self.id = id
        self.numGamesPlayed = numGamesPlayed
        self.numHomeGames = numHomeGames
        self.results = results
        self.homeResults = homeResults
        self.awayResults = awayResults
        self.pointsFor = pointsFor
        self.pointsAgainst = pointsAgainst
        self.PE = PE
        self.winProbability = winProbability
        
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

def calculate_moving_team_record(results):
    listOfRecord = []
    nthGame = 0
    for i in range(0, numGames):
        nthGame += 1
        listOfRecord.append(int(toDateWins[i])/nthGame)
    return trailing_weighted_average(listOfRecord, create_triangle_num_list(numGames))

def get_pythagorean_expectation(pf, pa):
    expectation = (pow(pf, 1.81))/(pow(pf, 1.81) + pow(pa, 1.81))
    return expectation


def calculate_moving_homegame_record(numGames):
    homeRecord = parse_home_away(tree, numGames)[1]
    homeGames = len(homeRecord)
    listOfRecord = []
    nthGame = 0
    for i in range(0, homeGames):
        nthGame += 1
        listOfRecord.append(homeRecord[i]/nthGame)
    return trailing_weighted_average(listOfRecord, create_triangle_num_list(homeGames))


def compile_game(team, home, pf, pa):
    for i in listOfTeams:
        if i.id == team:
            teamOfInterest = i
    teamOfInterest.numGamesPlayed += 1
    if home:
        teamOfInterest.numHomeGames += 1
    lastResult = teamOfInterest.results[numGamesPlayed-1]
    lastHomeResult = teamOfInterest.homeResults[numHomeGames - 1]
    lastAwayResult = teamOfInterest.awayResults[numGamesPlayed - numHomeGames - 1]

    if pf > pa:
        teamOfInterest.results.append(lastResult + 1)
        if home:
            teamOfInterest.homeResults.append(lastHomeResult + 1)
        else:
            teamOfInterest.awayResults.append(lastAwayResult + 1)
    else:
        teamOfInterest.append(lastResult)
        if home:
            teamOfInterest.homeResults.append(lastHomeResult)
        else:
            teamOfInterest.awayResults.append(lastAwayResult)
    teamOfInterest.pointsFor += pf
    teamOfInterest.pointsAgainst += pa
    teamOfInterest.PE = (teamOfInterest.pointsFor, teamOfInterest.pointsAgainst)
    overallMovingRecord = calculate_moving_team_record(teamOfInterest.results)
    
    
def initializeListOfTeams():
    returnList = []
    for team in teamNames:
        returnList.append(Team(team, 0, 0, [], [], [], 0, 0, 0, null))
    return returnList

    


with open('C:/Users/imaxm/Desktop/mitSophomore/sportsBetting/miller-fund/historical_odds/1617.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=",")
    line_count = 1
    listOfTeams = initializeListOfTeams()
    for row in csv_reader:
        teamName = row[3]
        print(teamName)
        for team in listOfTeams:
            if teamName == team.id:
                compile_game(team)
                print(team.results)

        


    
