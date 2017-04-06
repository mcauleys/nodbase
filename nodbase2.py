# TODO: Allow for multiple IDs to be input for the search functions
# TODO: Alter input so that date is a datetime object, not a string
# TODO: Why do the chromatograms come out all wobbly
# TODO: Can we teach the program to detect media peaks?

from pyteomics import mzxml # For reading in XMl data
from pymongo import MongoClient # For connecting to MongoDB
import csv # For exporting data
import pandas as pd # For utilization of dataframes
import matplotlib.pyplot as plt # For graphing
import os # For altering the data directory

class cd:
    # Used in the context of uploading lots of files from a different directory as the home directory
    """Context manager for changing the current working directory"""
    def __init__(self, newPath):
        self.newPath = os.path.expanduser(newPath)

    def __enter__(self):
        self.savedPath = os.getcwd()
        os.chdir(self.newPath)

    def __exit__(self, etype, value, traceback):
        os.chdir(self.savedPath)


def extract(filename, database):
    '''
    Processing the chromatogram for the mzXML file
    :param filename: An mzXML file in the current directory
    :return meta: A dictionary with the experiment specific information
    :return chrom:  A dictionary containing the retention times, base peak intensity and total ion current of a LC-MS run
    :return ms: a dictionary the m/z ratio and the resulting intensities
    '''
    # Establish MongoDB connection
    client = MongoClient()
    db = client[database]

    # Create an iterable from the mzxml file
    file = mzxml.read(filename)

    # Pull the metadata from the filename format
    file_split = filename.split('_')

    retentionTime = []
    bpi = []
    totion = []

    meta = {"strain": file_split[2],
            "date": file_split[0]}

    # Insert Metadata into the database and obtain unique ID
    id = db["meta"].insert_one(meta)
    expID = id.inserted_id
    print("Metadata insertion complete...")
    print("Inserted experiment has ID: " + str(expID))

#TODO: May want to have both chromatograms pulled in the same iterable run
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
    file = mzxml.read(filename)
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
    file = mzxml.read(filename)

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


def search_meta(database, field, term):
    client = MongoClient()
    db = client[database]
    cursor = db["meta"].find({field: term})

    _id = []

    for document in cursor:
        print(document)
        _id.append(document['_id'])

    return _id


# TODO May want to change this to input the MS level you are searching for instead of returning it
def search_chrom(database, expID):
    '''
    Search the MongoDB for a chromatogram with the corresponding Experiment ID
    :param database: the name of the database to search
    :param expID: the experiment ID as a list
    :return: chrom: a dictionary containing the retention time, bpi and total ion current of the chromatogram
    '''
    client = MongoClient()
    db = client[database]
    cursor = db["chrom"].find({"expID": expID})

    chrom = {}

    for document in cursor:
        chrom.update({'retentionTime': document['retentionTime'],
                      'bpi': document['bpi'],
                      'totion': document['totion'],
                      'ms_level': document['ms_level']})

    return chrom


# TODO Need to update to take the ms^2 into account
def search_ms(database, expID, retentiontime):
    '''
    Search the MongoDB for a series of ms spectra with the corresponding Experiment ID
    :param database: the name of the database to search
    :param expID: the experiment ID as a list
    :param retentiontime (float): retention time for the requested spectrum
    :return: chrom: a dictionary containing the retention time, bpi and total ion current of the chromatogram
    '''
    client = MongoClient()
    db = client[database]
    cursor = db["ms"].find({"expID": expID, "retentionTime": retentiontime})

    ms = {}

    for document in cursor:
        ms.update({'m/z': document['m/z'], 'intensity': document['intensity']})

    return ms


def print_csv(filename, data):
    '''
    Prints either a chromatogram or ms spectra of an LC-MS experiment as a .csv file
    :param filename: the name of the output file "example.csv" 
    :param data: a dictionary of lists containing either LC chromtogram or MS data
    :return: a file containing the data 
    '''
    df = pd.DataFrame(data)
    df.to_csv(filename, sep=",")


def print_meta(filename, data):
    '''
    Prints the meta data from an LC-MS experiment to a .csv file
    :param filename: the name of the output file "example.csv" 
    :param data: the experiment metadata you want to print
    :return: a file containing the data 
    '''
    with open(filename, 'wb') as csvfile:
        fieldname = data.keys()

        writer = csv.DictWriter(csvfile, fieldnames=fieldname)
        writer.writeheader()
        writer.writerow(data)


def plot_chrom(chrom, form):
    if form == 1:
        plt.plot(chrom['retentionTime'], chrom['totion'])
        plt.ylabel("Total ion current")
    else:
        plt.plot(chrom['retentionTime'], chrom['bpi'])
        plt.ylabel("Base peak intensity")
    plt.xlabel("Retention Time (minutes)")
    plt.show()


def plot_ms(ms):
    plt.plot(ms['m/z'], ms['intensity'])
    plt.ylabel("Intensity")
    plt.xlabel("m/z")
    plt.show()


def main():
    with cd("/home/scott/PycharmProjects/nodbase/Data"):
        file_names = os.listdir("/home/scott/PycharmProjects/nodbase/Data")
        for file in file_names:
            print("Beginning extraction of " + file)
            extract(file, 'nodbase')
            print (file + " extraction complete")
    print("XML processing successful...")


if __name__ == "__main__":
    main()
