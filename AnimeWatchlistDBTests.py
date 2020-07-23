import unittest 
import mysql.connector, json
import AnimeCard as ac
import AnimeWatchlistDB as db
import pprint


database = db.Database()

class testWatchlistDB(unittest.TestCase): 

    """ Helper Anime Card Methods """
    def createCurrentSeasonCard(self): 
        return ac.AnimeCard([0 , 'Anime', 'Summer', 'Ongoing', 'Action', 'url', 'url'], 'CurrentSeason')

    def createFinishedCard(self): 
        return ac.AnimeCard([0 , 'Anime', 'Summer', 'Action', 'url'], 'Finished')

    def createNormalCard(self): 
        return ac.AnimeCard([0 , 'Anime', 'Summer', 'Ongoing', 'Action', 0, 'url'], 'OtherCategory')

    """ Database Tests """ 
    
    def testCreateCurrentSeasonTable(self): 

        # Destroy table and check 
        database.destroyTable('CurrentSeason')
        tables = database.showTables()
        self.assertFalse('CurrentSeason' in tables)

        # Create table and check
        database.createTableCurrentSeason()
        tables = database.showTables()
        self.assertIn('CurrentSeason', tables)


    # def testCreateFinishedTable(self): 
        
    #     # Destroy table and check 
    #     database.destroyTable('Finished')
    #     tables = database.showTables()
    #     self.assertFalse('Finished' in tables)

    #     # Create table and check 
    #     database.createTableFinished()
    #     tables = database.showTables()
    #     self.assertIn('Finished', tables)

    def testCreateWatchlistTable(self): 
        
        # Create random watchlist table and check 
        database.createTableWatchlist('TestTable')
        tables = database.showTables()
        self.assertIn('TestTable', tables) 

        # Delete table after test
        database.destroyTable('TestTable')

    def testDestroyTable(self): 
        
        # Create random table 
        database.createTableWatchlist('TestTable')
        database.destroyTable('TestTable')
        tables = database.showTables()
        self.assertFalse('TestTable' in tables)

    def testDestroyTableDoesNotExist(self): 
        # Destroy non existent table 
        database.destroyTable('TableNotExisted')
        tables = database.showTables()
        self.assertFalse('TableNotExisted' in tables)

    def testGetWatchlistTable(self): 

        # get data from table and make sure length is not 0 
        data = database.getWatchlistTable('Finished')
        self.assertTrue(len(data) != 0)

    def testAddToWatchlist(self): 
        
        # Create Test Table and Test AnimeCard
        database.createTableWatchlist('TestTable') 
        anime = self.createNormalCard()

        database.addToWatchlist('TestTable' ,anime)
        data = database.getWatchlistTable('TestTable')
        self.assertTrue(len(data) != 0) 

        # Destroy Test Table after test
        database.destroyTable('TestTable')

    def testRemoveFromWatchlist(self): 
        
        # Create Test Table and Test Card
        database.createTableWatchlist('TestTable')
        card = self.createNormalCard()

        # Add Card And Remove 
        database.addToWatchlist('TestTable', card)
        database.removeFromWatchlist('TestTable', 'Anime')

        # Get data and check 
        data = database.getWatchlistTable('TestTable')
        self.assertTrue(len(data) == 0)

        # Destroy test table 
        database.destroyTable('TestTable')

    def testAddToFinished(self): 
        
        # Add Anime to finished 
        currentlength = len(database.getWatchlistTable('Finished'))
        database.addToFinished(self.createFinishedCard())
        newlength = len(database.getWatchlistTable('Finished'))

        # Check length 
        self.assertEquals(currentlength + 1, newlength)

    def testRemoveFromFinished(self): 
        
        # Remove same anime from finished 
        currentlength = len(database.getWatchlistTable('Finished'))
        database.removeFromFinished('Anime')
        newlength = len(database.getWatchlistTable('Finished'))

        # Check length 
        self.assertEquals(currentlength - 1, newlength)

    def testFilterByGenre(self): 
        
        # Create test watchlist 
        database.createTableWatchlist('TestTable')

        # Create 3 anime cards with different genres 
        database.addToWatchlist('TestTable', ac.AnimeCard([0 , 'Anime', 'Summer', 'Ongoing', 'Comedy', 0, 'url'], 'OtherCategory'))
        database.addToWatchlist('TestTable', ac.AnimeCard([0 , 'Anime', 'Summer', 'Ongoing', 'Action', 0, 'url'], 'OtherCategory'))
        database.addToWatchlist('TestTable', ac.AnimeCard([0 , 'Anime', 'Summer', 'Ongoing', 'SliceOfLife', 0, 'url'], 'OtherCategory'))

        # Call filter method 
        filtereddata = database.filterByGenre('TestTable')

        # Asserts
        self.assertEquals(filtereddata[0][4], 'Action')
        self.assertEquals(filtereddata[1][4], 'Comedy')
        self.assertEquals(filtereddata[2][4], 'SliceOfLife')

        # Delete Test Table 
        database.destroyTable('TestTable')

    def testFilterByAlpha(self): 
        
        # Create test table 
        database.createTableWatchlist('TestTable')

        # Create 3 anime card with different names 
        database.addToWatchlist('TestTable', ac.AnimeCard([0 , 'Anime3', 'Summer', 'Ongoing', 'Comedy', 0, 'url'], 'OtherCategory'))
        database.addToWatchlist('TestTable', ac.AnimeCard([0 , 'Anime2', 'Summer', 'Ongoing', 'Action', 0, 'url'], 'OtherCategory'))
        database.addToWatchlist('TestTable', ac.AnimeCard([0 , 'Anime1', 'Summer', 'Ongoing', 'SliceOfLife', 0, 'url'], 'OtherCategory'))

        # Call filter method 
        filtereddata = database.filterByAlpha('TestTable')

        # Assert 
        self.assertEquals(filtereddata[0][1], 'Anime1')
        self.assertEquals(filtereddata[1][1], 'Anime2')
        self.assertEquals(filtereddata[2][1], 'Anime3')

        # Destroy test table 
        database.destroyTable('TestTable')

    def testFilterBySeason(self): 
        
        # Create test table 
        database.createTableWatchlist('TestTable')

        # Create 3 anime card with different seasons 
        database.addToWatchlist('TestTable', ac.AnimeCard([0 , 'Anime3', 'Summer 2018', 'Ongoing', 'Comedy', 0, 'url'], 'OtherCategory'))
        database.addToWatchlist('TestTable', ac.AnimeCard([0 , 'Anime2', 'Summer 2016', 'Ongoing', 'Action', 0, 'url'], 'OtherCategory'))
        database.addToWatchlist('TestTable', ac.AnimeCard([0 , 'Anime1', 'Winter 2019', 'Ongoing', 'SliceOfLife', 0, 'url'], 'OtherCategory'))

        # Call filter method 
        filtereddata = database.filterBySeason('TestTable')

        # Assert 
        self.assertEquals(filtereddata[0][2], 'Summer 2016')
        self.assertEquals(filtereddata[1][2], 'Summer 2018')
        self.assertEquals(filtereddata[2][2], 'Winter 2019')

        # Destroy test table
        database.destroyTable('TestTable')

    
    

if __name__ == "__main__":
    unittest.main()