# TODO: Allow users to input their own search terms
# TODO: Allow users to search based on m/z
# TODO: Print the found metadata to the GUI

import Tkinter as tk  # Importing GUI commands
from pymongo import MongoClient  # For connecting to MongoDB
import matplotlib # For graphing
matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
# implement the default mpl key bindings
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure


class Meta:
    def __init__(self, field, term):
        self.metadata = []
        self.client = MongoClient()
        self.db = self.client['nodbase']
        self.cursor = self.db['meta'].find({field: term})

        self.expID = []

        for self.document in self.cursor:
            self.metadata.append(self.document)


class Chromatogram:
    def __init__(self, expID):
        self.chrom = {}
        self.client = MongoClient()
        self.db = self.client['nodbase']
        self.cursor = self.db['chrom'].find({'expID': expID})

        for self.document in self.cursor:
            self.chrom.update(
                {'retentionTime': self.document['retentionTime'],
                 'bpi': self.document['bpi'],
                 'totion': self.document['totion']})
               #  'ms_level': self.document['ms_level']}) Need to add this post testing


def analyze():
    win = tk.Toplevel()
    win.title("Analyze Nodbase Data")


    message = "This will have the search and analysis functions"
    tk.Label(win, text=message).pack()
    b1 = tk.Button(win, text='Done', command=search)
    b1.pack(side=tk.LEFT, padx=5, pady=5)
    b2 = tk.Button(win, text='Quit', command=win.destroy)
    b2.pack(side=tk.LEFT, padx=5, pady=5)


def search():
    met = Meta('strain', 'SA237')
    chrom = Chromatogram(met.metadata[3]['_id'])
    print(met.metadata)
    print(chrom.chrom)

    win = tk.Toplevel()
    win.title("Search results")

    f = Figure(figsize=(5, 4), dpi=100)
    a = f.add_subplot(111)
    x = chrom.chrom['retentionTime']
    y = chrom.chrom['bpi']

    a.plot(x, y)

    # a tk.DrawingArea
    canvas = FigureCanvasTkAgg(f, master=win)
    canvas.show()
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

    toolbar = NavigationToolbar2TkAgg(canvas, win)
    toolbar.update()
    canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=1)

    def on_key_event(event):
        print('you pressed %s' % event.key)
        key_press_handler(event, canvas, toolbar)

    canvas.mpl_connect('key_press_event', on_key_event)

    button = tk.Button(master=win, text='Quit', command=win.destroy)
    button.pack(side=tk.BOTTOM)


