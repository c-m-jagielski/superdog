# Superdog

"""
 Let people create a "league" (group) of up to 10 players
 Create team names
 Get the available games for the week
 Select your team to beat the spread
 Track who's right or not
 Track if anyone's superdog wins outright
 Log outright wins and overall W/L records of all teams
"""

def setup():
    print "Welcome to the Superdog showdown!"

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
    #print "margin:", margin

    # Did your Superdog team get an outright win?
    if myTeam == winner:
        outrightWin += 1
        superdogWin += 1
    else:
        # Did my team at least beat the spread?
        if margin < spread:
            superdogWin += 1

    print "outrightWin:", outrightWin
    print "superdogWin:", superdogWin

if __name__ == "__main__":
    setup()