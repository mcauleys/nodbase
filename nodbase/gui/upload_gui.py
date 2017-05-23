import Tkinter as tk  # Importing GUI commands
from nodbase.mongod.upload import fetch


def upload_gui():
    win = tk.Toplevel()
    win.title("Upload mzXML Data to Nodbase")

    fields = ['Filename',
                   'Name',
                   'Strain ID',
                   'Growth Media',
                   'Growth Method (solid/liquid)',
                   'Illicitor Name',
                   'Illicitor Concentration (uM)',
                   'Extraction Solvent',
                   'Column Type',
                   'Experiment Date',
                   'Upload Date']

    # Establish form for inserting meta data
    entries = []
    for field in fields:
        row = tk.Frame(win)
        lab = tk.Label(row, width=28, text=field, anchor='w')
        ent = tk.Entry(row)
        row.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)
        lab.pack(side=tk.LEFT)
        ent.pack(side=tk.RIGHT, expand=tk.YES, fill=tk.X)
        entries.append((field, ent))

    row = tk.Frame(win)
    b1 = tk.Label(row, text='Processing output:')
    row.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)
    b1.pack(side=tk.LEFT, padx=5, pady=5)

    row = tk.Frame(win)
    output = tk.Text(row)
    row.pack(side=tk.LEFT, fill=tk.X, padx=5, pady=5)
    output.pack()

    row = tk.Frame(win)
    row.pack()
    b1 = tk.Button(row, text='Enter', command=lambda e=entries, w=win, o=output: fetch(e, w, o))
    b1.pack(side=tk.LEFT, padx=5, pady=5)

