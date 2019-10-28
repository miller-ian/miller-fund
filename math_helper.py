import math

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

def calculate_pythagorean_expectation(pointsFor, pointsAgainst):
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
    winProb *= (1/100)
    if odds > 0:
        b = (odds / 100.0) + 1
    else:
        b = (100.0 / -odds) + 1
    b -= 1
    q = 1-winProb
    edge = (b*winProb-q) / b
    return edge*bankroll