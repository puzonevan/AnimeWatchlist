""" Main Application """ 
"""
    Desktop application to personally track and watchlist of anime
"""

""" Imports """
import AnimeCard, Season, Finished, Watchlist
import json
import tkinter as tk 
from tkinter import ttk 
import mysql.connector
import pprint

""" Setup Database Connection """
LOCALSERVER = mysql.connector.connect(
    host='localhost',
    user='root',
    password='Yamahapsre443', 
    database="AnimeWatchlist"
)
cursor = LOCALSERVER.cursor()

""" Create AnimeDatabase """
""" Uncomment if database does not exist """
# cursor.execute("CREATE DATABASE AnimeWatchlist")
""" Create Tables """
""" Uncomment if tables do not exist """ 
# Table 1: Current Season
# cursor.execute("CREATE TABLE CurrentSeason (id INT AUTO_INCREMENT PRIMARY KEY, Name VARCHAR(255), Season VARCHAR(255), Status VARCHAR(255), Genre VARCHAR(255), Picture VARCHAR(255))")
# Table 2: Default Watchlist
# cursor.execute("CREATE TABLE Watchlist (id INT AUTO_INCREMENT PRIMARY KEY, Name VARCHAR(255), Season VARCHAR(255), Status VARCHAR(255), Genre VARCHAR(255), CurrentEpisode TINYINT, Picture VARCHAR(255))")
# Table 3: Finished 
# cursor.execute("CREATE TABLE Finished (id INT AUTO_INCREMENT PRIMARY KEY, Name VARCHAR(255), Season VARCHAR(255), Genre VARCHAR(255), Picture VARCHAR(255))")

""" Loading Database Method """
""" return a dictionary with table name containing a list of anime """ 
""" Example: { 'Watchlist1': [(1, 'Anime1', ...), (2, 'Anime2', ...)]} """
def loadDatabase(): 
    output = {}
    cursor.execute("SHOW TABLES")
    tables = []
    for (table,) in cursor: 
        tables.append(table,)

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
        

""" createCategories Method """
def createCategories(data): 
    output = [] 
    for category in data.keys(): 
        if category == 'CurrentSeason': 
            currentseason = Season.Season('Spring', '2020', data.get(category))
            output.append(currentseason)
        elif category == 'Finished': 
            finished = Finished.Finished(data.get(category))
            output.append(finished)
        else: 
            watchlist = Watchlist.Watchlist('Watchlist', data.get(category))
            output.append(watchlist)

    return output


""" Table Methods """
def createNewWatchlist(name): 
    cursor.execute("CREATE TABLE {} (id INT AUTO_INCREMENT PRIMARY KEY, Name VARCHAR(255), Season VARCHAR(255), Status VARCHAR(255), Genre VARCHAR(255), CurrentEpisode TINYINT, Picture VARCHAR(255))".format(name))

def updateCurrentSeason(): 
    pass

def addToWatchlist(): 
    pass

def removeFromWatchlist(): 
    pass

def addToFinished(): 
    pass

def removeFromFinished(): 
    pass


""" Frame Methods """ 
def raiseframe(frame): 
    frame.tkraise()

""" AnimeCard Methods """ 
def createAnimeCard(animeCard, parentframe, row, col): 

    # AnimeCard Frame
    animeCardFrame = tk.Frame(
        master=parentframe, 
        width=140, height=170, 
        bg='white'
    )
    animeCardFrame.grid(row=row, column=col, padx=5, pady=5)

    # Anime Information 
    picture = tk.Label(animeCardFrame, text='Insert Picture Here')
    name = tk.Label(animeCardFrame, text=animeCard.name)
    season = tk.Label(animeCardFrame, text=animeCard.season)
    genre = tk.Label(animeCardFrame, text=animeCard.genre)

    # Grid Information 
    picture.grid(row=0, column=0, rowspan=3, columnspan=2)
    name.grid(row=3, column=0, columnspan=2)
    season.grid(row=4, column=0)
    genre.grid(row=4, column=1)

def runApplication(data): 

    # Row and Column
    row = 0
    column = 0
    # Create CurrentSeason, Finished, and Watchlist Objects 
    categories = createCategories(data)
            
    # GUI 
    root = tk.Tk()
    root.title('Anime Watchlist')
    root.geometry("800x500")
    tk.Grid.rowconfigure(root, 0, weight=1)
    tk.Grid.columnconfigure(root, 0, weight=0)
    tk.Grid.columnconfigure(root, 1, weight=1)

    # Frame 1: Current Season 
    currentseasonframe = tk.Frame(master=root, bg='red')
    currentseasonframe.grid(row=0, column=1, sticky="nswe")
    for animeCard in categories[0].anime: 
        createAnimeCard(animeCard, currentseasonframe, row, column)
        column += 1
        if column == 3:
            column = 0
            row += 1
    row = 0 
    column = 0

    # Frame 2: Finished
    finishedframe = tk.Frame(master=root, bg='yellow')
    finishedframe.grid(row=0, column=1, sticky="nswe")
    for animeCard in categories[1].anime: 
        createAnimeCard(animeCard, finishedframe, row, column)
        column += 1
        if column == 3:
            column = 0
            row += 1
    row = 0 
    column = 0

    # Frame 3: Watchlist 
    watchlistframe = tk.Frame(master=root, bg='blue')
    watchlistframe.grid(row=0, column=1, sticky="nswe")
    for animeCard in categories[2].anime: 
        createAnimeCard(animeCard, watchlistframe, row, column)
        column += 1
        if column == 3:
            column = 0
            row += 1
    row = 0 
    column = 0


    

    """ Left SideBar Frame """
    leftsidebar = tk.Frame(master=root, bg='gray')
    leftsidebar.grid(row=0, column=0, sticky="nsw")

    """ Left Sidebar Buttons"""
    # Add Watchlist Button
    addWatchlist = tk.Button(leftsidebar, text='Add Watchlist')
    addWatchlist.grid(row=0, column=0)

    # Current Season Category 
    currentseason = tk.Button(leftsidebar, text='Current Season', command=lambda: raiseframe(currentseasonframe))
    currentseason.grid(row=1, column=0)
    # Finished Category
    finished = tk.Button(leftsidebar, text='Finished', command=lambda: raiseframe(finishedframe))
    finished.grid(row=2, column=0)
    # Each Watchlist Category
    watchlist1 = tk.Button(leftsidebar, text='Watchlist1', command=lambda: raiseframe(watchlistframe))
    watchlist1.grid(row=3, column=0)
    


    root.mainloop()

def main(): 
    data = formatdata(loadDatabase())
    runApplication(data)
main()