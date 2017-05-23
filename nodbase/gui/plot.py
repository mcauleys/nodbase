import Tkinter as tk  # Importing GUI commands
import matplotlib # For graphing
matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure
from bisect import bisect_left # For finding closest retention time

from nodbase.analyze.ms import MS


class Plot:
    def plot_chrom(self, chromatogram):
        self.chromatogram = chromatogram
        self.a.plot(self.chromatogram['retentionTime'], self.chromatogram['bpi'], label=self.chromatogram['expID'])
        self.a.legend(loc='right')

    def pick_ms(self):
        self.cid = self.a.figure.canvas.mpl_connect('button_press_event', self.onclick)

    def onclick(self, event):
        self.clickval = event.xdata
        self.retentiontime = take_closest(self.chromatogram['retentionTime'], self.clickval)

        print("Locating MS Spectra...")
        self.ms = MS(self.chromatogram['expID'], self.retentiontime)

        self.plot_ms()

    def plot_ms(self):
        self.plot_area()
        self.spectra = self.ms.output()
        self.a.plot(self.spectra['m/z'], self.spectra['intensity'], label=self.ms.retentiontime)
        self.a.legend(loc='right')

    def plot_area(self):
        self.win = tk.Toplevel()
        self.win.title("Search results")

        self.f = Figure(figsize=(5, 4), dpi=100)
        self.a = self.f.add_subplot(111)

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
        self.button.pack(side=tk.LEFT)
        self.button = tk.Button(master=self.win, text='Find MS', command=self.pick_ms)
        self.button.pack(side=tk.LEFT)

    def __init__(self):
        self.plot_area()


def take_closest(my_list, my_number):
    """
    Assumes myList is sorted. Returns closest value to myNumber.

    If two numbers are equally close, return the smallest number.
    """
    pos = bisect_left(my_list, my_number)
    if pos == 0:
        return my_list[0]
    if pos == len(my_list):
        return my_list[-1]
    before = my_list[pos - 1]
    after = my_list[pos]
    if after - my_number < my_number - before:
        return after
    else:
        return before
