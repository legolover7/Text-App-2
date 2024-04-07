from pymongo import MongoClient
from env import ENV

def get_database(db_name): 
   # Provide the mongodb atlas url to connect python to mongodb using pymongo
   CONNECTION_STRING = ENV.MONGO_DB_URL
 
   # Create a connection using MongoClient. You can import MongoClient or use pymongo.MongoClient
   client = MongoClient(CONNECTION_STRING)
 
   # Create the database for our example (we will use the same database throughout the tutorial
   return client[db_name]
  
# This is added so that many files can reuse the function get_database()
if __name__ == "__main__":   
   # Get the database
   dbname = get_database("none")