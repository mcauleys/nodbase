import Tkinter as tk  # Importing GUI commands
from nodbase.mongod.search import search_exp
from nodbase.mongod.search import search_chrom_peak
from nodbase.mongod.search import search_ms_peak
from nodbase.analyze.chromatogram import Chromatogram
from plot import Plot


def search_gui(master):
    label = tk.Frame(master)
    label.grid(row=7, column=1, columnspan=3, pady=12)

    lab = tk.Label(label, width=10, text="Search by:")
    lab.pack(side='left')

    # The various search buttons
    btn_search = tk.Frame(master)
    btn_search.grid(row=8, column=1, columnspan=3, pady=12)

    btn_meta = tk.Button(btn_search, text='Metadata', command=meta_search_gui)
    btn_meta.pack(side='left')
    btn_rt = tk.Button(btn_search, text='Retention Time', command=rt_search_gui)
    btn_rt.pack(side='left')
    btn_mz = tk.Button(btn_search, text='M/Z', command=mz_search_gui)
    btn_mz.pack(side='left')


def meta_search_gui():
    win = tk.Toplevel()
    win.title("Search by experiment metadata")
    top_labels = tk.Frame(win)
    top_labels.pack(padx=5, pady=5)

    tk.Label(top_labels, width=10, text="Search field").pack(side='left')
    tk.Label(top_labels, width=10, text="Search term").pack(side='left')

    entries = []

    top_entries = tk.Frame(win)
    top_entries.pack(padx=5, pady=5)

    ent1 = tk.Entry(top_entries)
    ent1.pack(side='left')
    ent2 = tk.Entry(top_entries)
    ent2.pack(side='right')

    entries.append((ent1, ent2))

    bottom_frame = tk.Frame(win)
    bottom_frame.pack(padx=5, pady=5)

    btn_upload = tk.Button(bottom_frame, text='Search', width=10,
                           command=lambda e=entries, w=win: meta_results(w, e))
    btn_upload.pack(side='left')


def rt_search_gui():
    win = tk.Toplevel()
    win.title("Search by retention time")
    top_labels = tk.Frame(win)
    top_labels.pack(padx=5, pady=5)

    tk.Label(top_labels, width=10, text="Retention time").pack(side='left')
    tk.Label(top_labels, width=10, text="Intensity cutoff").pack(side='left')

    entries = []

    top_entries = tk.Frame(win)
    top_entries.pack(padx=5, pady=5)

    ent1 = tk.Entry(top_entries)
    ent1.pack(side='left')
    ent2 = tk.Entry(top_entries)
    ent2.pack(side='right')

    entries.append((ent1, ent2))

    bottom_frame = tk.Frame(win)
    bottom_frame.pack(padx=5, pady=5)

    btn_upload = tk.Button(bottom_frame, text='Search', width=10,
                           command=lambda e=entries, w=win: rt_results(w, e))
    btn_upload.pack(side='left')


def mz_search_gui():
    win = tk.Toplevel()
    win.title("Search by m/z")
    top_labels = tk.Frame(win)
    top_labels.pack(padx=5, pady=5)

    tk.Label(top_labels, width=10, text="m/z").pack(side='left')
    tk.Label(top_labels, width=10, text="Intensity cutoff").pack(side='left')

    entries = []

    top_entries = tk.Frame(win)
    top_entries.pack(padx=5, pady=5)

    ent1 = tk.Entry(top_entries)
    ent1.pack(side='left')
    ent2 = tk.Entry(top_entries)
    ent2.pack(side='right')

    entries.append((ent1, ent2))

    bottom_frame = tk.Frame(win)
    bottom_frame.pack(padx=5, pady=5)

    btn_upload = tk.Button(bottom_frame, text='Search', width=10,
                           command=lambda e=entries, w=win: mz_results(w, e))
    btn_upload.pack(side='left')


def meta_results(win, entries):
    metadata = search_exp(entries)

    # Show the number of results
    res_frame = tk.Frame(win)
    res_frame.pack()
    res_count1 = tk.Label(res_frame, width=20, text="Number of results")
    res_count2 = tk.Label(res_frame, width=20, text=len(metadata))
    res_count1.pack(side='left')
    res_count2.pack(side='right')

