import tkinter as tk 
import mysql.connector
# Debug 
# import pprint, time

""" Global Variables """
database = None 
dbData = None
animeData = None 

""" Main Window Class """
class AnimeWatchlistUI(tk.Frame): 

    """ Constructor """
    def __init__(self, parent, db, dbDatas, animeDatas):

        """ Initialize Frame """
        tk.Frame.__init__(self, parent)

        """ Global Variables """ 
        # Parameters
        global database
        database = db
        global dbData
        dbData = dbDatas
        global animeData
        animeData = animeDatas

        """ Instance Variables """ 
        # Non-Parameters
        self.parent = parent 
        self.categories = []
        self.watchlistFrames = []
        
        
        """ Watchlist categories """
        self.databaseCategories(dbData)
        
        """ Watchlist frames """
        self.createWatchlistFrames(dbData)

        """ Left sidebar frame """
        self.leftsidebar = LeftSideBar(parent, self.categories, self.watchlistFrames)
        self.leftsidebar.grid(row=0, column=0, sticky="nsw")

    """ Helper functions for init """
    def databaseCategories(self, dbData): 
        for category in dbData.keys(): 
            self.categories.append(category)

    def createWatchlistFrames(self, dbData): 
        for category in self.categories: 
            watchlist = WatchlistFrame(self.parent, self.categories, category, dbData.get(category))
            watchlist.grid(row=0, column=1, sticky="nsew")
            self.watchlistFrames.append(watchlist)

""" Left Side Bar Class """
class LeftSideBar(tk.Frame): 
    
    """ Constructor """
    def __init__(self, parent, categories, watchlistframes):

        """ Initialize frame """
        tk.Frame.__init__(self, parent)
        self.config(bg='#242629', padx=15)

        """ Instance Variables """  
        # Parameters 
        self.parent = parent
        self.categories = categories 
        self.watchlistframes = watchlistframes
        
        # Non-Parameters
        self.addwatchlistbutton = None
        self.watchlistbuttons = []
        self.buttonsrow = 1
        
        """ AddToWatchlist button """
        self.createAddWatchlistButton()
        
        """ Category buttons """
        self.createWatchlistButtons()

    """ Helper functions for init """
    def createAddWatchlistButton(self): 
        self.addwatchlistbutton = tk.Button(
            self, text='Add Watchlist', 
            highlightbackground='#242629', 
            pady=10,
            command = lambda: self.addWatchlistTable(database),
        )
        self.addwatchlistbutton.grid(row=0, column=0)

    def createWatchlistButtons(self): 
        for position in range(len(self.watchlistframes)): 
            button = tk.Button(
                self, text=self.categories[position], 
                highlightbackground='#242629', 
                pady=5, 
                command= lambda position=position: self.raiseFrame(self.watchlistframes[position])
            )
            button.grid(row=self.buttonsrow, column=0)
            self.buttonsrow += 1
            self.watchlistbuttons.append(button)

    """ Button Commands """
    def raiseFrame(self, frame): 
        frame.tkraise()

    def addWatchlistTable(self, database): 
        
        inputWindow = tk.Toplevel(self)
        inputWindow.geometry("210x80")
        inputWindow.title('Add Watchlist')
        inputWindow.config(bg='#242629')

        nameLabel = tk.Label(inputWindow, text='Name', fg='#94a1b2', bg='#242629')
        nameEntry= tk.Entry(inputWindow, highlightbackground='#242629')
        nameLabel.place(x=10, y=20)
        nameEntry.place(x=10, y=40)

        def addTableToDatabaseAndRefresh(name): 
            if name != '': 
                database.createTableWatchlist(name)
                inputWindow.destroy()
            

            categorybutton = tk.Button(
                self, text=name, 
                highlightbackground='#242629', 
                pady=5, 
            )

            self.watchlistbuttons.append(categorybutton)
            categorybutton.grid(row=self.buttonsrow, column=0)
            self.buttonsrow += 1
            

        addbutton = tk.Button(
            inputWindow, text="Add",
            highlightbackground='#242629',
            command= lambda: addTableToDatabaseAndRefresh(nameEntry.get()),
        )
        addbutton.place(x=150, y=40)

