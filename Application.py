""" Main Application """ 
"""
    Desktop application to personally track and watchlist of anime
"""

""" Imports """
import AnimeCard, Season, Finished, Watchlist
import json
import tkinter as tk 
import mysql.connector
import pprint, time
import AnimeWatchlistUI as mainpage

""" Setup Database Connection """
LOCALSERVER = mysql.connector.connect(
    host='localhost',
    user='root',
    password='Yamahapsre443', 
    database="AnimeWatchlist"
)
cursor = LOCALSERVER.cursor()

""" CONSTANTS """
SEASON = 'SUMMER'
YEAR = '2020'

""" Create AnimeDatabase """
""" Uncomment if database does not exist """
# cursor.execute("CREATE DATABASE AnimeWatchlist")

""" Create Tables """
# Table 1: Current Season
def createTableCurrentSeason(): 
    cursor.execute("CREATE TABLE CurrentSeason (id INT AUTO_INCREMENT PRIMARY KEY, Name VARCHAR(255), Season VARCHAR(255), Status VARCHAR(255), Genre VARCHAR(255), Source VARCHAR(255))")
# Table 2: Default Watchlist
def createTableWatchlist(name): 
    cursor.execute("CREATE TABLE {} (id INT AUTO_INCREMENT PRIMARY KEY, Name VARCHAR(255), Season VARCHAR(255), Status VARCHAR(255), Genre VARCHAR(255), CurrentEpisode TINYINT, Picture VARCHAR(255))".format(name))
# Table 3: Finished 
def createTableFinished(): 
    cursor.execute("CREATE TABLE Finished (id INT AUTO_INCREMENT PRIMARY KEY, Name VARCHAR(255), Season VARCHAR(255), Genre VARCHAR(255), Picture VARCHAR(255))")

""" Loading Database Method """
""" return a dictionary with table name containing a list of anime """ 
""" Example: { 'Watchlist1': [(1, 'Anime1', ...), (2, 'Anime2', ...)]} """
def loadDatabase(): 
    output = {}
    cursor.execute("SHOW TABLES")
    tables = []

    # Get names of tables
    for (table,) in cursor: 
        tables.append(table,)

    # Put all data from each table
    for table in tables: 
        sql = "SELECT * FROM {}".format(table)
        cursor.execute(sql)
        output[table] = cursor.fetchall()
    return output

""" formatData Method """
def formatdata(data): 
    
    for category in data.keys(): 
        categoryanime = []
        for anime in data.get(category): 
            card = AnimeCard.AnimeCard(anime, category)
            categoryanime.append(card)
        data[category] = categoryanime
        
    return data
        
""" loadAnimeData method """
def loadAnimeData(): 
    jsonFile = open('./anime-offline-database-master/anime-offline-database.json')
    animeData = json.load(jsonFile).get('data')
    jsonFile.close()
    return animeData

""" createCategories Method """
def createCategories(data): 
    output = [] 
    for category in data.keys(): 
        if category == 'CurrentSeason': 
            currentseason = Season.Season(SEASON, YEAR, data.get(category))
            output.append(currentseason)
        elif category == 'Finished': 
            finished = Finished.Finished(data.get(category))
            output.append(finished)
        else: 
            watchlist = Watchlist.Watchlist('Watchlist', data.get(category))
            output.append(watchlist)
    
    return output

def updateCurrentSeason(animeData): 

    # Drop current table: 
    cursor.execute('DROP TABLE CurrentSeason')

    # Create new table: 
    createTableCurrentSeason()

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
        cursor.execute(sql, vals)
        LOCALSERVER.commit()


def addToWatchlist(watchlist, animeCard): 
    sql = "INSERT INTO {} (Name, Season, Status, Genre, CurrentEpisode, Picture) VALUES (%s, %s, %s, %s, %s)".format(watchlist)
    vals = (
        animeCard.name, 
        animeCard.season, 
        animeCard.status, 
        animeCard.genre, 
        animeCard.currentep, 
        animeCard.pictureurl
    )
    cursor.execute(sql, vals)
    LOCALSERVER.commit()

def removeFromWatchlist(watchlist, animename): 
    sql = "DELETE FROM {} WHERE Name = %s".format(watchlist)
    val = (animename, )
    cursor.execute(sql, val)
    LOCALSERVER.commit()

def addToFinished(animeCard): 
    sql = "INSERT INTO Finished (Name, Season, Genre, Picture) VALUES (%s, %s, %s, %s)"
    vals = (
        animeCard.name, 
        animeCard.season,
        animeCard.genre,
        animeCard.pictureurl
    )
    cursor.execute(sql, vals)
    LOCALSERVER.commit()

def removeFromFinished(animename): 
    sql = "DELETE FROM Finished WHERE Name = %s"
    val = (animename,)
    cursor.execute(sql, val)
    LOCALSERVER.commit()


