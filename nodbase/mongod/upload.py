from pyteomics import mzxml  # For reading in XMl data
from pymongo import MongoClient  # For connecting to MongoDB
import Tkinter as tk  # Importing GUI commands


def fetch(entries, win, output):
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
    callback(win, output, 'Extraction beginning...')

    # Establish MongoDB connection
    client = MongoClient()
    db = client['nodbase']

    # Create an iterable from the mzxml file
    file = mzxml.read(meta['Filename'])

    retentionTime = []
    bpi = []
    totion = []

    # Insert Metadata into the database and obtain unique ID
    id = db["meta"].insert_one(meta)
    expID = id.inserted_id

    callback(win, output, 'Metadata insertion complete...')

    # TODO: May want to have both chromatograms pulled in the same iterable run?
    # Chromatogram - MS Level 1
    for scan in file:
        if scan['msLevel'] == 1:
            retentionTime.append(str(scan["retentionTime"]))
            bpi.append(scan["basePeakIntensity"])
            totion.append(scan["totIonCurrent"])

    chrom = {"retentionTime": retentionTime,
                  "bpi": bpi,
                  "totion": totion,
                  "ms_level": 1,
                  "expID": expID}

    # Add the chromatogram to the database
    db["chrom"].insert_one(chrom)

    callback(win, output, 'MS Chromatogram extraction and insertion complete...')

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
            retentionTime.append(str(scan["retentionTime"]))
            bpi.append(scan["basePeakIntensity"])
            totion.append(scan["totIonCurrent"])

    chrom = {"retentionTime": retentionTime,
             "bpi": bpi,
             "totion": totion,
             "ms_level": 2,
             "expID": expID}

    # Add the chromatogram to the database
    db["chrom"].insert_one(chrom)

    callback(win, output, 'MS^2 Chromatogram extraction and insertion complete...')

    # Remove the chromatogram variable
    del chrom
    del bpi
    del retentionTime
    del totion

    # Re-establish iterable file
    file = mzxml.read(meta['Filename'])

    # MS Spectra
    for scan in file:
        mz = [str(i) for i in scan["m/z array"].tolist()]
        intensity = scan['intensity array'].tolist()

        spectrum = {"expID": expID,
                    "retentionTime": str(scan["retentionTime"]),
                    "m/z": mz,
                    "intensity": intensity}

        if scan['msLevel'] == 1:
            spectrum['ms_level'] = 1
            db["ms"].insert_one(spectrum)

        elif scan['msLevel'] == 2:
            spectrum['ms_level'] = 2
            db["ms2"].insert_one(spectrum)

    callback(win, output, 'MS and MS^2 spectra extraction and insertion complete...')
    callback(win, output, 'Data processing complete. Thank you for contributing to Nodbase')


def callback(win, output, s):
    output.insert(tk.INSERT, s + '\n')
    output.pack()
    win.update_idletasks()