""" Watchlist Class """
class WatchlistFrame(tk.Frame):
    
    """ Constructor """
    def __init__(self, parent, categories, category, animeCards):

        """ Initialize frame """ 
        tk.Frame.__init__(self, parent)
        self.config(bg='#16161a')

        """ Instance Variables """ 
        # Parameters
        self.categories = categories
        self.category = category
        self.animeCards = animeCards

        # Non-Parameters
        self.parent = parent
        self.updatewatchlistbutton = None
        self.addanimebutton = None
        self.defaultoption = None 
        self.filterOptions = None 
        self.animeCardFrames = [] 
        self.start = 0
        self.finish = 16
        self.page = 1
        self.leftpagebutton = None
        self.pagelabel = None  
        self.rightpagebutton = None 

        """ Update watchlist button """
        self.createUpdateWatchlistButton()

        """ Add Anime button """ 
        self.createAddAnimeButton()

        """ Filter Frame """ 
        self.createFilterFrame()

        """ AnimeCard frames """
        self.createAnimeCardFrames()
        
        """ Left/Right page buttons """
        self.createLeftRightPageButtons()

    """ Helper functions for init """
    def createUpdateWatchlistButton(self): 
        self.updatewatchlistbutton = tk.Button(
            self, text="Update", 
            highlightbackground='#16161a',
            command=self.updateWatchlistCommand,
        )
        self.updatewatchlistbutton.grid(row=0,column=0)

    def createAddAnimeButton(self): 
        self.addanimebutton = tk.Button(
            self, text='Add Anime', 
            highlightbackground='#16161a',
            command=self.addAnimeCommand,
        )
        self.addanimebutton.grid(row=0, column=1)

    def createLeftRightPageButtons(self): 
        leftrightframe = tk.Frame(self)
        leftrightframe.grid(row=0,column=3)
        self.leftpagebutton = tk.Button(
            leftrightframe, text="<<", 
            highlightbackground='#16161a',
            pady=5,
            command=self.leftButtonCommand,
        )
        self.rightpagebutton = tk.Button(
            leftrightframe, text=">>",
            highlightbackground='#16161a',
            pady=5,
            command=self.rightButtonCommand,
        )
        self.pagelabel = tk.Label(
            leftrightframe, text=str(self.page),
            bg='#16161a', pady=6, fg='#94a1b2',
        )
        self.leftpagebutton.grid(row=0, column=0)
        self.pagelabel.grid(row=0, column=1)
        self.rightpagebutton.grid(row=0, column=2)
    
    def createFilterFrame(self):
        filterFrame = tk.Frame(self)
        filterFrame.grid(row=0, column=2)
        self.defaultoption = tk.StringVar(self)
        self.defaultoption.set('A-Z')
        self.filterOptions = tk.OptionMenu(
            filterFrame, self.defaultoption,
            'A-Z','Genre','Season',
        )
        self.filterOptions.config(bg='#16161a')
        self.filterOptions.grid(row=0, column=0)

        filterbutton = tk.Button(
            filterFrame, text='Filter', 
            highlightbackground='#16161a',
            command=self.filterCommand,
        )
        filterbutton.grid(row=0, column=1)

    def createAnimeCardFrames(self): 
        row = 1
        column = 0
        for animecard in self.animeCards[self.start:self.finish]: 
            animeCard = AnimeCardFrame(self, self.categories, self.category, animecard)
            animeCard.grid(row=row, column=column, padx=5, pady=5, sticky='nesw')
            self.animeCardFrames.append(animeCard)
            column += 1
            if column == 4:
                column = 0
                row += 1
        
    """ Button Commands """
    def deleteCurrentAnimeCardFrames(self): 
        for animeCardFrame in self.animeCardFrames:
            animeCardFrame.destroy()
    
    def leftButtonCommand(self): 
        if self.start >= 16: 
            self.start -= 16
            self.finish -= 16

        self.deleteCurrentAnimeCardFrames()
        self.createAnimeCardFrames()
        if self.page > 1: 
            self.page -= 1
            self.pagelabel.config(text=str(self.page))

    def rightButtonCommand(self):
        self.start += 16
        self.finish += 16

        self.deleteCurrentAnimeCardFrames()
        self.createAnimeCardFrames()
        if self.page < (len(self.animeCards)/16):
            self.page += 1
            self.pagelabel.config(text=str(self.page))

    def addAnimeCommand(self): 
        
        """ Initialize new window """
        searchaddanimewindow= tk.Toplevel(self)
        searchaddanimewindow.title('Add Anime')
        searchaddanimewindow.geometry('400x750')
        searchaddanimewindow.config(bg='#242629')



        start = 0
        finish = 5
        for anime in animeData[start:finish]: 
            animeframe = AnimeCardSearchFrame(searchaddanimewindow, anime)
            animeframe.pack(side=tk.TOP, pady=5)

        leftbutton = tk.Button(
            searchaddanimewindow, text="<<", 
            highlightbackground='#242629'
        )
        leftbutton.place(x=100, y=720)
        rightbutton = tk.Button(
            searchaddanimewindow, text=">>", 
            highlightbackground='#242629'
        )
        rightbutton.place(x=250, y=720)

    def filterCommand(self): 
        option = self.defaultoption.get()
        
        if option == 'A-Z': 
            filtereddata = database.filterByAlpha(self.category)
            self.animeCards = database.createAnimeCards(filtereddata, self.category)
            self.deleteCurrentAnimeCardFrames()
            self.createAnimeCardFrames()
        elif option == 'Genre': 
            filtereddata = database.filterByGenre(self.category)
            self.animeCards = database.createAnimeCards(filtereddata, self.category)
            self.deleteCurrentAnimeCardFrames()
            self.createAnimeCardFrames()
        elif option == 'Seasons': 
            filtereddata = database.filterBySeason(self.category)
            self.animeCards = database.createAnimeCards(filtereddata, self.category)
            self.deleteCurrentAnimeCardFrames()
            self.createAnimeCardFrames()

    def updateWatchlistCommand(self): 
        
        # Update the animecards using the database 
        self.animeCards = database.createAnimeCards(database.getWatchlistTable(self.category), self.category)
        
        # Delete the current anime cards 
        self.deleteCurrentAnimeCardFrames()

        # Create the new anime cards 
        self.createAnimeCardFrames()


