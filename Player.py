from database import querySQL
from trueskill import Rating, rate_1vs1, quality_1vs1
import bcrypt
ALPHANUM = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890"
PLAYERS = {}

class Player:
    # reset Player use table
    @staticmethod
    def resetTable():
        querySQL("DROP TABLE IF EXISTS players;")
        Player.createTable()

    # create Player user table 
    @staticmethod
    def createTable():
        querySQL((
            "CREATE TABLE IF NOT EXISTS players ("
            "id INTEGER PRIMARY KEY,"
            "username VARCHAR(64) UNIQUE NOT NULL,"
            "password VARCHAR(64) NOT NULL,"
            "tokens INTEGER DEFAULT 0,"
            "skillMu REAL DEFAULT 25.000,"
            "skillSigma REAL DEFAULT 8.333,"
            "sid VARCHAR(64) DEFAULT NULL,"
            "opponent INTEGER REFERENCES players(id) DEFAULT NULL,"
            "active INTEGER DEFAULT 0,"
            "gameMode VARCHAR(32) DEFAULT NULL,"
            "gameFormat VARCHAR(32) DEFAULT NULL,"
            "gameWager INTEGER DEFAULT 0"
            ");"
        ))
        Player.create("shahrose", "pass")
        Player.create("rose", "pass")

    # reset ephemeral Player columns (server startup)
    @staticmethod
    def startTable():
        Player.createTable()
        querySQL("UPDATE players SET sid = NULL, opponent = NULL;")

    # get player by socket.io ID
    @classmethod
    def get(cls, sid):
        result = querySQL("SELECT * FROM players WHERE sid = ? LIMIT 1;", sid)
        if result==None: return None
        return cls(result)


    # Fetch Player by username|id (also validates password if provided)
    # if search fails, returns error <String>
    @classmethod
    def fetch(cls, username, plainPassword=None):
        if type(username) is int or username.isdigit():
            result = querySQL("SELECT * FROM players WHERE id = ? LIMIT 1", username)            
        else:
            result = querySQL("SELECT * FROM players WHERE username = ? LIMIT 1", username)
        if result==None:
            return "User does not exist"
        if plainPassword!=None and not bcrypt.checkpw(plainPassword.encode('utf8'), result["password"]):
            return "Password is incorrect"
        return cls(result)

    # Create/Fetch Player in database
    # if creation fails, returns error <String>
    @classmethod
    def create(cls, username, plainPassword):
        if any([(char not in ALPHANUM) for char in username]):
            return "Username must be alphanumeric"
        if username.isdigit():
            return "Username can not be a number."
        if type(Player.fetch(username))==Player:
            return "User already exists"
        hashPassword = bcrypt.hashpw(plainPassword.encode('utf8'), bcrypt.gensalt())
        pid = querySQL(
            "INSERT INTO players (username, password) VALUES (?,?);",
            username,
            hashPassword
        )
        return Player.fetch(pid)

    def __init__(self, dbDict):
        self.__id = dbDict["id"]
        self.__username = dbDict['username']
        self.__hashPassword = dbDict['password']
        self.__tokens = dbDict['tokens']
        self.__rating = Rating(dbDict['skillMu'], dbDict['skillSigma'])
        self.__sid = dbDict['sid']
        # game state
        self.__opponent = dbDict['opponent']
        self.__active = dbDict['active']
        self.__gameMode = dbDict['gameMode']
        self.__gameFormat = dbDict['gameFormat']
        self.__gameWager = dbDict['gameWager']

    def __repr__(self):
        return str(self)

    def __str__(self):
        activeChar = "[!]" if self.active else ""
        return f"<Player{self.id}> {self.username} ({self.sid}) {activeChar}"

    def __eq__(self, other):
        if type(other) is not Player: return False
        return self.id == other.id

    def __hash__(self):
        return hash(self.id)

    def print(self):
        self.printTable()
        if self.opponent!=None:
            self.opponent.printTable(False)

    def printTable(self, line=True):
        if line:
            print(f"{self.username:─^27}")
        else:
            print(f"{self.username:^27}")
        print(f"    mu: {self.rating.mu:.0f}   │   id: {self.id}")
        if self.sid!=None:
            print(f" sigma: {self.rating.sigma:.1f}  │  sid: {self.sid}")
        else:
            print(f" sigma: {self.rating.sigma:.1f}  │  sid:")
    
    #####################
    # PROPERTIES
    #####################

    @property
    def id(self): return self.__id

    @property
    def username(self): return self.__username

    @property
    def hashPassword(self): return self.__hashPassword

    @property
    def password(self): raise AttributeError("<Player.password> is not directly stored for security purposes.")
    @password.setter
    def password(self, value):
        self.__hashPassword = bcrypt.hashpw(value.encode('utf8'), bcrypt.gensalt())
        querySQL("UPDATE players SET password = ? WHERE id = ?", self.__hashPassword, self.id)  

    @property
    def rating(self): return self.__rating
    @rating.setter
    def rating(self, value):
        if type(value) != Rating:
            raise ValueError(f"<Player.rating> must be a [trueskill.Rating] object, not {type(value)}")
        self.__rating = value
        querySQL(
            "UPDATE players SET skillMu = ?, skillSigma = ? WHERE id = ?",
            self.rating.mu, self.rating.sigma, self.id
        )

    @property
    def active(self): return self.__active
    @active.setter
    def active(self, value):
        self.__active = 1 if value==True else 0
        querySQL("UPDATE players SET active = ? WHERE id = ?", self.active, self.id)    

    @property
    def gameMode(self): return self.__gameMode
    @gameMode.setter
    def gameMode(self, value):
        if value == "": value = None
        self.__gameMode = value
        querySQL("UPDATE players SET gameMode = ? WHERE id = ?", self.gameMode, self.id)    

    @property
    def gameFormat(self): return self.__gameFormat
    @gameFormat.setter
    def gameFormat(self, value):
        if value == "": value = None
        self.__gameFormat = value
        querySQL("UPDATE players SET gameFormat = ? WHERE id = ?", self.gameFormat, self.id) 

    @property
    def gameWager(self): return self.__gameWager
    @gameWager.setter
    def gameWager(self, value):
        self.__gameWager = value
        querySQL("UPDATE players SET gameWager = ? WHERE id = ?", self.gameWager, self.id) 

    @property
    def sid(self): return self.__sid
    @sid.setter
    def sid(self, value):
        self.__sid = value
        querySQL("UPDATE players SET sid = ? WHERE id = ?", self.sid, self.id)    

    @property
    def online(self): return (self.__sid == None)

    @property
    def opponent(self):
        if self.__opponent==None: return None
        return Player.fetch(self.__opponent)
    @opponent.setter
    def opponent(self, value):
        if type(value)==Player:
            self.__opponent = value.id
        elif value is None:
            self.__opponent = None
        elif value.isdigit():
            self.__opponent = value
        else:
            raise ValueError("[Player.opponent] must be assigned a <Player>, <int>, or <None>")
        querySQL("UPDATE players SET opponent = ? WHERE id = ?", self.__opponent, self.id)    

    @property
    def tokens(self): return self.__tokens
    def gainTokens(self, value):
        self.__tokens += value
        querySQL("UPDATE players SET tokens = ? WHERE id = ?", self.__tokens, self.id)    
    def loseTokens(self, value):
        self.__tokens -= value
        querySQL("UPDATE players SET tokens = ? WHERE id = ?", self.__tokens, self.id)    


    #####################
    # MATCHMAKING
    #####################

    # see matchmaking compatability (0 ~ 1, higher the better)
    def getCompatability(self, otherPlayer=None):
        if otherPlayer==None: otherPlayer = self.opponent
        return quality_1vs1(self.rating, otherPlayer.rating)

    # have this player win (defeat another player)
    def beatOpponent(self, losingPlayer=None):
        # resolve game
        if self.gameMode=="competetive":
            if losingPlayer==None: losingPlayer = self.opponent
            self.rating, losingPlayer.rating = rate_1vs1(self.rating, losingPlayer.rating)
        elif self.gameMode=="casual":
            pass 
        elif self.gameMode=="casino":
            self.opponent.loseTokens(self.gameWager)
            self.gainTokens(self.gameWager)

    # clear all game-state related data
    def clearGame(self):
        self.opponent = None
        self.active = False
        self.gameMode = None
        self.gameFormat = None
        self.gameWager = 0
        print(self, self.opponent)

    # have this player abandon a game (trigger opponent's victory on their behalf)
    async def abandon(self, sio):

        if self.opponent!=None:
            await sio.emit(to=self.opponent.sid, event="opponentQuit")
            self.opponent.beatOpponent()
            self.opponent.clearGame()
            self.clearGame()


# Unit Tests
if __name__ == "__main__":
    #Player.resetTable()
    Player.startTable()
    
    assert str(Player.create("shahrose", "SuperSecretPass")) == "<Player:shahrose:1>"
    assert str(Player.create("person", "SuperSecretPass")) == "<Player:person:2>"

    assert Player.create("shahrose", "SuperSecretPass") == "User already exists"
    assert Player.create("Raúl", "123456") == "Username must be alphanumeric"
    
    assert str(Player.fetch("shahrose", "SuperSecretPass")) == "<Player:shahrose:1>"
    assert Player.fetch("faker") == "User does not exist"
    assert Player.fetch("shahrose", "WrongPassword") == "Password is incorrect"

    print("All <Player> Unit Tests Passed!")