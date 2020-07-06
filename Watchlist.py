""" Watchlist Profile """
"""
    Name: name of watchlist (slice of life watchlist)
    Shows: list of AnimeCards (AnimeCard1, AnimeCard2)
"""

class Watchlist(): 

    id = 1

    def __init__(self, name, animeCards): 
        self.name = '{} {}'.format(name, Watchlist.id)
        self.anime = animeCards
        Watchlist.id += 1
        

    def addtowatchlist(self, animeCard): 
        self.anime.append(animeCard)

    def removefromewatchlist(self, animeCard): 
        self.anime.remove(animeCard)

    