""" Anime Card Class """
class AnimeCardFrame(tk.Frame): 
    
    """ Constructor """
    def __init__(self, parent, categories, category, animecard): 

        """ Initialize frame """ 
        tk.Frame.__init__(self, parent)
        self.config(bg='#242629', padx=10, pady=10, width=300)

        """ Instance Variables """
        # Parameters 
        self.parent = parent 
        self.categories = categories 
        self.category = category 
        self.animecard = animecard

        # Non-Parameters 
        self.name = None 
        self.season = None 
        self.genre = None 
        self.addbutton = None 
        self.removebutton = None 
        self.linkbutton = None 

        """ Name/Season/Genre """
        self.createNameSeasonGenre()

        """ Additional functionality based on watchlist category """
        self.createAdditionalFunctionality()

    """ Helper methods for init """
    def createNameSeasonGenre(self): 
        self.name = tk.Message(self, text=self.animecard.name, width=150, fg='#fffffe', bg='#242629')
        self.season = tk.Label(self, text=self.animecard.season, fg='#94a1b2', bg='#242629')
        self.genre = tk.Label(self, text=self.animecard.genre, fg='#94a1b2', bg='#242629')
        self.name.grid(row=0, column=0, columnspan=3)
        self.genre.grid(row=1, column=0, columnspan=3)
        self.season.grid(row=2, column=0, columnspan=2)

    def createAdditionalFunctionality(self): 
        if self.category == 'CurrentSeason': 
            self.addbutton = tk.Button(
                self, text='Add', 
                highlightbackground='#242629', 
                command=lambda: self.addAnime(self.categories, self.category, database, self.animecard),
            )
            self.linkbutton = tk.Button(
                self, text='Click here for source', 
                highlightbackground='#242629'
            )
            self.addbutton.grid(row=2, column=2)
            self.linkbutton.grid(row=3, column=0, columnspan=3)
        elif self.category == 'Finished': 
            self.removebutton = tk.Button(
                self, text='Remove', 
                highlightbackground='#242629', 
                command=lambda: self.removeAnime(database, self.category, self.animecard),
            )
            self.removebutton.grid(row=2, column=2)
        else: 
            self.removebutton = tk.Button(
                self, text='Remove',
                highlightbackground='#242629',
                command=lambda: self.removeAnime(database, self.category, self.animecard), 
            )
            self.removebutton.grid(row=2, column=2)

    """ Button Commands """
    def addAnime(self, categories, currentcategory, database, animecard): 
        addwindow = tk.Toplevel(self)
        addwindow.title('Add to Watchlist')
        addwindow.geometry("200x200")
        addwindow.config(bg='#242629')

        addLabel = tk.Label(
            addwindow, text='Add to:',
            bg='#242629', fg='#94a1b2'
        )
        addLabel.grid(row=0, column=0)

        def addToDatabase(name, animecard): 
            if name == "Finished": 
                database.addToFinished(animecard)
            else: 
                database.addToWatchlist(name, animecard)
            addwindow.destroy()

        row = 1
        column = 0
        for cat in categories: 
            if cat != currentcategory:
                catbutton = tk.Button(
                    addwindow, text=cat, 
                    highlightbackground='#242629',
                    command=lambda cat=cat: addToDatabase(cat, animecard)
                )
                catbutton.grid(row=row, column=column)
                row += 1
                if row == 4: 
                    row = 1 
                    column += 1

    def removeAnime(self, database, category, animecard): 
        if category == "Finished": 
            database.removeFromFinished(animecard.name)
        else: 
            database.removeFromWatchlist(category, animecard.name)
        self.destroy()
        


