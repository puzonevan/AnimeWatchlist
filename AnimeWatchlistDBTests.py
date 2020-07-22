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
        pass

    def testRemoveFromFinished(self): 
        pass

    def testFilterByGenre(self): 
        pass

    def testFilterByAlpha(self): 
        pass

    def testFilterBySeason(self): 
        pass

    def testCreateAnimeCard(self): 
        pass

    def testCreateAnimeCards(self): 
        pass

    
    """ JSON Tables """ 
    
    

if __name__ == "__main__":
    unittest.main()