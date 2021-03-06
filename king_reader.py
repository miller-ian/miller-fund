from lxml import html
import requests
import math
import json
from datetime import datetime
import sys

def build_price_dict():
    aDict = {}
    source = requests.get('https://www.bovada.lv/services/sports/event/v2/events/A/description/basketball/nba').json()
    length = len(source[0]['events'])
    for i in range(length):
        stuff = source[0]['events'][i]
    
    
        eventType = stuff['type']
        if eventType == "GAMEEVENT":
            event = stuff['description']
            try:
                away = stuff['displayGroups'][0]['markets'][0]['outcomes'][0]['price']['american']
                home = stuff['displayGroups'][0]['markets'][0]['outcomes'][1]['price']['american']
                aDict[event] = [away, home]
            except:
                print(" ")
    return aDict
    
def parse_prices(awayTeam, homeTeam, price_dict):
    for i in price_dict.keys():
        if awayTeam in i and homeTeam in i:
            return price_dict[i]    

def get_team_location(team):
    return{
        'GSW' : 'golden-state-warriors',
        'MIL' : 'milwaukee-bucks',
        'PHI' : 'philadelphia-76ers',
        'NOP' : 'new-orleans-pelicans',
        'OKC' : 'oklahoma-city-thunder',
        'TOR' : 'toronto-raptors',
        'LAC' : 'la-clippers',
        'WAS' : 'washington-wizards',
        'SAC' : 'sacramento-kings',
        'POR' : 'portland-trail-blazers',
        'HOU' : 'houston-rockets',
        'BOS' : 'boston-celtics',
        'SAS' : 'san-antonio-spurs',
        'BRK' : 'brooklyn-nets',
        'LAL' : 'los-angeles-lakers',
        'DEN' : 'denver-nuggets',
        'MIN' : 'minnesota-timberwolves',
        'CHO' : 'charlotte-hornets',
        'ATL' : 'atlanta-hawks',
        'UTA' : 'utah-jazz',
        'DAL' : 'dallas-mavericks',
        'IND' : 'indiana-pacers',
        'DET' : 'detroit-pistons',
        'PHO' : 'phoenix-suns',
        'ORL' : 'orlando-magic',
        'NYK' : 'new-york-knicks',
        'MIA' : 'miami-heat',
        'CHI' : 'chicago-bulls',
        'CLE' : 'cleveland-cavaliers',
        'MEM' : 'memphis-grizzlies',
    }.get(team)

def get_team_long(team):
    return{
        'GSW' : 'Golden State Warriors',
        'MIL' : 'Milwaukee Bucks',
        'PHI' : 'Philadelphia 76ers',
        'NOP' : 'New Orleans Pelicans',
        'OKC' : 'Oklahoma City Thunder',
        'TOR' : 'Toronto Raptors',
        'LAC' : 'Los Angeles Clippers',
        'WAS' : 'Washington Wizards',
        'SAC' : 'Sacramento Kings',
        'POR' : 'Portland Trail Blazers',
        'HOU' : 'Houston Rockets',
        'BOS' : 'Boston Celtics',
        'SAS' : 'San Antonio Spurs',
        'BRK' : 'Brooklyn Nets',
        'LAL' : 'Los Angeles Lakers',
        'DEN' : 'Denver Nuggets',
        'MIN' : 'Minnesota Timberwolves',
        'CHO' : 'Charlotte Hornets',
        'ATL' : 'Atlanta Hawks',
        'UTA' : 'Utah Jazz',
        'DAL' : 'Dallas Mavericks',
        'IND' : 'Indiana Pacers',
        'DET' : 'Detroit Pistons',
        'PHO' : 'Phoenix Suns',
        'ORL' : 'Orlando Magic',
        'NYK' : 'New York Knicks',
        'MIA' : 'Miami Heat',
        'CHI' : 'Chicago Bulls',
        'CLE' : 'Cleveland Cavaliers',
        'MEM' : 'Memphis Grizzlies',
    }.get(team)

