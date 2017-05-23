import Tkinter as tk  # Importing GUI commands
import nodbase.mongod as mongod
import upload_gui
import search_gui


def launch(master, collections):
    """
    Initializes the nodbase launch window
    :param master: Tkinter root for GUI
    :param collections: A dictionary of the collection names and number of documents for the database
    :return: NA
    """
    lab = tk.Label(master, width=20, text="Current status of Nodbase:")
    lab1 = tk.Label(master, width=10, text="Collection")
    lab2 = tk.Label(master, width=20, text="Number of Documents")
    lab.grid(row=0, column=1, padx=20, pady=12)
    lab1.grid(row=1, column=1, padx=20, pady=12)
    lab2.grid(row=1, column=2, padx=20, pady=12)

    for i, collection in enumerate(collections):
        col = tk.Label(master, width=10, text=collection)
        res = tk.Label(master, width=10, text=collections[collection])
        col.grid(row=(i+2), column=1, padx=20, pady=12)
        res.grid(row=(i+2), column=2, padx=20, pady=12)

    # Buttons
    bottom_frame = tk.Frame(master)
    bottom_frame.grid(row=6, column=1, columnspan=3, pady=12)

    btn_upload = tk.Button(bottom_frame, text='Upload', width=7,
                           command=upload_gui.upload_gui)
    btn_upload.pack(side='left')
    btn_analyze = tk.Button(bottom_frame, text='Search', width=7,
                            command=lambda m=master: search_gui.search_gui(master))
    btn_analyze.pack(side='left')


root = tk.Tk()
root.title("Welcome to Nodbase")

col_info = mongod.db_info('nodbase')
launch(root, col_info)

root.mainloop()
