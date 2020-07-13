import mysql.connector 
import AnimeCard

""" CONSTANTS """
SEASON = 'SUMMER'
YEAR = '2020'

class Database(): 
    
    def __init__(self): 
        self.LOCALSERVER = mysql.connector.connect(
            host='localhost',
            user='root',
            password='Yamahapsre443',
            database="AnimeWatchlist"
        )
        self.cursor = self.LOCALSERVER.cursor()

    """ Loading Data """
    def loadDatabase(self): 
        output = {}
        self.cursor.execute("SHOW TABLES")
        tables = []

        # Get names of tables
        for (table,) in self.cursor: 
            tables.append(table,)

        # Put all data from each table
        for table in tables: 
            sql = "SELECT * FROM {}".format(table)
            self.cursor.execute(sql)
            output[table] = self.cursor.fetchall()

        # Format output
        for category in output.keys(): 
            categoryanime = []
            for anime in output.get(category): 
                card = AnimeCard.AnimeCard(anime, category)
                categoryanime.append(card)
            output[category] = categoryanime
        
        return output

    """ Table Creators """
    def createTableCurrentSeason(self): 
        self.cursor.execute("CREATE TABLE CurrentSeason (id INT AUTO_INCREMENT PRIMARY KEY, Name VARCHAR(255), Season VARCHAR(255), Status VARCHAR(255), Genre VARCHAR(255), Source VARCHAR(255))")
    def createTableFinished(self): 
        self.cursor.execute("CREATE TABLE Finished (id INT AUTO_INCREMENT PRIMARY KEY, Name VARCHAR(255), Season VARCHAR(255), Genre VARCHAR(255), Picture VARCHAR(255))")
    def createTableWatchlist(self, name): 
        self.cursor.execute("CREATE TABLE {} (id INT AUTO_INCREMENT PRIMARY KEY, Name VARCHAR(255), Season VARCHAR(255), Status VARCHAR(255), Genre VARCHAR(255), CurrentEpisode TINYINT, Picture VARCHAR(255))".format(name))

    """ Update Tables """
    def updateCurrentSeasonTable(self, animeData): 

        # Drop current table: 
        self.cursor.execute('DROP TABLE CurrentSeason')

        # Create new table: 
        self.createTableCurrentSeason()

        # Filter method based on season and year
        def filterCurrentSeason(animeData): 
            output = []
            for anime in animeData: 
                if anime.get('animeSeason').get('season') == SEASON and str(anime.get('animeSeason').get('year')) == YEAR:
                    output.append(anime)
            return output 
        filteredanime = filterCurrentSeason(animeData)

        # Add each anime from the filtered data to the table
        for anime in filteredanime: 
            title = ' '
            genre = ' '
            if 'synonym' in anime.keys(): 
                title = anime.get('synonym')[0]
            else: 
                title = anime.get('title')

            if 'tags' in anime.keys() and len(anime.get('tags')) > 0: 
                genre = anime.get('tags')[0]

            season = anime.get('animeSeason').get('season') + ' ' + str(anime.get('animeSeason').get('year'))
            sql = "INSERT INTO CurrentSeason (Name, Season, Status, Genre, Source) VALUES (%s, %s, %s, %s, %s)"
            vals = (
                title,
                season, 
                anime.get('status'), 
                genre,
                anime.get('sources')[0]
            )
        self.cursor.execute(sql, vals)
        self.LOCALSERVER.commit()

    def updateFinishedTable(self): 
        pass 
    def updateWatchlistTable(self): 
        pass

    """ Add/removes to/from Watchlists """ 
    def addToWatchlist(self, name, animecard): 
        sql = "INSERT INTO {} (Name, Season, Status, Genre, CurrentEpisode, Picture) VALUES (%s, %s, %s, %s, %s, %s)".format(name)
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
    
    