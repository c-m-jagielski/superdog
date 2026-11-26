Superdog


Based on College Gameday weekly SuperDog picks.
Multiple players can play. Each player chooses a "superdog", akin to an underdog, to beat the spread on a given weekend of college football games.
Players accumulate points each week and compete against each other throughout the season.
Outright wins give more points.

Ideally I'd like this game to keep track of the user's picks and accumulate scores automatically based on an available API somewhere of real-time games.

I do not claim to own or have come up with this idea.

## Web app

`app/index.html` is a self-contained web app for running a Superdog league:

- Players join with a team name and pick one underdog per week (picks lock at kickoff).
- The commissioner posts each week's games and spreads, then enters final scores.
- Scoring follows `test.py`: an underdog that loses by less than the spread is a cover (1 pt by default); an outright win scores more (2 pts by default); losing by exactly the spread is a push.
- Standings rank players by points, then outright wins, with a week-by-week grid.

It is built to run as a Claude artifact, which stores league data and identifies players. Live scores aren't pulled automatically yet; the commissioner enters final scores.