def get_record(tree):
    stuff = tree.xpath('//tr[@class="team-blockup-data"]//td//p/text()')
    record = stuff[0]
    dash = record.find('-')
    wins = int(record[:dash])
    losses = int(record[dash+1:])
    return wins+losses

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

def calculate_moving_team_record(tree, numGames):
    toDateWins = tree.xpath('//tr//td[@data-stat="wins"]/text()')
    listOfRecord = []
    nthGame = 0
    for i in range(0, numGames):
        nthGame += 1
        listOfRecord.append(int(toDateWins[i])/nthGame)
    return trailing_weighted_average(listOfRecord, create_triangle_num_list(numGames))

def parse_home_away(tree, numGames):
    results = tree.xpath('//tr//td/text()')
    awayWins = 0
    awayRecord = []
    awayGames = 0
    homeWins = 0
    homeRecord = []
    homeGames = 0
    for i in range((7 * numGames) - 1):
        if results[i] == '@':
            awayGames += 1
            if results[i + 1] == 'W':
                awayWins += 1
                awayRecord.append(awayWins)
            elif results[i + 1] == 'L':
                awayRecord.append(awayWins)
        if ('p' in results[i]) and (results[i+1] != '@'):
            homeGames += 1
            if results[i + 1] == 'W':
                homeWins += 1
                homeRecord.append(homeWins)
            elif results[i + 1] == 'L':
                homeRecord.append(homeWins)
    return awayRecord, homeRecord

def calculate_moving_awaygame_record(tree, numGames):
    awayRecord = parse_home_away(tree, numGames)[0]
    awayGames = len(awayRecord)
    listOfRecord = []
    nthGame = 0
    for i in range(0, awayGames):
        nthGame += 1        
        listOfRecord.append(awayRecord[i]/(nthGame))
    return trailing_weighted_average(listOfRecord, create_triangle_num_list(awayGames))

def calculate_moving_homegame_record(tree, numGames):
    homeRecord = parse_home_away(tree, numGames)[1]
    homeGames = len(homeRecord)
    listOfRecord = []
    nthGame = 0
    for i in range(0, homeGames):
        nthGame += 1
        listOfRecord.append(homeRecord[i]/nthGame)
    return trailing_weighted_average(listOfRecord, create_triangle_num_list(homeGames))

def calculate_pythagorean_expectation(tree, team):
    """
    Final value will be a weighted average of pythagorean expectation over the season and
    the last 3 games.

    season- 70%
    last3 - 30%
    """
    stats = tree.xpath('//table[@class="tr-table"]//tr//td[@class="text-right"]/text()')
    power = 8.9
    pointsFor = float(stats[3])
    pointsAgainst = float(stats[13])
    expectation = (pow(pointsFor, power))/(pow(pointsFor, power) + pow(pointsAgainst, power))
    return expectation


def normalize(p1, p2):
    regular = True
    greater = 0
    smaller = 0
    if p1 > p2:
        greater = p1
        smaller = p2
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
    print(winProb, odds, bankroll)
    winProb *= (1/100)
    if odds > 0:
        b = (odds / 100.0) + 1
    else:
        b = (100.0 / -odds) + 1
    b -= 1
    q = 1-winProb
    edge = (b*winProb-q) / b
    return edge*bankroll

def get_model_lines(homeTeam, awayTeam):
    homeConfidence = (50 * calculate_pythagorean_expectation(newTree, homeTeam)) + (25 * calculate_moving_team_record(tree, numGamesPlayed)) + (25 * calculate_moving_homegame_record(tree, numGamesPlayed))
    awayConfidence = (50 * calculate_pythagorean_expectation(newTreeAway, awayTeam)) + (25 * calculate_moving_team_record(awayTree, numGamesPlayedAway)) + (25 * calculate_moving_awaygame_record(awayTree, numGamesPlayedAway))
    normalizedHome = (normalize(homeConfidence, awayConfidence)[0]*100) 
    normalizedAway = (normalize(homeConfidence, awayConfidence)[1]*100)
    winner = homeTeam
    loser = awayTeam
    if homeConfidence < awayConfidence:
        winner = awayTeam
        loser = homeTeam
    if winner == awayTeam:
        return ((winner, 'if moneyline >', convert_to_moneyline(normalizedAway)), (loser, 'if moneyline >', convert_to_moneyline(normalizedHome)))
    else:
        return ((winner, 'if moneyline >', convert_to_moneyline(normalizedHome)), (loser, 'if moneyline >', convert_to_moneyline(normalizedAway)))

