import tkinter as tk 
import mysql.connector
from selenium import webdriver
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
        
        # loop through each key and append 
        for category in dbData.keys(): 
            self.categories.append(category)

    def createWatchlistFrames(self, dbData): 

        # loop through each category and create new Watchlist Frame
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
        self.addremovewatchlistbutton = None
        self.addremoveframe = None
        self.watchlistbuttons = []
        self.buttonsrow = 1
        
        """ AddToWatchlist button """
        self.createAddRemoveWatchlistButton()
        
        """ Category buttons """
        self.createWatchlistButtons()

    """ Helper functions for init """
    def createAddRemoveWatchlistButton(self): 

        # Button for Add / Removing watchlists
        self.addremovewatchlistbutton = tk.Button(
            self, text='Add/Remove', 
            highlightbackground='#242629', 
            pady=10,
            command = lambda: self.addRemoveWatchlistTable(database),
        )

        # Button grids 
        self.addremovewatchlistbutton.grid(row=0, column=0)

    def createWatchlistButtons(self): 

        # Loop through each watchlist frame 
        for position in range(len(self.watchlistframes)): 

            # Create button for each watchlist 
            button = tk.Button(
                self, text=self.categories[position], 
                highlightbackground='#242629', 
                pady=5, 
                command= lambda position=position: self.raiseFrame(self.watchlistframes[position])
            )

            # Button grid 
            button.grid(row=self.buttonsrow, column=0)

            # Increments/appends 
            self.buttonsrow += 1
            self.watchlistbuttons.append(button)

    """ Button Commands """
    def raiseFrame(self, frame): 
        frame.tkraise()

    def addRemoveWatchlistTable(self, database): 
        
        # Create new window
        self.addremoveframe = tk.Toplevel(self)
        self.addremoveframe.geometry("220x110")
        self.addremoveframe.title('Add Watchlist')
        self.addremoveframe.config(bg='#242629')

        # Add Label and text Entry 
        nameLabel = tk.Label(self.addremoveframe, text='Name', fg='#94a1b2', bg='#242629')
        nameEntry= tk.Entry(self.addremoveframe, highlightbackground='#242629')
        nameLabel.place(x=10, y=20)
        nameEntry.place(x=10, y=40)

        # Add button 
        addbutton = tk.Button(
            self.addremoveframe, text="Add",
            highlightbackground='#242629',
            command= lambda: self.addTableAndRefresh(nameEntry.get()),
        )
        # Remove button 
        removebutton = tk.Button(
            self.addremoveframe, text="Remove",
            highlightbackground='#242629',
            command= lambda: self.removeTableAndRefresh(nameEntry.get()),
        )
        addbutton.place(x=90, y=70)
        removebutton.place(x=10, y=70)

    def addTableAndRefresh(self, name): 

        if name != '': 
            # Create table in database 
            database.createTableWatchlist(name)

            # Update categories 
            self.categories.append(name)

            # Refresh dbData 
            dbData = database.loadDatabase()

            # Update watchlist frames
            newwatchlistframe = WatchlistFrame(self.parent, self.categories, name, dbData.get(name))
            self.watchlistframes.append(newwatchlistframe)

            # Add new watchlist button
            categorybutton = tk.Button(
                self, text=name, 
                highlightbackground='#242629', 
                pady=5, 
                command=lambda newwatchlistframe=newwatchlistframe: self.raiseFrame(newwatchlistframe),
            )
            self.watchlistbuttons.append(categorybutton)

            # Add button to end of row 
            categorybutton.grid(row=self.buttonsrow, column=0)
            self.buttonsrow += 1

            # Destroy window 
            self.addremoveframe.destroy()
        
    def removeTableAndRefresh(self, name): 

            # Condition to not destroy current season and finished 
            if name != 'CurrentSeason' and name != 'Finished': 
                # Remove table from database 
                database.destroyTable(name)

                # Loop through buttons till matching name and destroy 
                for button in self.watchlistbuttons:
                    if button['text'] == name: 
                        button.destroy()
                        self.watchlistbuttons.remove(button)
                
                # Destroy window 
                self.addremoveframe.destroy()                    

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

        # Button to update watchlist 
        self.updatewatchlistbutton = tk.Button(
            self, text="Update", 
            highlightbackground='#16161a',
            command=self.updateWatchlistCommand,
        )
        self.updatewatchlistbutton.grid(row=0,column=0)

    def createAddAnimeButton(self): 

        # Button to add anime to watchlist 
        self.addanimebutton = tk.Button(
            self, text='Add Anime', 
            highlightbackground='#16161a',
            command=self.addAnimeCommand,
        )
        self.addanimebutton.grid(row=0, column=1)

    def createLeftRightPageButtons(self): 

        # Frame for left right buttons and label 
        leftrightframe = tk.Frame(self)
        leftrightframe.grid(row=0,column=3)

        # Button to scroll left 
        self.leftpagebutton = tk.Button(
            leftrightframe, text="<<", 
            highlightbackground='#16161a',
            pady=5,
            command=self.leftButtonCommand,
        )

        # Button to scroll right 
        self.rightpagebutton = tk.Button(
            leftrightframe, text=">>",
            highlightbackground='#16161a',
            pady=5,
            command=self.rightButtonCommand,
        )

        # Numerical label for current page
        self.pagelabel = tk.Label(
            leftrightframe, text=str(self.page),
            bg='#16161a', pady=6, fg='#94a1b2',
        )

        # Button grids 
        self.leftpagebutton.grid(row=0, column=0)
        self.pagelabel.grid(row=0, column=1)
        self.rightpagebutton.grid(row=0, column=2)
    
    def createFilterFrame(self):

        # Frame for dropdown and filter button 
        filterFrame = tk.Frame(self)
        filterFrame.grid(row=0, column=2)

        # Dropdown default value 
        self.defaultoption = tk.StringVar(self)
        self.defaultoption.set('A-Z')

        # Dropdown menu 
        self.filterOptions = tk.OptionMenu(
            filterFrame, self.defaultoption,
            'A-Z','Genre','Seasons',
        )
        self.filterOptions.config(bg='#16161a')
        self.filterOptions.grid(row=0, column=0)

        # Button to do filter
        filterbutton = tk.Button(
            filterFrame, text='Filter', 
            highlightbackground='#16161a',
            command=self.filterCommand,
        )
        filterbutton.grid(row=0, column=1)

    def createAnimeCardFrames(self): 

        row = 1
        column = 0
        # Create the first 16 anime card frames 
        for animecard in self.animeCards[self.start:self.finish]: 

            # Create AnimeCardFrame and grid 
            animeCard = AnimeCardFrame(self, self.categories, self.category, animecard)
            animeCard.grid(row=row, column=column, padx=5, pady=5, sticky='nesw')

            self.animeCardFrames.append(animeCard)

            # Organizational increments 
            column += 1
            if column == 4:
                column = 0
                row += 1
        
    """ Button Commands """
    def deleteCurrentAnimeCardFrames(self): 

        # Loop through each AnimeCard object and destroy 
        for animeCardFrame in self.animeCardFrames:
            animeCardFrame.destroy()
    
    def leftButtonCommand(self): 

        # Decrement range 
        if self.start >= 16: 
            self.start -= 16
            self.finish -= 16

        # Delete current anime cards and create new ones 
        self.deleteCurrentAnimeCardFrames()
        self.createAnimeCardFrames()

        # Decrement page number
        if self.page > 1: 
            self.page -= 1
            self.pagelabel.config(text=str(self.page))

    def rightButtonCommand(self):

        # Increment range 
        if self.finish > len(self.animeCardFrames): 
            return 
        self.start += 16
        self.finish += 16

        # Delete current anime cards and create new ones 
        self.deleteCurrentAnimeCardFrames()
        self.createAnimeCardFrames()

        # Increment page number 
        if self.page < (len(self.animeCards)/16):
            self.page += 1
            self.pagelabel.config(text=str(self.page))

    def addAnimeCommand(self): 
        
        # Create new window 
        searchaddanimewindow= tk.Toplevel(self)
        searchaddanimewindow.title('Add Anime')
        searchaddanimewindow.geometry('460x750')
        searchaddanimewindow.config(bg='#242629')

        # Create AddAnimeWindow object for new window
        animewindow = AddAnimeWindow(searchaddanimewindow, self.category)
        animewindow.pack()

    def filterCommand(self): 

        # Get selected option 
        option = self.defaultoption.get()
        
        filtereddata = [] 

        # Filter based on option
        if option == 'A-Z': 
            filtereddata = database.filterByAlpha(self.category)
        elif option == 'Genre': 
            filtereddata = database.filterByGenre(self.category)
        elif option == 'Seasons': 
            filtereddata = database.filterBySeason(self.category)
        
        # Create animecards from filtered data 
        self.animeCards = database.createAnimeCards(filtereddata, self.category)

        # Delete and Create new AnimeCard frames 
        self.deleteCurrentAnimeCardFrames()
        self.createAnimeCardFrames()

    def updateWatchlistCommand(self): 
        
        # Category check
        if self.category == 'CurrentSeason': 
            database.updateCurrentSeasonTable(animeData)

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

        # Content 
        self.picture = None
        self.name = None 
        self.season = None 
        self.genre = None 

        # Additional Functionality
        self.addbutton = None 
        self.removebutton = None 
        self.linkbutton = None 
        self.addtofinished = None

        """ Picture """
        self.createPicture()

        """ Name/Season/Genre """
        self.createNameSeasonGenre()

        """ Additional functionality based on watchlist category """
        self.createAdditionalFunctionality()

    """ Helper methods for init """
    def createPicture(self): 

        # Category check 
        if self.category == 'CurrentSeason': 
            return 

        # Convert AnimeCard pictureurl 
        image = self.animecard.convertPictureUrl()

        # Insert into label 
        self.picture = tk.Label(self, image=image)
        self.picture.photo = image
        self.picture.grid(row=0,column=0, columnspan=3)

    def createNameSeasonGenre(self): 
        
        # Name/Season/Genre 
        self.name = tk.Message(self, text=self.animecard.name, width=170, fg='#fffffe', bg='#242629')
        self.season = tk.Label(self, text=self.animecard.season, fg='#7f5af0', bg='#242629')
        self.genre = tk.Label(self, text=self.animecard.genre, fg='#7f5af0', bg='#242629')

        # Category grid checks 
        if self.category == 'CurrentSeason': 
            self.name.grid(row=0, column=0, columnspan=3)
            self.genre.grid(row=1, column=0, columnspan=2)
        else: 
            self.name.grid(row=1, column=0, columnspan=3)
            self.genre.grid(row=3, column=0, columnspan=3)
            self.season.grid(row=2, column=0, columnspan=2)

    def createAdditionalFunctionality(self): 
        
        # Category checks 
        if self.category == 'CurrentSeason': 

            # CurrentSeason add button 
            self.addbutton = tk.Button(
                self, text='Add', 
                highlightbackground='#242629', 
                command= self.addAnime,
            )

            # CurrentSeason link button 
            self.linkbutton = tk.Button(
                self, text='Click here for source', 
                highlightbackground='#242629', 
                command=self.linkCommand,
            )

            # Grid buttons 
            self.addbutton.grid(row=1, column=2)
            self.linkbutton.grid(row=2, column=0, columnspan=3)

        elif self.category == 'Finished': 

            # Finished remove button 
            self.removebutton = tk.Button(
                self, text='Remove', 
                highlightbackground='#242629', 
                command= self.removeAnime,
            )

            # Button grids 
            self.removebutton.grid(row=2, column=2)

        else: 

            # Watchlist remove button 
            self.removebutton = tk.Button(
                self, text='Remove',
                highlightbackground='#242629',
                command= self.removeAnime, 
            )
            
            # Watchlist add to finished button 
            self.addtofinished = tk.Button(
                self, text='Add to Finished', 
                highlightbackground='#242629', 
                command= self.addAnimeToFinished, 
            )

            # Button grids 
            self.removebutton.grid(row=2, column=2)
            self.addtofinished.grid(row=4, column=0, columnspan=3)

    """ Button Commands """
    def addAnime(self): 

        # Create new window 
        addwindow = tk.Toplevel(self)
        addwindow.title('Add to Watchlist')
        addwindow.geometry("200x200")
        addwindow.config(bg='#242629')

        # Label to add to which playlist
        addLabel = tk.Label(
            addwindow, text='Add to:',
            bg='#242629', fg='#94a1b2'
        )
        addLabel.grid(row=0, column=0)

        # add to database method
        def addToDatabase(name): 
            if name == "Finished": 
                database.addToFinished(self.animecard)
            else: 
                database.addToWatchlist(name, self.animecard)
            addwindow.destroy()

        # Make each watchlist except current one its own button 
        # When button is pressed, the anime is added to that watchlist 
        row = 1
        column = 0
        for cat in self.categories: 
            if cat != self.category:
                catbutton = tk.Button(
                    addwindow, text=cat, 
                    highlightbackground='#242629',
                    command=lambda cat=cat: addToDatabase(cat)
                )
                catbutton.grid(row=row, column=column)
                row += 1
                if row == 4: 
                    row = 1 
                    column += 1

    def removeAnime(self): 
        
        # Category check 
        if self.category == "Finished": 
            database.removeFromFinished(self.animecard.name)
        else: 
            database.removeFromWatchlist(self.category, self.animecard.name)

        # Destroy current AnimeCardFrame
        self.destroy()
    
    def linkCommand(self): 

        # Create Browser
        browser = webdriver.Chrome()
        # Go to link
        browser.get(self.animecard.source)

    def addAnimeToFinished(self): 

        # Add anime to Finished watchlist 
        database.addToFinished(self.animecard)

        # Remove anime from watchlist 
        database.removeFromWatchlist(self.category, self.animecard.name)

        # Destroy Anime Card Frame 
        self.destroy()



