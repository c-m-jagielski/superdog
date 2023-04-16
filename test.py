# Superdog

import time
#from pymongo import MongoClient

"""
 Let people create a "league" (group) of up to 10 players
 Create team names
 Get the available games for the week
 Select your team to beat the spread
 Track who's right or not
 Track if anyone's superdog wins outright
 Log outright wins and overall W/L records of all teams
"""

"""
  Main thread:
    initialize users in db with 0 wins & any user data
    input all possible games for this week
    add those games to the database
    users select their Superdog (pick a "loser" team to beat the spread)
    add those selections
    when games end,
        add the game outcomes to the db
        query who picked what
        calculate outright wins
        calculate superdog wins
        add user updates to the db
    query user db to show WL record after this week
    start again the next week!
"""

def setup():
    print("Welcome to the Superdog showdown!")

    # These should be "global"... persist across all games
    outrightWin = 0
    superdogWin = 0

    # Set up a game
    team1 = "Dallas"
    team2 = "Denver"
    expectedWinner = team2
    spread = 7.0

    # I pick this game as my Superdog, choosing the non-picked team to beat the spread
    myTeam = team1
    winner = team1
    loser = team2
    scores = {
        "Dallas": 24,
        "Denver": 14,
    }
    multiplier = -1 if winner != expectedWinner else 1
    margin = (scores[winner] - scores[loser]) * multiplier
    #print("margin:", margin)

    # Did your Superdog team get an outright win?
    if myTeam == winner:
        outrightWin += 1
        superdogWin += 1
    else:
        # Did my team at least beat the spread?
        if margin < spread:
            superdogWin += 1

    print("\nReport at " + str(time.ctime()) + ":")
    print("outrightWin:", outrightWin)
    print("superdogWin:", superdogWin)

"""
def init_mongo():
    client = MongoClient()  # MongoClient('localhost', 27017)
    db = client.test_database  # or ... client['test-database']
    collection = db.test_collection  # a group of stored documents
"""

def test_placeholder():
    pass

if __name__ == "__main__":
    setup()