def get_model_lines_plus_kelly(homeTeam, newTree, tree, numGamesPlayed, awayTeam, newTreeAway, awayTree, numGamesPlayedAway, bankroll):
    weights = [100, 0, 0]
    homeConfidence = (weights[0] * calculate_pythagorean_expectation(newTree, homeTeam)) + (weights[1] * calculate_moving_team_record(tree, numGamesPlayed)) + (weights[2] * calculate_moving_homegame_record(tree, numGamesPlayed))
    awayConfidence = (weights[0] * calculate_pythagorean_expectation(newTreeAway, awayTeam)) + (weights[1] * calculate_moving_team_record(awayTree, numGamesPlayedAway)) + (weights[2] * calculate_moving_awaygame_record(awayTree, numGamesPlayedAway))
    
    normalizedHome = (normalize(homeConfidence, awayConfidence)[0]*100) 
    normalizedAway = (normalize(homeConfidence, awayConfidence)[1]*100)
    print(str(homeTeam) + " -> " + str(normalizedHome))
    print(str(awayTeam) + " -> " + str(normalizedAway))
    price_dict = build_price_dict()
    awayTeamForPrice = get_team_long(awayTeam)
    homeTeamForPrice = get_team_long(homeTeam)
    try:
        awayLine, homeLine = parse_prices(awayTeamForPrice, homeTeamForPrice, price_dict)

        if awayLine == 'EVEN':
            awayLine = 100.0
        if homeLine == 'EVEN':
            homeLine = 100.0
        awayLine = int(awayLine)

        homeLine = int(homeLine)
        awayWager = kelly_compute(normalizedAway, awayLine, bankroll)
        homeWager = kelly_compute(normalizedHome, homeLine, bankroll)
        if awayWager > 0:
            return ("bet " + str(awayWager) + " on " + str(awayTeam))
        else:
            return ("bet " + str(homeWager) + " on " + str(homeTeam))
    except:
        today = datetime.today()
        d1 = datetime.strptime("10-23-2019", '%m-%d-%Y')
        delta = (d1 - today).days
        
        return ("No listings for this game yet! The NBA season starts in " + str(delta) + " days")

def theMain(homeTeam, awayTeam, bankroll):
    
    try:
        bankroll = float(bankroll)
    except:
        print("Please enter a valid number for bankroll!")
        sys.exit(1)

    try:
        page = requests.get('https://www.basketball-reference.com/teams/' + str(homeTeam) + '/2019_games.html')
        tree = html.fromstring(page.content)

        newPage = requests.get('https://www.teamrankings.com/nba/team/' + get_team_location(homeTeam) + '/')
        newTree = html.fromstring(newPage.content)
        
        awayPage = requests.get('https://www.basketball-reference.com/teams/' + str(awayTeam) + '/2019_games.html')
        awayTree = html.fromstring(awayPage.content)

        newPageAway = requests.get('https://www.teamrankings.com/nba/team/' + get_team_location(awayTeam) + '/')
        newTreeAway = html.fromstring(newPageAway.content)
    except:
        print("One or both teams entered does not exist!")
        sys.exit(1)
    numGamesPlayed = get_record(newTree)
    numGamesPlayedAway = get_record(newTreeAway)
    print(get_model_lines_plus_kelly(homeTeam, newTree, tree, numGamesPlayed, awayTeam, newTreeAway, awayTree, numGamesPlayedAway, bankroll))







