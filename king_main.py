import king_scraper as ks
import king_reader as kr
if __name__ == '__main__':

    homeTeam = input("Give 3-letter abbreviation for home team: ")
    awayTeam = input("Give 3-letter abbreviation for away team: ")

    ks.write(homeTeam, awayTeam)
    
    bankroll = input("Enter your bankroll:")

    print(kr.theMain(homeTeam, awayTeam, bankroll))