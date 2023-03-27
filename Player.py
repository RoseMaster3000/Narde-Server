from database import querySQL
from trueskill import Rating, rate_1vs1, quality_1vs1
import bcrypt
ALPHANUM = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890"


class Player:
    # create Player user table (sqlite) 
    @staticmethod
    def initTable():
        querySQL("DROP TABLE IF EXISTS players;")
        querySQL((
            "CREATE TABLE players ("
            "id INTEGER PRIMARY KEY,"
            "username VARCHAR(64) UNIQUE NOT NULL,"
            "password VARCHAR(64) NOT NULL,"
            "skillMu REAL DEFAULT 25.000,"
            "skillSigma REAL DEFAULT 8.333,"
            "sid VARCHAR(64) DEFAULT NULL,"
            "partner VARCHAR(64) DEFAULT NULL"
            ");"
        ))

    # Fetch Player from database (also validates password if provided)
    # if search fails, returns error <String>
    @classmethod
    def fetch(cls, username, plainPassword=None):
        result = querySQL("SELECT * FROM players WHERE username = ? LIMIT 1", username)
        if result==None:
            return "User does not exist"
        if plainPassword!=None and not bcrypt.checkpw(plainPassword, result["password"]):
            return "Password is incorrect"
        return cls(result)

    # Create/Fetch Player in database
    # if creation fails, returns error <String>
    @staticmethod
    def create(username, plainPassword):
        if any([(char not in ALPHANUM) for char in username]):
            return "Username must be alphanumeric"
        if type(Player.fetch(username))==Player:
            return "User already exists"
        hashPassword = bcrypt.hashpw(plainPassword, bcrypt.gensalt())
        query = "INSERT INTO players (username, password) VALUES (?,?);"
        pid = querySQL(query, username, hashPassword)
        return Player.fetch(username, plainPassword)

    def __init__(self, dbDict):
        self.__id = dbDict["id"]
        self.__username = dbDict['username']
        self.__hashPassword = dbDict['password']
        self.__rating = Rating(dbDict['skillMu'], dbDict['skillSigma'])
        self.__sid = dbDict['sid']
        self.__partner = dbDict['partner']

    def __repr__(self):
        return str(self)

    def __str__(self):
        return f"<Player:{self.username}:{self.id}>"

    def print(self):
        self.printTable()
        if self.partner!=None:
            self.partner.printTable(False)

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
        self.__hashPassword = bcrypt.hashpw(value, bcrypt.gensalt())
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
    def sid(self): return self.__sid
    @sid.setter
    def sid(self, value):
        self.__sid = value
        querySQL("UPDATE players SET sid = ? WHERE id = ?", self.sid, self.id)    

    @property
    def partner(self): return self.__partner
    @partner.setter
    def partner(self, value):
        self.__partner = value
        querySQL("UPDATE players SET partner = ? WHERE id = ?", self.partner, self.id)    

    #####################
    # MATCHMAKING
    #####################

    # see matchmaking compatability (0 ~ 1, higher the better)
    def getCompatability(self, otherPlayer):
        return quality_1vs1(self.rating, otherPlayer.rating)

    # have this player win (defeat another player)
    def defeatPlayer(self, losingPlayer):
        self.rating, losingPlayer.rating = rate_1vs1(self.rating, losingPlayer.rating)


# Unit Tests
if __name__ == "__main__":
    Player.initTable()    
    assert str(Player.create("shahrose", "SuperSecretPass")) == "<Player:shahrose:1>"
    assert str(Player.create("person", "SuperSecretPass")) == "<Player:person:2>"
    
    assert Player.create("shahrose", "SuperSecretPass") == "User already exists"
    assert Player.create("Raúl", "123456") == "Username must be alphanumeric"

    assert str(Player.fetch("shahrose", "SuperSecretPass")) == "<Player:shahrose:1>"
    assert Player.fetch("faker") == "User does not exist"
    assert Player.fetch("shahrose", "WrongPassword") == "Password is incorrect"

    print("All <Player> Unit Tests Passed!")
