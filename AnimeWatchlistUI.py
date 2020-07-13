import tkinter as tk 
import mysql.connector
# Debug 
import pprint, time

class AnimeWatchlistUI(tk.Frame): 

    def __init__(self, parent, database, dbData, animeData):

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
            watchlist = WatchlistFrame(parent, database, self.categories, category, dbData.get(category))
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
            pady=10,
            command = self.addToWatchlist,
        )
        self.addWatchlist.grid(row=0, column=0)
        
        """ Category buttons """
        self.categorybuttons = []
        for position in range(len(watchlistframes)): 
            button = tk.Button(
                self, text=categories[position], 
                highlightbackground='#242629', 
                pady=5, 
                command= lambda position=position: self.raiseFrame(watchlistframes[position])
            )
            button.grid(row=position+1, column=0)
            self.categorybuttons.append(button)
        # pprint.pprint(self.categorybuttons)

    
    def raiseFrame(self, frame): 
        frame.tkraise()

    def addToWatchlist(self): 
        
        inputWindow = tk.Toplevel(self)
        inputWindow.geometry("210x80")
        inputWindow.title('Add Watchlist')
        inputWindow.config(bg='#242629')

        nameLabel = tk.Label(inputWindow, text='Name', fg='#94a1b2', bg='#242629')
        nameEntry= tk.Entry(inputWindow, highlightbackground='#242629')
        nameLabel.place(x=10, y=20)
        nameEntry.place(x=10, y=40)

        addbutton = tk.Button(
            inputWindow, text="Add",
            highlightbackground='#242629',
        )
        addbutton.place(x=150, y=40)


class WatchlistFrame(tk.Frame):
    
    def __init__(self, parent, database, categories, category, animeCards):

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
            animeCard = AnimeCardFrame(self, database, categories, category, animecard)
            animeCard.grid(row=row, column=column, padx=5, pady=5, sticky='nesw')
            self.animeCardFrames.append(animeCard)
            column += 1
            if column == 4:
                column = 0
                row += 1
        
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
        for cat in categories: 
            if cat != currentcategory:
                catbutton = tk.Button(
                    addwindow, text=cat, 
                    highlightbackground='#242629',
                    command=lambda cat=cat: addToDatabase(cat, animecard)
                )
                catbutton.grid(row=row, column=0)
                row += 1
                if row == 4: 
                    row = 0 
                    column += 1

    def removeAnime(self, database, category, animecard): 
        if category == "Finished": 
            database.removeFromFinished(animecard.name)
        else: 
            database.removeFromWatchlist(category, animecard.name)
        self.destroy()
        



