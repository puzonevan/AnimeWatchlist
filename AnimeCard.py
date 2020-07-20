
""" AnimeCard Profile """
"""
    Name: title of the anime (Your Name)
    Season: season of release (Spring 2019)
    Status: ONGOING or FINISHED
    Picture: picture of anime
    Genre: “tags” in json data 
    Current Episode: 1
"""

from PIL import Image, ImageTk
from io import BytesIO
import requests, json 

class AnimeCard(): 

    def __init__(self, data, category): 

        self.name = ''
        self.season = '' 
        self.status = ''
        self.genre = ''
        self.pictureurl = '' 
        self.source = ''
        self.currentep = 0
        
        if category == 'CurrentSeason': 
            self.name = data[1]
            self.season = data[2]
            self.status = data[3]
            self.genre = data[4]
            self.source = data[5]
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

    def convertPictureUrl(self):
        
        if self.pictureurl == '': 
            return 

        imagerequest = requests.get(self.pictureurl)
        imagedata = imagerequest.content
        convertimg = Image.open(BytesIO(imagedata))
        convertimg = convertimg.resize((100, 150), Image.ANTIALIAS)
        image = ImageTk.PhotoImage(convertimg)

        return image

        
            
    def __str__(self): 
        return "{} | {} | {}".format(self.name, self.season, self.genre)



    
