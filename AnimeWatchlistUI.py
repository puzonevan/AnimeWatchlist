import tkinter as tk 
import mysql.connector
# Debug 
import pprint, time

""" Global Variables """
database = None 
dbData = None
animeData = None 

""" Main Window """
class AnimeWatchlistUI(tk.Frame): 

    def __init__(self, parent, database, dbData, animeData):

        """ Global Variables """ 
        database = database
        dbData = dbData 
        animeData = animeData
        
        """ Root frame """
        tk.Frame.__init__(self, parent)
        self.parent = parent
        
        """ Watchlist categories """
        self.categories = []
        self.databaseCategories(dbData)
        
        """ Watchlist frames """
        self.watchlistFrames = []
        self.createWatchlistFrames(dbData)

        """ Left sidebar frame """
        self.leftsidebar = LeftSideBar(parent, self.categories, self.watchlistFrames)
        self.leftsidebar.grid(row=0, column=0, sticky="nsw")

    def databaseCategories(self, dbData): 
        for category in dbData.keys(): 
            self.categories.append(category)

    def createWatchlistFrames(self, dbData): 
        for category in self.categories: 
            watchlist = WatchlistFrame(self.parent, self.categories, category, dbData.get(category))
            watchlist.grid(row=0, column=1, sticky="nsew")
            self.watchlistFrames.append(watchlist)

class LeftSideBar(tk.Frame): 
    

    def __init__(self, parent, categories, watchlistframes):

        """ Instance Variables """  
        self.categories = categories 
        self.watchlistframes = watchlistframes

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
            pady=10,
            command = lambda: self.addWatchlistTable(database),
        )
        self.addWatchlist.grid(row=0, column=0)
        
        """ Category buttons """
        self.categorybuttons = []
        self.buttonsrow = 1
        for position in range(len(watchlistframes)): 
            button = tk.Button(
                self, text=categories[position], 
                highlightbackground='#242629', 
                pady=5, 
                command= lambda position=position: self.raiseFrame(watchlistframes[position])
            )
            button.grid(row=self.buttonsrow, column=0)
            self.buttonsrow += 1
            self.categorybuttons.append(button)
        # pprint.pprint(self.categorybuttons)

    
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

            self.categorybuttons.append(categorybutton)
            categorybutton.grid(row=self.buttonsrow, column=0)
            self.buttonsrow += 1
            

        addbutton = tk.Button(
            inputWindow, text="Add",
            highlightbackground='#242629',
            command= lambda: addTableToDatabaseAndRefresh(nameEntry.get()),
        )
        addbutton.place(x=150, y=40)

class WatchlistFrame(tk.Frame):
    
    def __init__(self, parent, categories, category, animeCards):

        """ Instance Variables """ 
        self.categories = categories
        self.category = category
        self.animeCards = animeCards

        # Debug 
        # pprint.pprint(self.database)
        # pprint.pprint(self.categories)
        # print(categories)
        # pprint.pprint(animeCards)
        # pprint.pprint(animeData)

        """ Initialize frame """ 
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.config(bg='#16161a')

        """ Add Anime button """ 
        self.addanimebutton = tk.Button(
            self, text='Add Anime', 
            highlightbackground='#16161a',
            command=self.addAnime,
        )
        self.addanimebutton.grid(row=0, column=2)

        """ Filter Frame """ 
        filterFrame = tk.Frame(self)
        filterFrame.grid(row=0, column=3)
        self.filteroptions = tk.StringVar(self)
        self.filteroptions.set('A-Z')
        self.filterOptions = tk.OptionMenu(
            filterFrame, self.filteroptions,
            'Genre','Seasons', 
        )
        self.filterOptions.config(bg='#16161a')
        self.filterOptions.grid(row=0, column=0)

        self.filterbutton = tk.Button(
            filterFrame, text='Filter', 
            highlightbackground='#16161a',
            command=self.filterCommand,
        )
        self.filterbutton.grid(row=0, column=1)

        """ AnimeCard frames """
        self.animeCardFrames = []
        self.start = 0
        self.finish = 16

        self.createAnimeCardFrames()
        
        self.leftpagebutton = tk.Button(
            self, text="<<", 
            highlightbackground="#16161a",
            command=self.leftPageCommand,
        )

        self.rightpagebutton = tk.Button(
            self, text=">>",
            highlightbackground="#16161a",
            command=self.rightPageCommand,
        )
        self.leftpagebutton.grid(row=5, column=1)
        self.rightpagebutton.grid(row=5, column=2)

    def deleteCurrentAnimeCardFrames(self): 
        for animeCardFrame in self.animeCardFrames:
            animeCardFrame.destroy

    def createAnimeCardFrames(self): 
        row = 1
        column = 0
        for animecard in self.animeCards[self.start:self.finish]: 
            animeCard = AnimeCardFrame(self, database, self.categories, self.category, animecard)
            animeCard.grid(row=row, column=column, padx=5, pady=5, sticky='nesw')
            self.animeCardFrames.append(animeCard)
            column += 1
            if column == 4:
                column = 0
                row += 1
    
    def leftPageCommand(self): 
        if self.start >= 16: 
            self.start -= 16
            self.finish -= 16

        self.deleteCurrentAnimeCardFrames()
        self.createAnimeCardFrames()

    def rightPageCommand(self):
        self.start += 16
        self.finish += 16

        self.deleteCurrentAnimeCardFrames()
        self.createAnimeCardFrames()

    def addAnime(self): 
        
        """ Initialize new window """
        searchaddanimewindow= tk.Toplevel(self)
        searchaddanimewindow.title('Add Anime')
        searchaddanimewindow.geometry('200x500')
        searchaddanimewindow.config(bg='#242629')

    def filterCommand(self): 
        option = self.filteroptions.get()
        
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

class AnimeCardFrame(tk.Frame): 
    
    def __init__(self, parent, database, categories, category, animecard): 

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
        self.name.grid(row=0, column=0, columnspan=3)
        self.genre.grid(row=1, column=0, columnspan=3)
        self.season.grid(row=2, column=0, columnspan=2)

        if category == 'CurrentSeason': 
            self.addbutton = tk.Button(
                self, text='Add', 
                highlightbackground='#242629', 
                command=lambda: self.addAnime(categories, category, database, animecard),
            )
            self.linkbutton = tk.Button(
                self, text='Click here for source', 
                highlightbackground='#242629'
            )
            self.addbutton.grid(row=2, column=2)
            self.linkbutton.grid(row=3, column=0, columnspan=3)
        elif category == 'Finished': 
            self.removebutton = tk.Button(
                self, text='Remove', 
                highlightbackground='#242629', 
                command=lambda: self.removeAnime(database, category, animecard),
            )
            self.removebutton.grid(row=2, column=2)
        else: 
            self.removebutton = tk.Button(
                self, text='Remove',
                highlightbackground='#242629',
                command=lambda: self.removeAnime(database, category, animecard), 
            )
            self.removebutton.grid(row=2, column=2)


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
        



""" Search Window """ 
class AnimeCardSearchFrame(tk.Frame): 

    def __init__(self, parent): 
        
        pass
