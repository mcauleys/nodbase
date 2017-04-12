import Tkinter as tk  # Importing GUI commands
from pyteomics import mzxml  # For reading in XMl data
from pymongo import MongoClient  # For connecting to MongoDB


class Upload:
    def upload(self):
        self.win = tk.Toplevel()
        self.win.title("Upload mzXML Data to Nodbase")

        self.fields = ['Filename',
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
        self.entries = []
        for self.field in self.fields:
            self.row = tk.Frame(self.win)
            self.lab = tk.Label(self.row, width=28, text=self.field, anchor='w')
            self.ent = tk.Entry(self.row)
            self.row.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)
            self.lab.pack(side=tk.LEFT)
            self.ent.pack(side=tk.RIGHT, expand=tk.YES, fill=tk.X)
            self.entries.append((self.field, self.ent))

        self.text_output = tk.Frame(self.win)
        self.output = tk.Text(self.text_output)
        self.text_output.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)
        self.output.pack()

        self.b1 = tk.Button(self.win, text='Enter',
                            command=self.fetch)
        self.b1.pack(side=tk.LEFT, padx=5, pady=5)
        self.b2 = tk.Button(self.win, text='Quit', command=self.win.destroy)
        self.b2.pack(side=tk.LEFT, padx=5, pady=5)

    # No idea why the callback text is only shown if the function throws an error
    def callback(self, s):
        print(s)
        self.output.insert(tk.INSERT, s+'\n')
        self.output.pack()
        self.win.update_idletasks()

    def fetch(self):
        """
        Transform data from the GUI into a dictionary for the extract function
        :param entries: the inputs from the GUI
        :return: NA
        """

        self.callback('Extraction beginning...')

        self.meta = {}
        for self.entry in self.entries:
            self.field = self.entry[0]
            self.text = self.entry[1].get()

            self.meta[self.field] = self.text

        """
        Processing the chromatogram, MS and MS^2 data the mzXML file and inputting to MongoDB
        :param meta: The inputted metadata for the experiment
        """
        # Establish MongoDB connection
        self.client = MongoClient()
        self.db = self.client['nodbase']

        # Create an iterable from the mzxml file
        self.file = mzxml.read(self.meta['Filename'])

        self.retentionTime = []
        self.bpi = []
        self.totion = []

        # Insert Metadata into the database and obtain unique ID
        self.id = self.db["meta"].insert_one(self.meta)
        self.expID = self.id.inserted_id

        self.callback("Metadata insertion complete...")

    # TODO: May want to have both chromatograms pulled in the same iterable run?
        # Chromatogram - MS Level 1
        for self.scan in self.file:
            if self.scan['msLevel'] == 1:
                self.retentionTime.append(self.scan["retentionTime"])
                self.bpi.append(self.scan["basePeakIntensity"])
                self.totion.append(self.scan["totIonCurrent"])

        self.chrom = {"retentionTime": self.retentionTime,
                      "bpi": self.bpi,
                      "totion": self.totion,
                      "ms_level": 1,
                      "expID": self.expID}
        self.callback("MS Chromatogram extraction complete...")

        # Add the chromatogram to the database
        self.db["chrom"].insert_one(self.chrom)
        self.callback("MS Chromatogram insertion complete...")

        # Remove the chromatogram variable
        del self.chrom

        # Re-establish iterable file and the holding variables
        self.file = mzxml.read(self.meta['Filename'])
        self.retentionTime = []
        self.bpi = []
        self.totion = []

        # Chromatogram - MS Level 2
        for self.scan in self.file:
            if self.scan['msLevel'] == 2:
                self.retentionTime.append(self.scan["retentionTime"])
                self.bpi.append(self.scan["basePeakIntensity"])
                self.totion.append(self.scan["totIonCurrent"])

        self.chrom = {"retentionTime": self.retentionTime,
                 "bpi": self.bpi,
                 "totion": self.totion,
                 "ms_level": 2,
                 "expID": self.expID}
        self.callback("MS^2 Chromatogram extraction complete...")

        # Add the chromatogram to the database
        self.db["chrom"].insert_one(self.chrom)
        self.callback("MS^2 Chromatogram insertion complete...")

        # Remove the chromatogram variable
        del self.chrom
        del self.bpi
        del self.retentionTime
        del self.totion

        # Re-establish iterable file
        self.file = mzxml.read(self.meta['Filename'])

        # MS Spectra
        for self.scan in self.file:
            self.spectrum = {"expID": self.expID,
                        "retentionTime": self.scan["retentionTime"],
                        "m/z": self.scan["m/z array"].tolist(),
                        "intensity": self.scan["intensity array"].tolist()}

            if self.scan['msLevel'] == 1:
                self.spectrum['ms_level'] = 1
                self.db["ms"].insert_one(self.spectrum)

            elif self.scan['msLevel'] == 2:
                self.spectrum['ms_level'] = 2
                self.db["ms2"].insert_one(self.spectrum)

        self.callback("MS extraction and insertion complete...")
        self.callback('Thank you for adding your data to Nodbase')

    def __init__(self):
        self.upload()


def upload():
    Upload()
