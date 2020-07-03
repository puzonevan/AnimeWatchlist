
""" AnimeCard Profile """
"""
    Name: title of the anime (Your Name)
    Season: season of release (Spring 2019)
    Status: ONGOING or FINISHED
    Picture: picture of anime
    Genre: “tags” in json data 
    Current Episode: 1
"""
class AnimeCard(): 

    def __init__(self, data, category): 

        if category == 'CurrentSeason': 
            self.name = data[1]
            self.season = data[2]
            self.status = data[3]
            self.genre = data[4]
            self.pictureurl = data[5]
        elif category == 'Finished': 
            self.name = data[1]
            self.season = data[2]
            self.genre = data[3]
            self.pictureurl = data[4]
        else:
            self.name = data[1]
            self.season = data[2]
            self.status = data[3]
            self.genre = data[4]
            self.currentep = data[5]
            self.pictureurl = data[6]




    
