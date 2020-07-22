import mysql.connector, json
import AnimeCard

""" CONSTANTS """
SEASON = 'SUMMER'
YEAR = '2020'

class Database(): 
    
    """ Constructor """
    def __init__(self): 
        self.LOCALSERVER = mysql.connector.connect(
            host='localhost',
            user='root',
            password='Yamahapsre443',
            database="AnimeWatchlist"
        )
        self.cursor = self.LOCALSERVER.cursor()

    """ loadDatabase method - retrieves data from database """
    def loadDatabase(self): 

        self.cursor.execute("SHOW TABLES")
        output = {}
        tables = []

        # Get names of tables
        for (table,) in self.cursor: 
            tables.append(table,)

        # Put all data from each table
        for table in tables: 
            sql = "SELECT * FROM {}".format(table)
            self.cursor.execute(sql)
            output[table] = self.cursor.fetchall()

        # Format output as AnimeCards 
        for category in output.keys(): 
            categoryanime = []
            for anime in output.get(category): 
                card = AnimeCard.AnimeCard(anime, category)
                categoryanime.append(card)
            output[category] = categoryanime
        
        return output

    """ Table creation/destroy methods - create given tables in database """
    def createTableCurrentSeason(self): 
        self.cursor.execute("CREATE TABLE CurrentSeason (id INT AUTO_INCREMENT PRIMARY KEY, Name VARCHAR(255), Season VARCHAR(255), Status VARCHAR(255), Genre VARCHAR(255), Source VARCHAR(255), Picture VARCHAR(255))")
    def createTableFinished(self): 
        self.cursor.execute("CREATE TABLE Finished (id INT AUTO_INCREMENT PRIMARY KEY, Name VARCHAR(255), Season VARCHAR(255), Genre VARCHAR(255), Picture VARCHAR(255))")
    def createTableWatchlist(self, name): 
        sql = "CREATE TABLE {} (id INT AUTO_INCREMENT PRIMARY KEY, Name VARCHAR(255), Season VARCHAR(255), Status VARCHAR(255), Genre VARCHAR(255), CurrentEpisode TINYINT, Picture VARCHAR(255))".format(name)
        self.cursor.execute(sql)

    def destroyTable(self, name): 
        sql = "DROP TABLE IF EXISTS {}".format(name)
        self.cursor.execute(sql)

    """ Update table methods """
    def updateCurrentSeasonTable(self, animeData): 

        # Drop current table: 
        self.cursor.execute('DROP TABLE CurrentSeason')

        # Create new table: 
        self.createTableCurrentSeason()

        # Filter method based on season and year
        filteredanime = [] 
        for anime in animeData: 
            if anime.get('season') == "{} {}".format(SEASON, YEAR): 
                filteredanime.append(anime)

        # Add each anime from the filtered data to the table
        for anime in filteredanime: 
            sql = "INSERT INTO CurrentSeason (Name, Season, Status, Genre, Source, Picture) VALUES (%s, %s, %s, %s, %s, %s)"
            vals = (
                anime.get('name'),
                anime.get('season'), 
                anime.get('status'), 
                anime.get('genres')[0],
                anime.get('source'),
                anime.get('pictureurl'),
            )
            self.cursor.execute(sql, vals)
            self.LOCALSERVER.commit()

    """ Get Content from tables """ 
    def getWatchlistTable(self, watchlist): 
        sql = "SELECT * FROM {}".format(watchlist)
        self.cursor.execute(sql)
        return self.cursor.fetchall()

    """ Add/removes to/from watchlist tables """ 
    def addToWatchlist(self, name, animecard): 
        sql = "INSERT INTO {} (Name, Season, Status, Genre, CurrentEpisode, Picture) VALUES (%s, %s, %s, %s, %s, %s)".format(name)
        vals = (
            animecard.name, 
            animecard.season, 
            animecard.status, 
            animecard.genre, 
            animecard.currentep, 
            animecard.pictureurl,
        )
        self.cursor.execute(sql, vals)
        self.LOCALSERVER.commit()

    def removeFromWatchlist(self, name, animename): 
        sql = "DELETE FROM {} WHERE Name = %s".format(name)
        val = (animename, )
        self.cursor.execute(sql, val)
        self.LOCALSERVER.commit()

    def addToFinished(self, animecard): 
        sql = "INSERT IGNORE INTO Finished (Name, Season, Genre, Picture) VALUES (%s, %s, %s, %s)"
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
    def filterByGenre(self, watchlist): 
        sql = "SELECT * FROM {} ORDER BY Genre".format(watchlist)
        self.cursor.execute(sql)
        return self.cursor.fetchall()

    def filterByAlpha(self, watchlist):
        sql = "SELECT * FROM {} ORDER BY Name".format(watchlist)
        self.cursor.execute(sql)
        return self.cursor.fetchall()

    def filterBySeason(self, watchlist): 
        sql = "SELECT * FROM {} ORDER BY Season".format(watchlist)
        self.cursor.execute(sql)
        return self.cursor.fetchall()
    

    """ Create Anime Cards """ 
    def createAnimeCard(self, anime, category): 
        return AnimeCard.AnimeCard(anime, category)

    def createAnimeCards(self, filtereddata, category): 
        output = []
        for anime in filtereddata: 
            output.append(AnimeCard.AnimeCard(anime, category))
        return output


class AnimeData(): 

    """ Constructor """ 
    def __init__(self): 
        self.data = self.loadAnimeData()

    """ loadAnimeData method """
    def loadAnimeData(self): 
        jsonFile = open('./anime-offline-database-master/anime-offline-database.json')
        animeData = json.load(jsonFile).get('data')
        jsonFile.close()

        output = []
        # Format 
        for anime in animeData: 
            filteredanime = {}
            filteredanime['name'] = anime.get('title')
            filteredanime['type'] = anime.get('type')
            filteredanime['episodecount'] = anime.get('episodes')
            filteredanime['genres'] = anime.get('tags')
            filteredanime['status'] = anime.get('status')
            filteredanime['synonyms'] = anime.get('synonyms')
            filteredanime['season'] = "{} {}".format(anime.get('animeSeason').get('season'), anime.get('animeSeason').get('year'))
            filteredanime['source'] = anime.get('sources')[0]
            filteredanime['pictureurl'] = anime.get('picture')
            filteredanime['epcount'] = anime.get('episodes')

            output.append(filteredanime)
        return output
    