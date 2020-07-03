""" Main Application """ 
"""
    Desktop application that is a personal tracker and watchlist of anime
"""

""" Imports """
import AnimeCard, Finished, Season, Watchlist
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


""" Button Methods """ 
def displayCurrentSeason(): 
    pass

def displayWatchlist(): 
    pass

def displayFinished():
    pass

""" Frame Methods """ 
def raiseframe(frame): 
    frame.tkraise()

""" AnimeCard Methods """ 
def createAnimeCard(parentframe, row, col): 

    # AnimeCard Frame
    animeCard = tk.Frame(
        master=parentframe, 
        width=140, height=170, 
        bg='white'
    )
    animeCard.grid(row=row, column=col, padx=5, pady=5)

    # Anime Information 
    picture = tk.Label(animeCard, text='Insert Picture Here')
    name = tk.Label(animeCard, text='Kaguya Sama: Love is War')
    season = tk.Label(animeCard, text='Spring 2020')
    genre = tk.Label(animeCard, text='Romantic Comedy')

    # Grid Information 
    picture.grid(row=0, column=0, rowspan=3, columnspan=2)
    name.grid(row=3, column=0, columnspan=2)
    season.grid(row=4, column=0)
    genre.grid(row=4, column=1)


def runApplication(data): 
    
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
    createAnimeCard(currentseasonframe, 0, 0)
    createAnimeCard(currentseasonframe, 0, 1)
    createAnimeCard(currentseasonframe, 0, 2)
    createAnimeCard(currentseasonframe, 0, 3)

    # Frame 2: Watchlist 
    watchlistframe = tk.Frame(master=root, bg='blue')
    watchlistframe.grid(row=0, column=1, sticky="nswe")

    # Frame 3: Finished
    finishedframe = tk.Frame(master=root, bg='yellow')
    finishedframe.grid(row=0, column=1, sticky="nswe")

    # Left Sidebar 
    leftsidebar = tk.Frame(master=root, bg='gray')
    leftsidebar.grid(row=0, column=0, sticky="nsw")

    # Categories for Left Sidebar
    currentseason = tk.Button(leftsidebar, text='Current Season', command=lambda: raiseframe(currentseasonframe))
    currentseason.grid(row=0, column=0)

    watchlist1 = tk.Button(leftsidebar, text='Watchlist1', command=lambda: raiseframe(watchlistframe))
    watchlist1.grid(row=1, column=0)

    archived = tk.Button(leftsidebar, text='Finished', command=lambda: raiseframe(finishedframe))
    archived.grid(row=2, column=0)


    # Top of Main Contents: Searchbar and filter
    # searchbar = tk.Entry(maincontents)
    # searchbar.grid(row=0, column=0, columnspan=3)

    # filterbutton = tk.Button(maincontents, text='icon here')
    # filterbutton.grid(row=0, column=3)
    
    root.mainloop()

def main(): 
    data = loadDatabase()
    runApplication(data)
main()