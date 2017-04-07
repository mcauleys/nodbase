import Tkinter as tk  # Importing GUI commands
from pyteomics import mzxml  # For reading in XMl data
from pymongo import MongoClient  # For connecting to MongoDB


def upload():
    win = tk.Toplevel()
    win.title("Upload mzXML Data to Nodbase")

    fields = ['Filename',
              'Name',
              'String ID',
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
    output = tk.Text(row)
    row.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)
    output.pack(side=tk.LEFT)
    b1 = tk.Button(win, text='Enter',
                   command=lambda: fetch(entries, output))
    b1.pack(side=tk.LEFT, padx=5, pady=5)
    b2 = tk.Button(win, text='Quit', command=win.destroy)
    b2.pack(side=tk.LEFT, padx=5, pady=5)

# No idea why the callback text is only shown if the function throws an error
def callback(s, output):
    print("call back")
    output.insert(tk.END, s)
    output.see(tk.END)
    output.pack()


def fetch(entries, output):
    callback('Extraction beginning...', output)
    """
    Transform data from the GUI into a dictionary for the extract function
    :param entries: the inputs from the GUI
    :return: NA
    """
    meta = {}
    for entry in entries:
        field = entry[0]
        text = entry[1].get()

        meta[field] = text

    """
    Processing the chromatogram, MS and MS^2 data the mzXML file and inputting to MongoDB
    :param meta: The inputted metadata for the experiment
    """
    # Establish MongoDB connection
    client = MongoClient()
    db = client['nodbase']

    # Create an iterable from the mzxml file
    print(meta)
    file = mzxml.read(meta['Filename'])

    retentionTime = []
    bpi = []
    totion = []

    # Insert Metadata into the database and obtain unique ID
    id = db["meta"].insert_one(meta)
    expID = id.inserted_id
    print("Metadata insertion complete...")
    output.insert(tk.END, "Metadata insertion complete...")
    output.see(tk.END)

# TODO: May want to have both chromatograms pulled in the same iterable run?
    # Chromatogram - MS Level 1
    for scan in file:
        if scan['msLevel'] == 1:
            retentionTime.append(scan["retentionTime"])
            bpi.append(scan["basePeakIntensity"])
            totion.append(scan["totIonCurrent"])

    chrom = {"retentionTime": retentionTime,
              "bpi": bpi,
              "totion": totion,
              "ms_level": 1,
             "expID": expID}
    print("Chromatogram extraction complete...")

    # Add the chromatogram to the database
    db["chrom"].insert_one(chrom)
    print("Chromatogram insertion complete...")

    # Remove the chromatogram variable
    del chrom

    # Re-establish iterable file and the holding variables
    file = mzxml.read(meta['Filename'])
    retentionTime = []
    bpi = []
    totion = []

    # Chromatogram - MS Level 2
    for scan in file:
        if scan['msLevel'] == 2:
            retentionTime.append(scan["retentionTime"])
            bpi.append(scan["basePeakIntensity"])
            totion.append(scan["totIonCurrent"])

    chrom = {"retentionTime": retentionTime,
             "bpi": bpi,
             "totion": totion,
             "ms_level": 2,
             "expID": expID}
    print("Chromatogram extraction complete...")

    # Add the chromatogram to the database
    db["chrom"].insert_one(chrom)
    print("Chromatogram insertion complete...")

    # Remove the chromatogram variable
    del chrom
    del bpi
    del retentionTime
    del totion

    # Re-establish iterable file
    file = mzxml.read(meta['Filename'])

    # MS Spectra
    for scan in file:
        spectrum = {"expID": expID,
                    "retentionTime": scan["retentionTime"],
                    "m/z": scan["m/z array"].tolist(),
                    "intensity": scan["intensity array"].tolist()}

        if scan['msLevel'] == 1:
            spectrum['ms_level'] = 1
            db["ms"].insert_one(spectrum)

        elif scan['msLevel'] == 2:
            spectrum['ms_level'] = 2
            db["ms2"].insert_one(spectrum)

    print("MS extraction and insertion complete...")