""" Add Anime Window Class """
class AddAnimeWindow(tk.Frame): 

    def __init__(self, parent, category): 

        """ Initialize Frame """
        tk.Frame.__init__(self, parent)
        self.config(bg='#242629')

        """ Instance Variables """
        # Parameters 
        self.parent = parent
        self.category = category

        # Non Paramters 
        self.searcharea = None 
        self.leftrightarea = None 
        self.animelist = animeData
        self.animecards = []
        self.start = 0 
        self.finish = 5

        """ Search area """ 
        self.createSearchArea()

        """ Left/Right area """ 
        self.createLeftRightArea()

        """ Anime Cards """ 
        self.createAnimeCards()

    """ Helper functions for init """ 
    def createSearchArea(self): 
        
        # Frame for search entry and button 
        self.searcharea = tk.Frame(self)
        self.searcharea.grid(row=0,column=0)

        # Entry text for user 
        animeentry = tk.Entry(
            self.searcharea, highlightbackground='#242629',
            width=15,
        )
        # Button to generate search 
        searchbutton = tk.Button(
            self.searcharea, text='Search', 
            highlightbackground='#242629',
            command=lambda: self.searchCommand(animeentry.get()),
        )

        # Content grids 
        animeentry.grid(row=0,column=0)
        searchbutton.grid(row=0,column=1)

    def createLeftRightArea(self):

        # Frame for left right buttons 
        self.leftrightarea = tk.Frame(self)
        self.leftrightarea.grid(row=0,column=1)

        # Button to scroll left 
        leftbutton = tk.Button(
            self.leftrightarea, text="<<", 
            highlightbackground='#242629',
            command=self.leftButtonCommand,
        )
        # Button to scroll right 
        rightbutton = tk.Button(
            self.leftrightarea, text=">>", 
            highlightbackground='#242629',
            command=self.rightButtonCommand,
        )

        # Button grids 
        leftbutton.grid(row=0, column=0)
        rightbutton.grid(row=0, column=1)

    def createAnimeCards(self): 

        row = 1
        # Loop and create anime cards for first 5 anime 
        for anime in self.animelist[self.start:self.finish]: 
            animeframe = AnimeCardSearchFrame(self, anime, self.category)
            animeframe.grid(row=row, column=0, columnspan=4, sticky='nsew', pady=2)
            self.animecards.append(animeframe)
            row += 1 

    def deleteAnimeCards(self): 

        # Loop through each animecard frame and destroy 
        for animecard in self.animecards: 
            animecard.destroy()

    """ Button Commands """ 
    def leftButtonCommand(self): 

        # Increment range 
        if self.start >= 5: 
            self.start -= 5
            self.finish -= 5

        # Delete current anime cards and create updated ones 
        self.deleteAnimeCards()
        self.createAnimeCards()

    def rightButtonCommand(self): 

        # Upper bound check 
        if self.finish > len(self.animelist): 
            return 
            
        # Decrement range
        self.start += 5 
        self.finish += 5
        
        # Delete current anime cards and create updated ones 
        self.deleteAnimeCards()
        self.createAnimeCards()

    def searchCommand(self, entry):
        
        # Empty entry: show original animedata
        if entry == '': 
            self.animelist = animeData
            self.deleteAnimeCards()
            self.createAnimeCards() 
        # Non-empty entry: search
        else: 
            searchresults = []
            for anime in animeData: 
                
                # check if entry is in the anime name
                if entry in anime.get('name'): 
                    searchresults.append(anime)
                    continue
                
                # check if entry is in one of the synonyms 
                for synonym in anime.get('synonyms'): 
                    if entry in synonym: 
                        searchresults.append(anime)
                        break
                        
            self.animelist = searchresults 
            self.deleteAnimeCards() 
            self.createAnimeCards()

