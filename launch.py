from Tkinter import *  # Importing GUI commands
from pymongo import MongoClient  # For connecting to MongoDB
from upload import *  # Move into upload
from analyze import *


def launch(master, collections):
    """
    Initializes the nodbase launch window
    :param master: Tkinter root for GUI
    :param collections: A dictionary of the collection names and number of documents for the database
    :return: NA
    """
    lab = Label(master, width=20, text="Current status of Nodbase")
    lab1 = Label(master, width=10, text="Collections")
    lab2 = Label(master, width=20, text="Number of Documents")
    lab.grid(row=0, column=1, padx=20, pady=12)
    lab1.grid(row=1, column=1, padx=20, pady=12)
    lab2.grid(row=1, column=2, padx=20, pady=12)

    for i, collection in enumerate(collections):
        col = Label(master, width=10, text=collection)
        res = Label(master, width=10, text=collections[collection])
        col.grid(row=(i+2), column=1, padx=20, pady=12)
        res.grid(row=(i+2), column=2, padx=20, pady=12)

    # Buttons
    bottom_frame = Frame(master)
    bottom_frame.grid(row=6, column=1, columnspan=3)

    btn_upload = Button(bottom_frame, text='Upload', width=7, command=upload)
    btn_upload.pack(side='left')
    btn_analyze = Button(bottom_frame, text='Analyze', width=7, command=analyze)
    btn_analyze.pack(side='left', padx=80)
    btn_exit = Button(bottom_frame, text='Exit', width=7, command=root.quit)
    btn_exit.pack(side='right')


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


def fetch(entries):
       result = {}
       for entry in entries:
           field = entry[0]
           text = entry[1].get()
           print('%s: "%s"' % (field, text))

           result[field] = text

       return result


if __name__ == '__main__':
    root = Tk()
    root.title("Welcome to Nodbase")

    col_info = db_info('nodbase')
    launch(root, col_info)

    root.mainloop()


