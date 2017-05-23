from pymongo import MongoClient  # For connecting to MongoDB


def db_info(database):
    """
    Fetches the names of the collections and the number of documents in each collection
    :param database: (str) database name
    :return doc_count: (dict) {collection name: number of documents} 
    """
    client = MongoClient()
    db = client[database]
    col = db.collection_names()

    doc_count = {}

    for collection in col:
        doc_count[collection] = db[collection].count()

    return doc_count
