import csv
import sys
import json
from datetime import datetime
from lxml import html
import requests
import math_helper as mt

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
                print(stuff['displayGroups'][0]['markets'][0]['outcomes'][0]['price']['american'])
                away = stuff['displayGroups'][0]['markets'][0]['outcomes'][0]['price']['american']
                home = stuff['displayGroups'][0]['markets'][0]['outcomes'][1]['price']['american']
                aDict[event] = [away, home]
            except:
                aDict[event] = [0, 0]
                continue
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

def calculate_moving_team_record(tree, numGames):
    toDateWins = tree.xpath('//tr//td[@data-stat="wins"]/text()')
    listOfRecord = []
    nthGame = 0
    for i in range(0, numGames):
        nthGame += 1
        listOfRecord.append(int(toDateWins[i])/nthGame)
    return mt.trailing_weighted_average(listOfRecord, mt.create_triangle_num_list(numGames))

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
    return mt.trailing_weighted_average(listOfRecord, mt.create_triangle_num_list(awayGames))

def calculate_moving_homegame_record(tree, numGames):
    homeRecord = parse_home_away(tree, numGames)[1]
    homeGames = len(homeRecord)
    listOfRecord = []
    nthGame = 0
    for i in range(0, homeGames):
        nthGame += 1
        listOfRecord.append(homeRecord[i]/nthGame)
    return mt.trailing_weighted_average(listOfRecord, mt.create_triangle_num_list(homeGames))

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

def write(homeTeam, awayTeam):
    homeLong = get_team_long(homeTeam)
    awayLong = get_team_long(awayTeam)
    price_dict = parse_prices(awayLong, homeLong, build_price_dict())
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
    homeTeamMovingRecord = calculate_moving_team_record(tree, numGamesPlayed)
    awayTeamMovingRecord = calculate_moving_team_record(awayTree, numGamesPlayedAway)

    homeTeamMovingHomeRecord = calculate_moving_homegame_record(tree, numGamesPlayed)
    awayTeamMovingAwayRecord = calculate_moving_awaygame_record(tree, numGamesPlayedAway)

    homeTeamPythagoreanExpectation = calculate_pythagorean_expectation(newTree, homeTeam)
    awayTeamPythagoreanExpectation = calculate_pythagorean_expectation(newTreeAway, awayTeam)
    
    today = datetime.today()
    print(price_dict)
    # print(today)
    # print(homeTeam)
    # print(homeTeamMovingRecord)
    # print(homeTeamMovingHomeRecord)
    # print(homeTeamPythagoreanExpectation)
    # print(price_dict) #home
    # print(awayTeam)
    # print(awayTeamMovingRecord)
    # print(awayTeamMovingAwayRecord)
    # print(awayTeamPythagoreanExpectation)
    # print(price_dict[0])


    
    with open('1920.csv', 'a') as csv_file:

        csv_writer = csv.writer(csv_file, delimiter=',')
        csv_writer.writerow([today, 
                            homeTeam, 
                            homeTeamMovingRecord, 
                            homeTeamMovingHomeRecord, 
                            homeTeamPythagoreanExpectation, 
                            price_dict[1], 
                            awayTeam, 
                            awayTeamMovingRecord, 
                            awayTeamMovingAwayRecord, 
                            awayTeamPythagoreanExpectation, 
                            price_dict[0]])
        

