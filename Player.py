from SQLITE import querySQL
from trueskill import Rating, rate_1vs1, quality_1vs1
import bcrypt

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
            'partner VARCHAR(64) DEFAULT NULL'
            ");"
        ))

    # see if player exists / return it
    @classmethod
    def verify(cls, username, plainPassword):
        result = querySQL("SELECT * FROM players WHERE username = ? LIMIT 1", username)
        if len(result)==0:
            False, "User does not exist."
        if not bcrypt.checkpw(plainPassword, result["password"]):
            False, "Password is incorrect."
        return True, cls(result)

    # Create Player in database
    @classmethod
    def create(cls, username, plainPassword):
        hashPassword = bcrypt.hashpw(plainPassword, bcrypt.gensalt())
        query = "INSERT INTO players (username, password) VALUES (?,?);"
        pid = querySQL(query, username, hashPassword)
        print(pid)

    # constructor
    def __init__(self, result):
        self.__id = result["id"]
        self.__username = result['username']
        self.__hashPassword = result['password']
        self.__rating = Rating(result['skillMu'], result['skillSigma'])
        self.__sid = result['sid']
        self.__partner = result['partner']

    def __repr__(self):
        return f"<Player:{self.username}:{self.id}>"

    def print(self):
        self.qprint("Self")
        if partner!=None:
            self.partner.qprint("Partner")

    def qprint(self, label):
        print("{label:<10}: {self.username:<20} ({self.rating.mu:.0f}, {self.rating.sigma:.2f})")
        print("          {self.sid}")
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
    def password(self): return self.__hashPassword

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

    # see matchmaking compatability
    def getCompatability(self, otherPlayer):
        quality_1vs1(self.rating, otherPlayer.rating)

    # have this player win (defeat another player)
    def defeatPlayer(self, losingPlayer):
        self.rating, losingPlayer.rating = rate_1vs1(self.rating, losingPlayer.rating)



# initialize Tables
if __name__ == "__main__":
    Player.initTable()    
    Player.create("shahrose", "SuperSecretPass")
    print( Player.verify("shahrose", "SuperSecretPass")[1] )
