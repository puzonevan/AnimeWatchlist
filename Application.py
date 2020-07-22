""" Main Application """ 
"""
    Desktop application to personally track and watchlist of anime
"""

""" Imports """
import tkinter as tk, json
import AnimeWatchlistUI as mainpage
import AnimeWatchlistDB as db
# Debug 
import pprint, time

def main(): 

    """ Retrieve data from SQL and format """
    database = db.Database()

    """ Retrieve data from json file and format"""
    animeData = db.AnimeData().data

    """ Run Tkinter Object Oriented Application """
    root = tk.Tk()
    root.geometry("1000x600")
    root.title('AnimeWatchlist')

    tk.Grid.rowconfigure(root, 0, weight=1)
    tk.Grid.columnconfigure(root, 0, weight=0)
    tk.Grid.columnconfigure(root, 1, weight=1)

    mainpage.database = database 
    mainpage.dbData = database.loadDatabase()
    mainpage.animeData = animeData
    mainpage.AnimeWatchlistUI(root, database, database.loadDatabase(), animeData)

    root.mainloop()
    
main()