#TODO Need to make this more dynamic
    # Define the Result headers
    res_head = tk.Frame(win)
    res_head.pack()
    res_head1 = tk.Label(res_head, width=20, text="Selection")
    res_head4 = tk.Label(res_head, width=20, text="Experiment ID")
    res_head1.pack(side='left')
    res_head4.pack(side='left')

    # Variable for selecting the results you want to test
    var = {}

    for i, result in enumerate(metadata):
        var[result['_id']] = tk.Variable()
        res = tk.Frame(win)
        res.pack()
        res_check = tk.Checkbutton(res,
                                   width=5,
                                   variable=var[result['_id']],
                                   onvalue=1, offvalue=0,
                                   text="")
        res3 = tk.Label(res, width=40, text=result["_id"])
        res_check.pack(side='left')
        res3.pack(side='left')

    # Selection button
    btn_select = tk.Frame(win)
    btn_select.pack()
    btn_select1 = tk.Button(btn_select, text='Select', width=7, command=lambda v=var: find_chrom(v))
    btn_select1.pack(side='left')


def rt_results(win, entries):
    metadata = search_chrom_peak(entries)

    # Show the number of results
    res_frame = tk.Frame(win)
    res_frame.pack()
    res_count1 = tk.Label(res_frame, width=20, text="Number of results")
    res_count2 = tk.Label(res_frame, width=20, text=len(metadata))
    res_count1.pack(side='left')
    res_count2.pack(side='right')

    # Define the Result headers
    res_head = tk.Frame(win)
    res_head.pack()
    res_head1 = tk.Label(res_head, width=20, text="Selection")
    res_head4 = tk.Label(res_head, width=20, text="Experiment ID")
    res_head1.pack(side='left')
    res_head4.pack(side='left')

    # Variable for selecting the results you want to test
    var = {}

    for i, result in enumerate(metadata):
        var[result['_id']] = tk.Variable()
        res = tk.Frame(win)
        res.pack()
        res_check = tk.Checkbutton(res,
                                   width=5,
                                   variable=var[result['_id']],
                                   onvalue=1, offvalue=0,
                                   text="")
        res3 = tk.Label(res, width=40, text=result["_id"])
        res_check.pack(side='left')
        res3.pack(side='left')

    # Selection button
    btn_select = tk.Frame(win)
    btn_select.pack()
    btn_select1 = tk.Button(btn_select, text='Select', width=7, command=lambda v=var: find_chrom(v))
    btn_select1.pack(side='left')


def mz_results(win, entries):
    metadata = search_ms_peak(entries)

    # Show the number of results
    res_frame = tk.Frame(win)
    res_frame.pack()
    res_count1 = tk.Label(res_frame, width=20, text="Number of results")
    res_count2 = tk.Label(res_frame, width=20, text=len(metadata))
    res_count1.pack(side='left')
    res_count2.pack(side='right')

    # Define the Result headers
    res_head = tk.Frame(win)
    res_head.pack()
    res_head1 = tk.Label(res_head, width=20, text="Selection")
    res_head4 = tk.Label(res_head, width=20, text="Experiment ID")
    res_head1.pack(side='left')
    res_head4.pack(side='left')

    # Variable for selecting the results you want to test
    var = {}

    for i, result in enumerate(metadata):
        var[result['_id']] = tk.Variable()
        res = tk.Frame(win)
        res.pack()
        res_check = tk.Checkbutton(res,
                                   width=5,
                                   variable=var[result['_id']],
                                   onvalue=1, offvalue=0,
                                   text="")
        res3 = tk.Label(res, width=40, text=result["_id"])
        res_check.pack(side='left')
        res3.pack(side='left')

    # Selection button
    btn_select = tk.Frame(win)
    btn_select.pack()
    btn_select1 = tk.Button(btn_select, text='Select', width=7, command=lambda v=var: find_chrom(v))
    btn_select1.pack(side='left')


def find_chrom(var):
    # Locates the experiment IDs from the selection and saves them to expID
    chromatos = {}
    bigplot = Plot()
    for exp_id in var:
        if var[exp_id].get() == 1:
            chromatos[exp_id] = Chromatogram(exp_id)

    for key in chromatos:
        bigplot.plot_chrom(chromatos[key].output())

