import tkinter as tk 
import pprint
import mysql.connector

class AnimeWatchlistUI(tk.Frame): 

    def __init__(self, parent, dbData, animeData):

        # Debug 
        # pprint.pprint(dbData)
        # pprint.pprint(animeData)

        """ Root frame """
        tk.Frame.__init__(self, parent)
        self.parent = parent
        
        """ Watchlist categories """
        self.categories = []
        for category in dbData.keys(): 
            self.categories.append(category)
        # pprint.pprint(self.categories)
        
        """ Watchlist frames """
        self.watchlistFrames = []
        for category in self.categories: 
            watchlist = WatchlistFrame(parent, category, dbData.get(category))
            watchlist.grid(row=0, column=1, sticky="nsew")
            self.watchlistFrames.append(watchlist)
        # pprint.pprint(self.watchlistFrames)

        """ Left sidebar frame """
        self.leftsidebar = LeftSideBar(parent, self.categories, self.watchlistFrames)
        self.leftsidebar.grid(row=0, column=0, sticky="nsw")

class LeftSideBar(tk.Frame): 
    

    def __init__(self, parent, categories, watchlistframes):

        # Debug 
        # pprint.pprint(categories) 
        # pprint.pprint(watchlistframes)

        """ Initialize frame """
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.config(bg='#242629', padx=15)

        """ AddToWatchlist button """
        self.addWatchlist = tk.Button(
            self, text='Add Watchlist', 
            highlightbackground='#242629', 
            command = self.addToWatchlist,
        )
        self.addWatchlist.grid(row=0, column=0)
        
        """ Category buttons """
        self.categorybuttons = []
        for position in range(len(watchlistframes)): 
            button = tk.Button(
                self, text=categories[position], 
                highlightbackground='#242629', 
                command= lambda position=position: self.raiseFrame(watchlistframes[position])
            )
            button.grid(row=position+1, column=0)
            self.categorybuttons.append(button)
        # pprint.pprint(self.categorybuttons)

    
    def raiseFrame(self, frame): 
        frame.tkraise()

    def addToWatchlist(self): 
        pass

class WatchlistFrame(tk.Frame):
    
    def __init__(self, parent, category, animeCards):

        # Debug 
        # pprint.pprint(animeCards)
        # print(category)

        """ Initialize frame """ 
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.config(bg='#16161a')

        """ AnimeCard frames """
        row = 0
        column = 0 
        # for animecard in animeCards: 
        #     self.animeCard = AnimeCardFrame(self, animecard)
        #     self.animeCard.grid(row=row, column=column)
        #     column += 1
        #     if column == 4:
        #         column = 0
        #         row += 1

        self.animeCardFrames = [] 
        for animecard in animeCards: 
            animeCard = AnimeCardFrame(self, category, animecard)
            animeCard.grid(row=row, column=column, padx=5, pady=5, sticky='nesw')
            self.animeCardFrames.append(animeCard)
            column += 1
            if column == 4:
                column = 0
                row += 1
        
class AnimeCardFrame(tk.Frame): 
    
    def __init__(self, parent, category, animecard): 

        # Debug 
        # print(category)
        # print(animecard)

        """ Initialize frame """ 
        tk.Frame.__init__(self, parent)
        self.parent = parent 
        self.config(bg='#242629', padx=10, pady=10, width=300)

        self.name = tk.Message(self, text=animecard.name, width=150, fg='#fffffe', bg='#242629')
        self.season = tk.Label(self, text=animecard.season, fg='#94a1b2', bg='#242629')
        self.genre = tk.Label(self, text=animecard.genre, fg='#94a1b2', bg='#242629')
        self.name.grid(row=0, column=1, columnspan=3)
        self.genre.grid(row=1, column=1, columnspan=3)
        self.season.grid(row=2, column=0, columnspan=2)

        if category == 'CurrentSeason': 
            self.addbutton = tk.Button(
                self, text='Add', 
                highlightbackground='#242629', 
            )
            self.linkbutton = tk.Button(
                self, text='Click here for source', 
                highlightbackground='#242629'
            )
            self.addbutton.grid(row=2, column=2)
            self.linkbutton.grid(row=3, column=0, columnspan=3)
        elif category == 'Finished': 
            pass
        else: 
            self.removebutton = tk.Button(
                self, text='Remove',
                highlightbackground='#242629', 
            )
            self.removebutton.grid(row=2, column=2)


        



