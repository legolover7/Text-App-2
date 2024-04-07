from database.get_database import get_database
dbname = get_database("texting_app")

# Insert an object into the database
def insert(table, object):
    dbname[table].insert_one(object)

# Queries the database
def query(table, collection="", query={}, limit=20):
    collection_name = dbname[table]

    if collection != "":
        category_index = collection_name.create_index(collection)

    collection = collection_name if collection == "" else category_index
    if query != {}:
        item_details = collection.find(query).limit(limit)
    else:
        item_details = collection.find().limit(limit).sort({"_id":1})
    return item_details