""" Watchlist Profile """
"""
    Name: name of watchlist (slice of life watchlist)
    Shows: list of AnimeCards (AnimeCard1, AnimeCard2)
"""

class Watchlist(): 

    def __init__(self, name): 
        self.name = name
        self.anime = []

    def addtowatchlist(self, animeCard): 
        self.anime.append(animeCard)

    def removefromewatchlist(self, animeCard): 
        self.anime.remove(animeCard)

    