""" Search Window Class  """ 
class AnimeCardSearchFrame(tk.Frame): 

    """ Constructor """
    def __init__(self, parent, anime): 
        
        """ Initialize Frame """
        tk.Frame.__init__(self, parent)
        self.config(bg='#16161a')
        self.config(width=400, padx=10, pady=10)
        

        """ Instance Variables """ 
        # Parameters 
        self.parent = parent
        self.anime = anime

        # Non-Parameters 
        self.name = None 
        self.type = None 
        self.season = None 
        self.episodecount = None
        self.genre = None 
        self.status = None
        self.addbutton = None
        self.linkbutton = None

        """ Name """
        self.createName() 

        """ Type Season EpCount """
        self.createTypeSeasonEpCount()

        """ Genre Status """
        self.createGenreStatus() 

        """ Link button """
        self.createLinkAddButton()

    """ Helper functions for init """
    def createName(self): 
        self.name = tk.Message(
            self, text=self.anime.get('name'), 
            width=380, pady=5,
            fg='#fffffe', bg='#16161a',
        )
        self.name.grid(row=0,column=0, columnspan=3)

    def createTypeSeasonEpCount(self): 
        self.type = tk.Label(
            self, text=self.anime.get('type'), 
            fg='#fffffe', bg='#16161a',
        )
        self.type.grid(row=1, column=0)

        self.season = tk.Label(
            self, text=self.anime.get('season'), 
            fg='#fffffe', bg='#16161a',
        )
        self.season.grid(row=1,column=1)

        self.episodecount = tk.Label(
            self, text="Episode Count: {}".format(self.anime.get('episodecount')),
            fg='#fffffe', bg='#16161a',
        )
        self.episodecount.grid(row=1, column=2)

    def createGenreStatus(self): 

        genretext = "" 
        genres = self.anime.get('genres')[0:3]
        for genre in genres: 
            genretext += genre + " "

        self.genre = tk.Label(
            self, text=genretext, 
            fg='#fffffe', bg='#16161a',
        )
        self.genre.grid(row=2, column=0, columnspan=2)

        self.status = tk.Label(
            self, text=self.anime.get('status'), 
            fg='#fffffe', bg='#16161a',
        )
        self.status.grid(row=2, column=2)

    def createLinkAddButton(self): 

        self.linkbutton = tk.Button(
            self, text="Click for source",
            highlightbackground='#16161a',
        )
        self.linkbutton.grid(row=3, column=0, columnspan=2)

        self.addbutton = tk.Button(
            self, text='Add Anime', 
            highlightbackground='#16161a',
        )
        self.addbutton.grid(row=3, column=2)