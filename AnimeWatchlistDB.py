import mysql.connector 

class Database(): 
    
    def __init__(self): 
        self.LOCALSERVER = mysql.connector.connect(
            host='localhost',
            user='root',
            password='Yamahapsre443',
            database="AnimeWatchlist"
        )
        self.cursor = self.LOCALSERVER.cursor()

    """ Table Creators """
    def createTableCurrentSeason(self): 
        self.cursor.execute("CREATE TABLE CurrentSeason (id INT AUTO_INCREMENT PRIMARY KEY, Name VARCHAR(255), Season VARCHAR(255), Status VARCHAR(255), Genre VARCHAR(255), Source VARCHAR(255))")
    def createTableFinished(self): 
        self.cursor.execute("CREATE TABLE Finished (id INT AUTO_INCREMENT PRIMARY KEY, Name VARCHAR(255), Season VARCHAR(255), Genre VARCHAR(255), Picture VARCHAR(255))")
    def createTableWatchlist(self, name): 
        self.cursor.execute("CREATE TABLE {} (id INT AUTO_INCREMENT PRIMARY KEY, Name VARCHAR(255), Season VARCHAR(255), Status VARCHAR(255), Genre VARCHAR(255), CurrentEpisode TINYINT, Picture VARCHAR(255))".format(name))

    """ Update Tables """
    def updateCurrentSeasonTable(self, animeData): 
        pass
    def updateFinishedTable(self): 
        pass 
    def updateWatchlistTable(self): 
        pass

    """ Add/removes to/from Watchlists """ 
    def addToWatchlist(self, name, animecard): 
        sql = "INSERT INTO {} (Name, Season, Status, Genre, CurrentEpisode, Picture) VALUES (%s, %s, %s, %s, %s)".format(name)
        vals = (
            animecard.name, 
            animecard.season, 
            animecard.status, 
            animecard.genre, 
            animecard.currentep, 
            animecard.pictureurl
        )
        self.cursor.execute(sql, vals)
        self.LOCALSERVER.commit()

    def removeFromWatchlist(self, name, animename): 
        sql = "DELETE FROM {} WHERE Name = %s".format(name)
        val = (animename, )
        self.cursor.execute(sql, val)
        self.LOCALSERVER.commit()

    def addToFinished(self, animecard): 
        sql = "INSERT INTO Finished (Name, Season, Genre, Picture) VALUES (%s, %s, %s, %s)"
        vals = (
            animecard.name, 
            animecard.season,
            animecard.genre,
            animecard.pictureurl
        )
        self.cursor.execute(sql, vals)
        self.LOCALSERVER.commit()

    def removeFromFinished(self, animename): 
        sql = "DELETE FROM Finished WHERE Name = %s"
        val = (animename,)
        self.cursor.execute(sql, val)
        self.LOCALSERVER.commit()

    """ Filter Tables """ 
    def filterByGenre(self, watchlist, genre): 
        pass
    
    