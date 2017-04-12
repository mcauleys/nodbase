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


class Chromatogram:
    def __init__(self, expID):
        self.find_chrom(expID)
        self.plot()

    def find_chrom(self, expID):
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

    def plot(self):
        self.win = tk.Toplevel()
        self.win.title("Search results")

        self.f = Figure(figsize=(5, 4), dpi=100)
        self.a = self.f.add_subplot(111)
        self.x = self.chrom['retentionTime']
        self.y = self.chrom['bpi']

        self.a.plot(self.x, self.y)

        # a tk.DrawingArea
        self.canvas = FigureCanvasTkAgg(self.f, master=self.win)
        self.canvas.show()
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        self.toolbar = NavigationToolbar2TkAgg(self.canvas, self.win)
        self.toolbar.update()
        self.canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        def on_key_event(event):
            print('you pressed %s' % event.key)
            key_press_handler(event, self.canvas, self.toolbar)

        self.canvas.mpl_connect('key_press_event', on_key_event)

        self.button = tk.Button(master=self.win, text='Quit', command=self.win.destroy)
        self.button.pack(side=tk.BOTTOM)


class Analyze:
    def create_window(self):
        self.win = tk.Toplevel()
        self.win.title("Search and Analyze Nodbase Data")

        self.top_labels = tk.Frame(self.win)
        self.top_labels.pack()

        tk.Label(self.top_labels, width=10, text="Search field").pack(side='left')
        tk.Label(self.top_labels, width=10, text="Search term").pack(side='right')

        self.entries = []

        self.top_entries = tk.Frame(self.win)
        self.top_entries.pack()

        self.ent1 = tk.Entry(self.top_entries)
        self.ent1.pack(side='left')
        self.ent2 = tk.Entry(self.top_entries)
        self.ent2.pack(side='right')

        self.entries.append((self.ent1, self.ent2))

        self.bottom_frame = tk.Frame(self.win)
        self.bottom_frame.pack()

        self.btn_upload = tk.Button(self.bottom_frame, text='Search', width=7, command=self.search)
        self.btn_upload.pack(side='left')
        self.btn_exit = tk.Button(self.bottom_frame, text='Exit', width=7, command=self.win.destroy)
        self.btn_exit.pack(side='right')

    def search(self):
        # This assumes only a single field:term pair
        for self.entry in self.entries:
            field = self.entry[0].get()
            term = self.entry[1].get()

        # Need to search across the metadata and allow for selection of hits
        # Place those hits into separate Meta instances
        self.metadata = []
        self.client = MongoClient()
        self.db = self.client['nodbase']
        self.cursor = self.db['meta'].find({field: term})

        for self.document in self.cursor:
            self.metadata.append(self.document)

        # Show the number of results
        self.res_frame = tk.Frame(self.win)
        self.res_frame.pack()
        self.res_count1 = tk.Label(self.res_frame, width=20, text="Number of results")
        self.res_count2 = tk.Label(self.res_frame, width=20, text=len(self.metadata))
        self.res_count1.pack(side='left')
        self.res_count2.pack(side='right')

        # Define the Result headers
        self.res_head = tk.Frame(self.win)
        self.res_head.pack()
        self.res_head1 = tk.Label(self.res_head, width=20, text="Selection")
        self.res_head2 = tk.Label(self.res_head, width=20, text="Date")
        self.res_head3 = tk.Label(self.res_head, width=20, text="Strain")
        self.res_head4 = tk.Label(self.res_head, width=20, text="Experiment ID")
        self.res_head1.pack(side='left')
        self.res_head2.pack(side='left')
        self.res_head3.pack(side='left')
        self.res_head4.pack(side='left')

        # Variable for selecting the results you want to test
        self.var = {}

        for i, self.result in enumerate(self.metadata):
            self.var[self.result['_id']] = tk.Variable()
            self.res = tk.Frame(self.win)
            self.res.pack()
            self.res_check = tk.Checkbutton(self.res,
                                            width=5,
                                            variable=self.var[self.result['_id']],
                                            onvalue=1, offvalue=0,
                                            text="")
            self.res1 = tk.Label(self.res, width=20, text=self.result["date"])
            self.res2 = tk.Label(self.res, width=20, text=self.result["strain"])
            self.res3 = tk.Label(self.res, width=40, text=self.result["_id"])
            self.res_check.pack(side='left')
            self.res1.pack(side='left')
            self.res2.pack(side='left')
            self.res3.pack(side='left')

        # Selection button
        self.btn_select = tk.Frame(self.win)
        self.btn_select.pack()
        self.btn_select1 = tk.Button(self.btn_select, text='Select', width=7, command=self.find_chrom)
        self.btn_select1.pack()

    def find_chrom(self):
        # Locates the experiment IDs from the selection and saves them to expID
        self.chromatos = {}
        for self.id in self.var:
            if self.var[self.id].get() == 1:
                self.chromatos[self.id] = Chromatogram(self.id)

    def __init__(self):
        self.create_window()


def analyze():
    Analyze()


