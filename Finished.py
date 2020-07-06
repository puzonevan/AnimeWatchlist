""" Finished Profile """
""" 
    Shows: list of Anime Cards
"""

class Finished(): 
    
    def __init__(self, animeCards): 
        self.anime = animeCards

    def addtofinished(self, animeCard): 
        self.anime.append(animeCard)

    def removefromfinished(self, animeCard): 
        self.anime.remove(animeCard)