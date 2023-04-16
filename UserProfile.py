import time

class UserProfile:
    def __init__(self, name, email, photo):
        self.name = name
        self.email = email
        self.photo = photo

        self.initTime = time.time()
        self.lastUpdateTime = self.initTime

        self.outrightWins = 0
        self.superdogWins = 0

    def chooseGame(self, game):
        """
        Choose their Superdog for this week, store in db

        :param game:
        :return:
        """
        print("game:", game)

    def updateRecord(self, outrightWin, superdogWin):
        """
        Update the user's record

        :param outrightWin:
        :param superdogWin:
        :return:
        """
        #TODO do this in the db instead of class variables
        self.outrightWins += outrightWin
        self.superdogWins += superdogWin

if __name__ == "__main__":
    userName = "Bob"
    userEmail = "bob@gmail.com"
    userPic = "coolbob.jpg"

    user_profile = UserProfile(userName, userEmail, userPic)
