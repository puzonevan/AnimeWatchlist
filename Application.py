""" Main Application """ 
"""
    Desktop application to personally track and watchlist of anime
"""

""" Imports """
import AnimeCard, Season, Finished, Watchlist
import tkinter as tk, json
import AnimeWatchlistUI as mainpage
import AnimeWatchlistDB as db
# Debug 
import pprint, time

        
""" loadAnimeData method """
def loadAnimeData(): 
    jsonFile = open('./anime-offline-database-master/anime-offline-database.json')
    animeData = json.load(jsonFile).get('data')
    jsonFile.close()
    return animeData


def main(): 

    """ Setup saved data from Database """
    database = db.Database()

    """ Setup anime data from json file """
    animeData = loadAnimeData()

    """ Run Object Oriented Application """
    root = tk.Tk()
    root.geometry("930x520")
    root.title('AnimeWatchlist')

    tk.Grid.rowconfigure(root, 0, weight=1)
    tk.Grid.columnconfigure(root, 0, weight=0)
    tk.Grid.columnconfigure(root, 1, weight=1)

    mainpage.AnimeWatchlistUI(root, database, database.loadDatabase(), animeData)

    root.mainloop()
    
main()