""" AnimeCard Methods """ 
def createAnimeCard(animeCard, parentframe, row, col): 

    # AnimeCard Frame
    animeCardFrame = tk.Frame(
        master=parentframe,  
        padx=10, pady=10, 
        bg='#242629'
    )
    animeCardFrame.grid(row=row, column=col, padx=5, pady=5, sticky='nesw')

    # Anime Information 
    name = tk.Message(animeCardFrame, text=animeCard.name, width=200, fg='#fffffe', bg='#242629')
    season = tk.Label(animeCardFrame, text=animeCard.season, fg='#94a1b2', bg='#242629')
    genre = tk.Label(animeCardFrame, text=animeCard.genre, fg='#94a1b2', bg='#242629')
    def removeClick(): 
        if parentframe._name == '!frame':
            removeFromWatchlist('CurrentSeason', animeCard.name)
            animeCardFrame.destroy()
        elif parentframe._name == '!frame2': 
            removeFromFinished(animeCard.name)
            animeCardFrame.destroy()
    removeButton = tk.Button(animeCardFrame, text='remove', highlightbackground='#242629', command=removeClick)

    # Grid Information 
    name.grid(row=0, column=0, columnspan=3)
    genre.grid(row=1, column=0, columnspan=3)
    season.grid(row=2, column=0, columnspan=2)
    removeButton.grid(row=2, column=2)

def runApplication(data, animeData): 

    # Row and Column
    row = 0
    column = 0
    # Create CurrentSeason, Finished, and Watchlist Objects 
    categories = createCategories(data)
            
    # GUI 
    root = tk.Tk()
    root.title('Anime Watchlist')
    root.geometry("930x520")
    tk.Grid.rowconfigure(root, 0, weight=1)
    tk.Grid.columnconfigure(root, 0, weight=0)
    tk.Grid.columnconfigure(root, 1, weight=1)

    # Frame 1: Current Season 
    currentseasonframe = tk.Frame(master=root, bg='#16161a')
    currentseasonframe.grid(row=0, column=1, sticky="nswe")
    start = 0
    for animeCard in categories[0].anime[start:start+16]: 
        createAnimeCard(animeCard, currentseasonframe, row, column)
        column += 1
        if column == 4:
            column = 0
            row += 1
    row = 0 
    column = 0

    # Frame 2: Finished
    finishedframe = tk.Frame(master=root, bg='#16161a')
    finishedframe.grid(row=0, column=1, sticky="nswe")
    for animeCard in categories[1].anime: 
        createAnimeCard(animeCard, finishedframe, row, column)
        column += 1
        if column == 4:
            column = 0
            row += 1
    row = 0 
    column = 0

    # Frame 3: Watchlist 
    watchlistframe = tk.Frame(master=root, bg='#16161a')
    watchlistframe.grid(row=0, column=1, sticky="nswe")
    for animeCard in categories[2].anime: 
        createAnimeCard(animeCard, watchlistframe, row, column)
        column += 1
        if column == 4:
            column = 0
            row += 1
    row = 0 
    column = 0


    """ Left SideBar Frame """
    leftsidebar = tk.Frame(master=root, bg='#242629', padx=15)
    leftsidebar.grid(row=0, column=0, sticky="nsw")

    """ Left Sidebar Buttons"""
    # Add Watchlist Button
    addWatchlist = tk.Button(leftsidebar, text='Add Watchlist', highlightbackground='#242629')
    addWatchlist.grid(row=0, column=0)

    """ raiseframe method """ 
    def raiseframe(frame): 
        frame.tkraise()
    # Current Season Category 
    currentseason = tk.Button(leftsidebar, text='Current Season', highlightbackground='#242629', command=lambda: raiseframe(currentseasonframe))
    currentseason.grid(row=1, column=0)
    # Finished Category
    finished = tk.Button(leftsidebar, text='Finished', highlightbackground='#242629', command=lambda: raiseframe(finishedframe))
    finished.grid(row=2, column=0)
    # Each Watchlist Category
    watchlist1 = tk.Button(leftsidebar, text='Watchlist1', highlightbackground='#242629', command=lambda: raiseframe(watchlistframe))
    watchlist1.grid(row=3, column=0)

    root.mainloop()

def main(): 

    """ Setup saved data from Database """
    databaseData = formatdata(loadDatabase())

    """ Setup anime data from json file """
    animeData = loadAnimeData()
    
    """ Update Current Season """
    # updateCurrentSeason(animeData)

    """ Run Object Oriented Application """
    root = tk.Tk()
    root.geometry("930x520")
    root.title('AnimeWatchlist')
    tk.Grid.rowconfigure(root, 0, weight=1)
    tk.Grid.columnconfigure(root, 0, weight=0)
    tk.Grid.columnconfigure(root, 1, weight=1)
    mainpage.AnimeWatchlistUI(root, databaseData,animeData)
    root.mainloop()
    
main()