
# The Miller Fund
The purpose of this repo is to make money betting on NBA games.

# How to Use

1- Clone this repo

2- Open a terminal and run king_main.py

3- You must enter team abbreviations in all CAPS, and they must match exactly the abbreviations I have specified in king_reader.py. For example, if you want to consult the model on how to bet Clippers v Lakers, you would type LAL for home team abbreviation and LAC for away team abbreviation. 

# Notes

The model uses Kelly criterion to optimize expected value. The basic premise is this: the bigger the delta between a sportsbook line and the model's line, the more confident you should be in that bet. Therefore, you should place more money on that bet. This is why the model asks for your total bankroll.

This model scrapes from several websites to limit the amount of info you need to enter as the user. At times, there will be errors with the model if one website is updated and one is not yet. Therefore, its best to consult this model around 4 EST if you planning on placing for that night's slate of games. I've empirically determined that 4 EST is a safe time to assume that all websites I'm scraping from are completely up to date.

# Performance

As of now, the Miller Fund NBA Model has returned 7% over 80 games wagered on. 

Backtesting is currently in development to be able to refine model.
