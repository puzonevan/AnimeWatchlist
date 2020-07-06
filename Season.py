""" Season Profile """ 
""" 
    Name: Spring 2020
    Shows: list of AnimeCards
"""

class Season(): 

    def __init__(self, season, year, animeCards): 
        self.season = season
        self.year = year 
        self.anime = animeCards

    def addtocurrentseason(self, animeCard): 
        self.anime.append(animeCard)
    
    def removefromcurrentseason(self, animeCard): 
        self.anime.remove(animeCard)

    def updatecurrentseason(self, season, year): 
        self.season = season
        self.year = year 

    