""" Search Window Class  """ 
class AnimeCardSearchFrame(tk.Frame): 

    """ Constructor """
    def __init__(self, parent, anime, category): 
        
        """ Initialize Frame """
        tk.Frame.__init__(self, parent)
        self.config(bg='#16161a')
        self.config(padx=10, pady=10, width=350)
        

        """ Instance Variables """ 
        # Parameters 
        self.parent = parent
        self.anime = anime
        self.category = category 

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

        # Label for Anime Name 
        self.name = tk.Message(
            self, text=self.anime.get('name'), 
            width=380, pady=5,
            fg='#fffffe', bg='#16161a',
        )
        self.name.grid(row=0,column=0, columnspan=3)

    def createTypeSeasonEpCount(self): 

        # Label for type of anime
        self.type = tk.Label(
            self, text=self.anime.get('type'), 
            fg='#fffffe', bg='#16161a',
        )

        # Label for season of anime
        self.season = tk.Label(
            self, text=self.anime.get('season'), 
            fg='#fffffe', bg='#16161a',
        )

        # Label for episode count of anime 
        self.episodecount = tk.Label(
            self, text="Episode Count: {}".format(self.anime.get('episodecount')),
            fg='#fffffe', bg='#16161a',
        )
        
        # Content Grids
        self.type.grid(row=1, column=0)
        self.season.grid(row=1,column=1)
        self.episodecount.grid(row=1, column=2)

    def createGenreStatus(self): 
        
        # Create string with first 3 genres
        genretext = "" 
        genres = self.anime.get('genres')[0:3]
        for genre in genres: 
            genretext += genre + " "

        # Label for genre of anime 
        self.genre = tk.Label(
            self, text=genretext, 
            fg='#fffffe', bg='#16161a',
        )

        # Label for status of anime 
        self.status = tk.Label(
            self, text=self.anime.get('status'), 
            fg='#fffffe', bg='#16161a',
        )

        # Content grids 
        self.genre.grid(row=2, column=0, columnspan=2)
        self.status.grid(row=2, column=2)

    def createLinkAddButton(self): 
        
        # Button to link to anime source
        self.linkbutton = tk.Button(
            self, text="Click for source",
            highlightbackground='#16161a',
            command=self.linkCommand,
        )

        # Button to add anime to current watchlist 
        self.addbutton = tk.Button(
            self, text='Add Anime', 
            highlightbackground='#16161a',
            command=self.addAnimeCommand,
        )

        # Button grids
        self.linkbutton.grid(row=3, column=0, columnspan=2)
        self.addbutton.grid(row=3, column=2)

    """ Button Commands """ 
    def addAnimeCommand(self): 
        
        # create animecard from anime 
        animecard = database.createAnimeCard(self.formatanime(), self.category)

        # Category checks
        if self.category == 'Finished': 
            database.addToFinished(animecard)
        else: 
            database.addToWatchlist(self.category, animecard)
        
    def linkCommand(self): 

        # Open browser and go to link
        browser = webdriver.Chrome()
        browser.get(self.anime.get('source'))

    """ format anime data to list for animecard """
    def formatanime(self): 

        output = [] 
        # Category Check
        if self.category == 'Finished': 
            output.append(0)
            output.append(self.anime.get('name'))
            output.append(self.anime.get('season'))
            output.append(self.anime.get('genres')[0])
            output.append(self.anime.get('pictureurl'))
        else: 
            output.append(0)
            output.append(self.anime.get('name'))
            output.append(self.anime.get('season'))
            output.append(self.anime.get('status'))
            output.append(self.anime.get('genres')[0])
            output.append(1)
            output.append(self.anime.get('pictureurl'))
        return output